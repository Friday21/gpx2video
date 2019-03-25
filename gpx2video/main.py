import gpxpy.gpx
import matplotlib.pyplot as plt
from PIL import Image

from gpx2video.map import get_tile_bound, merge_tile_pic, num2deg

gpx_file = open('data/太子湾.gpx', 'r')
gpx = gpxpy.parse(gpx_file)


level = 16


def draw_pics():
    points = []
    cnt = 0
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                points.append(point)
                row_start, row_end, col_start, col_end = get_tile_bound(point.latitude, point.longitude, level)
                img = merge_tile_pic(level, row_start, row_end, col_start, col_end)
                left_top_latitude, left_top_longitude = num2deg(col_start, row_start, level)
                right_down_latitude, right_down_longitude = num2deg(col_end + 1, row_end + 1, level)
                row_range = left_top_latitude - right_down_latitude
                col_range = right_down_longitude - left_top_longitude

                plt.axis([0, 1920, 0, 1920])

                x_axes, y_axes = cal_ax(points, left_top_latitude, left_top_longitude,
                                        right_down_latitude, right_down_longitude, col_range, row_range)

                # TODO WRONG ！ 经纬度转瓦片像素坐标是非线性的。。。。
                x_ax = (point.longitude - left_top_longitude) / col_range * 1920
                y_ax = (point.latitude - right_down_latitude) / row_range * 1920

                plt.plot(x_axes, y_axes, 'b', markersize=10)
                plt.plot(x_ax, y_ax, 'bo', )
                plt.axis('off')
                plt.savefig('tmp.png', transparent=True)
                plt.close()

                pil_image = Image.open('tmp.png')
                pil_image = pil_image.resize((1920, 1920))

                img.paste(pil_image, (0, 0), mask=pil_image)
                cnt += 1
                img.show()
                print(left_top_latitude, left_top_longitude, right_down_latitude, right_down_longitude,
                      point.latitude, point.longitude)
                break
                # TODO crop to 1920 * 1080
                img.save('output/{}.png'.format(cnt))
                print('save', cnt)


def cal_ax(points, left_top_latitude, left_top_longitude, right_down_latitude,
           right_down_longitude, col_range, row_range):
    x_axes = []
    y_axes = []
    for point in points:
        if right_down_latitude <= point.latitude <= left_top_latitude and \
                left_top_longitude <= point.longitude <= right_down_longitude:
            x_ax = (point.longitude - left_top_longitude) / col_range * 1920
            y_ax = (point.latitude - right_down_latitude) / row_range * 1920
            x_axes.append(x_ax)
            y_axes.append(y_ax)
    return x_axes, y_axes


if __name__ == '__main__':
    draw_pics()
