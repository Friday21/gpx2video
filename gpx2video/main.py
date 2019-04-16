import json

import redis
import numpy as np
import gpxpy.gpx
import matplotlib.pyplot as plt
from PIL import Image

from gpx2video.map import get_tile_bound, merge_tile_pic, deg2pixel, wgs84togcj02, deg2num, num2deg, gcj02towgs84
from raster2xyz.raster2xyz import Raster2xyz
from gpx2video.dem_db import Dem
from mayavi import mlab
from tvtk.api import tvtk
from scipy.interpolate import griddata
from osgeo import gdal

r = redis.Redis(host='localhost', port=6379, db=0)
gpx_file = open('data/太子湾.gpx', 'r')
gpx = gpxpy.parse(gpx_file)


level = 16


def draw_pics():
    points = []
    cnt = 1
    row_start, row_end, col_start, col_end, row, col = 0, 100000000, 0, 100000000, None, None
    dem_data = None
    X, Y, Z = None, None, None
    img = None
    for track in gpx.tracks:
        for segment in track.segments:
            total = len(segment.points)
            for point in segment.points:
                zoom = level
                lng, lat = wgs84togcj02(point.longitude, point.latitude)
                col, row = deg2num(lat, lng, zoom)
                row_range = (row_end - row_start + 1) * 256
                col_range = (col_end - col_start + 1) * 256
                pixel_x, pixel_y = deg2pixel(lat, lng, zoom)
                x_ax = (((col - col_start) * 256) + pixel_x) / col_range * 1920
                y_ax = (1 - ((row - row_start) * 256 + pixel_y) / row_range) * 1920

                if x_ax < 50 or x_ax > 1800 or y_ax < 50 or y_ax > 1800:
                    # 当坐标不合适时刷新背景图片
                    print('refresh background')
                    row_start, row_end, col_start, col_end, row, col = get_tile_bound(lat, lng, zoom)
                    row_range = (row_end - row_start + 1) * 256
                    col_range = (col_end - col_start + 1) * 256
                    pixel_x, pixel_y = deg2pixel(lat, lng, zoom)
                    x_ax = (((col - col_start) * 256) + pixel_x) / col_range * 1920
                    y_ax = (1 - ((row - row_start) * 256 + pixel_y) / row_range) * 1920
                    img = merge_tile_pic(zoom, row_start, row_end, col_start, col_end)
                    # TODO 获取对应的dem 数据
                    dem_data = get_dem_data(row_start, row_end, col_start, col_end, zoom)

                image = img.copy()
                points.append({'row': row, 'col': col, 'pixel_x': pixel_x, 'pixel_y': pixel_y})
                x_axes, y_axes = cal_ax(points, row_start, row_end, col_start, col_end, col_range, row_range)

                plt.figure(figsize=(12, 12))
                plt.axis([-1920, 1920, -1920, 1920])
                plt.plot(x_axes, y_axes, 'b')
                plt.plot(x_ax, y_ax, 'bo', marker="*")
                plt.axis('off')

                plt.savefig('tmp.png', transparent=True, bbox_inches='tight')
                plt.close()

                pil_image = Image.open('tmp.png')
                pil_image = pil_image.resize((3840, 3840))
                pil_image = pil_image.crop((1920, 0, 3840, 1920))
                pil_image = pil_image.resize((1920, 1920))

                image.paste(pil_image, (0, 0), mask=pil_image)
                # TODO size 应该和行列成比例——> 差值？？

                image = image.rotate(180)
                image.save('output/{:0>6}.png'.format(cnt))

                bmp1 = tvtk.PNGReader(file_name='output/{:0>6}.png'.format(cnt))

                my_texture = tvtk.Texture(input_connection=bmp1.output_port, interpolate=1)

                mlab.figure(size=(3000, 3000), bgcolor=(0.16, 0.28, 0.46))
                scene = mlab.gcf().scene
                scene.set_size((1920, 1920))
                surf = mlab.surf(dem_data, color=(1, 1, 1), warp_scale=0.2)
                # mlab.show()
                mlab.savefig('output/raw.png')
                surf.actor.enable_texture = True
                surf.actor.tcoord_generator_mode = 'plane'
                surf.actor.actor.texture = my_texture
                mlab.savefig('output/dem.png')
                mlab.show()
                break

                cnt += 1
                # TODO crop to 1920 * 1080
                image.save('output/{:0>6}.png'.format(cnt))
                print('save {} of {}'.format(cnt, total))


def extract_xyz_from_dem():
    input_raster = 'DEM30.tif'
    output = 'hz.csv'
    rtxyz = Raster2xyz()
    x, y, z = rtxyz.translate(input_raster, output)
    return x, y, z


def get_dem_data(row_start, row_end, col_start, col_end, zoom):
    key = 'dem_{}'.format(zoom)
    row_key = 'dem_row'
    redis_data = r.get(key)
    if redis_data:
        row = int(r.get(row_key))
        data = np.array(json.loads(redis_data)).reshape(row, -1)
        return data
    print('get dem data')
    left_top_lat, left_top_lon = num2deg(col_start, row_start, zoom)
    right_down_lat, right_down_lon = num2deg(col_end + 1, row_end + 1, zoom)
    left_top_lon, left_top_lat = gcj02towgs84(left_top_lon, left_top_lat)
    right_down_lon, right_down_lat = gcj02towgs84(right_down_lon, right_down_lat)

    long, lat, height = extract_xyz_from_dem()
    print(type(height[0]))
    print(type(int(height[0])))
    length = len(lat)
    data = []
    row = 0
    first = False
    # 二分法查找第一个小于left_top_lat的点
    start_i = 0
    end_i = length
    while start_i < end_i:
        mid = (start_i + end_i) // 2
        if lat[mid] > left_top_lat:
            start_i = mid + 10000
        elif lat[mid] < left_top_lat:
            end_i = mid - 10000
        else:
            start_i = mid
            break
    print('start i', start_i)
    print(lat[start_i], left_top_lat)
    start_i = start_i - 10000 if start_i > 10000 else start_i

    # TODO 待优化
    for i in range(start_i, length):
        if lat[i] < right_down_lat:
            break
        if right_down_lat <= lat[i] <= left_top_lat and left_top_lon <= long[i] <= right_down_lon:
            data.append(int(height[i]))
            if not first:
                row += 1
                first = True
        else:
            first = False
    r.set(key, json.dumps(data))
    r.set(row_key, row)
    data = np.array(data).reshape(row, -1)
    print('get dem data done')
    return data


def cal_ax(points, row_start, row_end, col_start, col_end, col_range, row_range):
    x_axes = []
    y_axes = []
    for point in points:
        x_ax = ((point['col'] - col_start) * 256 + point['pixel_x']) / col_range * 1920
        y_ax = (1 - ((point['row'] - row_start) * 256 + point['pixel_y']) / row_range) * 1920
        x_axes.append(x_ax)
        y_axes.append(y_ax)
    return x_axes, y_axes


if __name__ == '__main__':
    # ffmpeg -start_number 001 -r 10 -i output/%6d.png -pix_fmt yuv420p test5.mp4
    draw_pics()
