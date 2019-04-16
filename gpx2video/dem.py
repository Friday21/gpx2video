import os

import numpy as np
from matplotlib import pyplot as plt, cm
from matplotlib.mlab import griddata
from mpl_toolkits.mplot3d import Axes3D
from matplotlib._png import read_png
from pylab import *
from matplotlib.cbook import get_sample_data
from raster2xyz.raster2xyz import Raster2xyz

import scipy as sp
import scipy.interpolate

from PIL import Image
from osgeo import gdal
from mayavi import mlab


path = os.path.dirname(os.path.abspath(__file__))
img_path = os.path.join(path, 'beauty.png')


def plot_surface():
    x, y, z = extract_xyz_from_dem()
    xi = np.linspace(min(x), max(x))
    yi = np.linspace(min(y), max(y))
    X, Y = np.meshgrid(xi, yi)
    # interpolation
    Z = griddata(x, y, z, xi, yi)
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.jet, linewidth=1, antialiased=True)
    plt.show()


def extract_xyz_from_dem():
    input_raster = 'DEM30.tif'
    output = 'hz.csv'
    rtxyz = Raster2xyz()
    x, y, z = rtxyz.translate(input_raster, output)
    return x, y, z


def plot_3d():
    x, y, z = extract_xyz_from_dem()
    # 2D grid construction
    spline = sp.interpolate.Rbf(x, y, z, function='thin-plate')
    xi = np.linspace(min(x), max(x))
    yi = np.linspace(min(y), max(y))
    X, Y = np.meshgrid(xi, yi)
    # interpolation
    Z = spline(X, Y)


def plot_terrain():
    ds = gdal.Open('DEM30.tif')
    # 对data做处理， 使得经纬度和卫星图像精确映射
    # resize 图片大小一样， 经纬度范围一样（精确度待定）
    # 存数据库？
    # x, y之间的比例？
    data = ds.ReadAsArray(xoff=0, yoff=0, xsize=2000, ysize=2000)
    # print(data)
    x, y, z = extract_xyz_from_dem()
    # print(z)
    print(len(data))
    print(len(data[0]))
    print(len(x), len(y), len(z))
    import pdb
    pdb.set_trace()
    mlab.figure(size=(1920, 1920), bgcolor=(0.16, 0.28, 0.46))
    mlab.surf(data, warp_scale=0.2)
    # f = mlab.gcf()
    # camera = f.scene.camera
    # camera.yaw(45)
    mlab.show()


if __name__ == '__main__':
    # plot_surface()
    plot_terrain()