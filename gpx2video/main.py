import cv2
import numpy as np
import gpxpy.gpx
import matplotlib.pyplot as plt
from PIL import Image

from gpx2video.map import get_tile_bound, merge_tile_pic, deg2pixel, wgs84togcj02, deg2num

gpx_file = open('data/太子湾.gpx', 'r')
gpx = gpxpy.parse(gpx_file)


level = 20


def draw_pics():
    points = []
    cnt = 0
    row_start, row_end, col_start, col_end, row, col = 0, 100000000, 0, 100000000, None, None
    img = None
    for track in gpx.tracks:
        for segment in track.segments:
            total = len(segment.points)
            for point in segment.points:
                lng, lat = wgs84togcj02(point.longitude, point.latitude)
                col, row = deg2num(lat, lng, level)
                row_range = (row_end - row_start + 1) * 256
                col_range = (col_end - col_start + 1) * 256
                pixel_x, pixel_y = deg2pixel(lat, lng, level)
                x_ax = (((col - col_start) * 256) + pixel_x) / col_range * 1920
                y_ax = (1 - ((row - row_start) * 256 + pixel_y) / row_range) * 1920

                if x_ax < 50 or x_ax > 1800 or y_ax < 50 or y_ax > 1800:
                    # 当坐标不合适时刷新背景图片
                    print('refresh background')
                    row_start, row_end, col_start, col_end, row, col = get_tile_bound(lat, lng, level)
                    row_range = (row_end - row_start + 1) * 256
                    col_range = (col_end - col_start + 1) * 256
                    pixel_x, pixel_y = deg2pixel(lat, lng, level)
                    x_ax = (((col - col_start) * 256) + pixel_x) / col_range * 1920
                    y_ax = (1 - ((row - row_start) * 256 + pixel_y) / row_range) * 1920
                    img = merge_tile_pic(level, row_start, row_end, col_start, col_end)

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
                cnt += 1
                # TODO crop to 1920 * 1080
                image.save('output/{:0>6}.png'.format(cnt))
                print('save {} of {}'.format(cnt, total))


def cal_ax(points, row_start, row_end, col_start, col_end, col_range, row_range):
    x_axes = []
    y_axes = []
    for point in points:
        x_ax = ((point['col'] - col_start) * 256 + point['pixel_x']) / col_range * 1920
        y_ax = (1 - ((point['row'] - row_start) * 256 + point['pixel_y']) / row_range) * 1920
        x_axes.append(x_ax)
        y_axes.append(y_ax)
    return x_axes, y_axes


def rotate_img(img):
    pts1 = np.float32([[0, 0], [1920, 0], [0, 1920], [1920, 1920]])  # 左上，右上，左下，右下
    pts2 = np.float32([[0, 200], [1920, 200], [0, 1720], [1920, 1720]])  # 变换后

    M = cv2.getPerspectiveTransform(pts1, pts2)
    dst = cv2.warpPerspective(img, M, (1920, 1920))

    plt.subplot(121), plt.imshow(img), plt.title('Input')
    plt.subplot(122), plt.imshow(dst), plt.title('Output')
    plt.show()
    plt.savefig('400_rotate.png')


if __name__ == '__main__':
    # out_path = '/Users/friday/work/friday/gpx-to-video/gpx2video/output'
    # img = cv2.imread('{}/400.png'.format(out_path))
    # rotate_img(img)
    # ffmpeg -start_number 001 -r 10 -i output/%6d.png -pix_fmt yuv420p test5.mp4
    draw_pics()
    # img = Image.open('together.png')
    # img = img.resize((3840, 3840))
    # img = img.crop((1920, 0, 3840, 1920))
    # img.show()