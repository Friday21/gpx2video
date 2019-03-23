import os
import math
import time

from PIL import Image

from gpx2video.config import map_path


tile_size = 256  # 瓦片大小256*256


def get_tile_bound(lat, lon):
    """获取瓦片的编号范围"""
    return 0, 0, 0, 0


def merge_tile_pic(level, row_start, row_end, col_start, col_end):
    """
    :param level: 地图等级
    :param row_start: 瓦片行号起点
    :param row_end: 瓦片行号终点
    :param col_start: 瓦片列号起点
    :param col_end: 瓦片列号终点
    :return: 合成好的图片
    """
    result_filepath = '{}.png'.format(123)

    tile_dir = os.path.join(map_path, str(level))

    # 拼接瓦片，生成底图
    color = (255, 255, 255, 0)

    width = int((col_end - col_start + 1) * tile_size)
    height = int((row_end - row_start + 1) * tile_size)

    out = Image.new('RGBA', (width, height), color)
    out_satellite = Image.new('RGBA', (width, height), color)
    out_overlay = Image.new('RGBA', (width, height), color)
    imx = 0
    for row in range(row_start, row_end + 1):
        imy = 0
        for col in range(col_start, col_end + 1):
            tile_file = os.path.join(tile_dir, str(col), '{}.jpg'.format(row))
            if os.path.exists(tile_file):
                satellite = Image.open(tile_file)
                overlay_file = tile_file.replace('satellite', 'overlay').replace('jpg', 'png')
                out_satellite.paste(satellite, (imy, imx))
                if os.path.exists(overlay_file):
                    overlay = Image.open(overlay_file)
                    out_overlay.paste(satellite, (imy, imx), overlay)
            imy += tile_size
        imx += tile_size
    out_satellite.paste(out_overlay, (0, 0), out_overlay)
    out_satellite.save(result_filepath)


def num2deg(col, row, zoom):
    """

    :param col: 瓦片列数col
    :param row: 瓦片行数row
    :param zoom: 瓦片缩放等级
    :return: lat_deg: 纬度， lon_deg 经度 返回的是瓦片左上角的的经纬度
    """
    n = 2.0 ** zoom
    lon_deg = col / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * row / n)))
    lat_deg = math.degrees(lat_rad)
    return lat_deg, lon_deg


def deg2num(lat_deg, lon_deg, zoom):
    """返回左上角经纬度为lat_deg, lon_deg的瓦片行列号"""
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return xtile+1, ytile+1  # col, row


if __name__ == '__main__':
    pass