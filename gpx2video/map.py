import os
import math

from PIL import Image

from gpx2video.config import map_path


tile_size = 256  # 瓦片大小256*256
x_pi = 3.14159265358979324 * 3000.0 / 180.0
pi = 3.1415926535897932384626  # π
a = 6378245.0  # 长半轴
ee = 0.00669342162296594323  # 扁率


def get_tile_bound(lat, lon, level):
    """获取瓦片的编号范围"""
    col, row = deg2num(lat, lon, level)  # 中心
    row_start = row - 6
    row_end = row + 5
    col_start = col - 6
    col_end = col + 5
    return row_start, row_end, col_start, col_end, row, col


def merge_tile_pic(level, row_start, row_end, col_start, col_end, filename=None):
    """
    :param level: 地图等级
    :param row_start: 瓦片行号起点
    :param row_end: 瓦片行号终点
    :param col_start: 瓦片列号起点
    :param col_end: 瓦片列号终点
    :return: 合成好的图片
    """

    tile_dir = os.path.join(map_path, str(level))

    # 拼接瓦片，生成底图
    color = (255, 255, 255, 0)

    width = int((col_end - col_start + 1) * tile_size)
    height = int((row_end - row_start + 1) * tile_size)

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
    # crop
    # new_height = width * 9/16
    # height_diff = height - new_height if height > new_height else height
    # out_satellite = out_satellite.crop((0, height_diff//2, width, height - height_diff//2))
    out_satellite = out_satellite.resize((1920, 1920))  # 1080p
    # out_satellite.show()
    return out_satellite


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
    return xtile, ytile  # col, row


def deg2pixel(lat_deg, lon_deg, zoom):
    n = 2.0 ** zoom
    lat_ang = lat_deg * math.pi / 180
    pixel_x = int((lon_deg + 180.0) / 360.0 * n * 256 % 256)
    pixel_y = int((1 - math.log(math.tan(lat_ang) + 1/math.cos(lat_ang))/(2*math.pi)) * n * 256 % 256)
    return pixel_x, pixel_y


def deg2pic(lat_deg, lon_deg, zoom):
    col, row = deg2num(lat_deg, lon_deg, zoom)
    path = os.path.join(map_path, str(zoom), str(col), '{}.jpg'.format(row))
    image = Image.open(path)
    image.show()


def wgs84togcj02(lng, lat):
    """
    WGS84转GCJ02(火星坐标系)
    :param lng:WGS84坐标系的经度
    :param lat:WGS84坐标系的纬度
    :return:
    """
    if out_of_china(lng, lat):  # 判断是否在国内
        return lng, lat
    dlat = transformlat(lng - 105.0, lat - 35.0)
    dlng = transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return [mglng, mglat]


def gcj02towgs84(lng, lat):
    """
    GCJ02(火星坐标系)转GPS84
    :param lng:火星坐标系的经度
    :param lat:火星坐标系纬度
    :return:
    """
    if out_of_china(lng, lat):
        return lng, lat
    dlat = transformlat(lng - 105.0, lat - 35.0)
    dlng = transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return [lng * 2 - mglng, lat * 2 - mglat]


def transformlat(lng, lat):
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + \
        0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * pi) + 40.0 *
            math.sin(lat / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * pi) + 320 *
            math.sin(lat * pi / 30.0)) * 2.0 / 3.0
    return ret


def transformlng(lng, lat):
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + \
        0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * pi) + 40.0 *
            math.sin(lng / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * pi) + 300.0 *
            math.sin(lng / 30.0 * pi)) * 2.0 / 3.0
    return ret


def out_of_china(lng, lat):
    """
    判断是否在国内，不在国内不做偏移
    :param lng:
    :param lat:
    :return:
    """
    if lng < 72.004 or lng > 137.8347:
        return True
    if lat < 0.8293 or lat > 55.8271:
        return True
    return False


if __name__ == '__main__':
    row_start, row_end, col_start, col_end = get_tile_bound(30.191082174611765, 120.08268313531809, 16)
    im = merge_tile_pic(16, row_start, row_end, col_start, col_end)
    im.show()
