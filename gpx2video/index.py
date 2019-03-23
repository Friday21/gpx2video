import os

from gpx2video.config import map_path
from gpx2video.map import num2deg


def read_data(file_path):
    with open(file_path, encoding='iso-8859-1') as f:
        lines = f.readlines()
        points = []
        for line in lines[10:14]:
            point = line.split(':')[1].split(',')
            points.append([float(point[0]), float(point[1].replace('\n', ''))])
        return points


def create_index_by_txt():
    """
    index: {'zoom': {   row: 10, col:6,
                        left_top_latitude: 20.21,  # 纬度， row
                        left_top_longitude: 29.22,  # 精度， col
                        right_down_latitude: 20.21,  # 纬度， row
                        right_down_longitude: 29.22,  # 精度， col
                        row_step: 0.1,
                        col_step: 0.2,
                        }}
    :return:
    """
    index = {}
    for i in range(10, 19):
        zoom_dir = os.path.join(map_path, 'L{}'.format(i))
        dirs = os.listdir(zoom_dir)
        dirs = [dir for dir in dirs if dir.startswith('R')]
        row = len(dirs)
        dirs.sort()

        first_dir_path = os.path.join(zoom_dir, dirs[0])
        filenames = os.listdir(first_dir_path)
        filenames = [filename for filename in filenames if filename.startswith('C') and filename.endswith('.txt')]
        col = len(filenames)
        filenames.sort()
        for file in filenames:
            if file.endswith('.txt'):
                file_path = os.path.join(first_dir_path, file)
                points = read_data(file_path)
                left_top_latitude, left_top_longitude = points[1]
                row_step = points[1][1] - points[0][1]
                col_step = points[2][0] - points[1][0]
                break

        last_dir_path = os.path.join(zoom_dir, dirs[-1])
        filenames = os.listdir(last_dir_path)
        filenames = [filename for filename in filenames if filename.startswith('C')]
        filenames.sort(reverse=True)
        for file in filenames:
            if file.endswith('.txt'):
                file_path = os.path.join(last_dir_path, file)
                points = read_data(file_path)
                right_down_latitude, right_down_longitude = points[3]
                break
        index[i] = {'row': row, 'col': col,
                    'left_top_latitude': left_top_latitude,
                    'left_top_longitude': left_top_longitude,
                    'right_down_latitude': right_down_latitude,
                    'right_down_longitude': right_down_longitude,
                    'row_step': row_step,
                    'col_step': col_step,
                    }

    print(index)


def create_index_by_tile():
    """根据地图目录下瓦片的行号和列号以及缩放层级来计算经纬度"""
    indexes = {}
    for i in range(10, 19):
        zoom_dir = os.path.join(map_path, 'L{}'.format(i))
        dirs = os.listdir(zoom_dir)
        dirs = [dir for dir in dirs if dir.startswith('R')]
        row = len(dirs)
        dirs.sort()

        first_dir_path = os.path.join(zoom_dir, dirs[0])
        first_filenames = os.listdir(first_dir_path)
        first_filenames = [filename for filename in first_filenames if filename.endswith('.jpg')]
        last_filenames = os.listdir(os.path.join(zoom_dir, dirs[-1]))
        last_filenames = [filename for filename in last_filenames if filename.endswith('.jpg')]
        last_filenames.sort()
        col = len(first_filenames)
        first_filenames.sort()

        start_row_num = int(dirs[0].replace('R', ''))
        start_col_num = int(first_filenames[0].replace('C', '').replace('.jpg', ''))

        end_row_num = int(dirs[-1].replace('R', ''))
        end_col_num = int(last_filenames[-1].replace('C', '').replace('.jpg', ''))

        left_top_latitude, left_top_longitude = num2deg(start_col_num, start_row_num, i)
        right_top_latitude, right_top_longitude = num2deg(end_col_num, end_row_num, i)

        row_step = (left_top_latitude - right_top_latitude) / (row-1)
        col_step = (right_top_longitude - left_top_longitude) / (col-1)

        right_down_latitude = right_top_latitude - row_step
        right_down_longitude = right_top_longitude + col_step

        indexes[i] = {'row': row, 'col': col,
                      'left_top_latitude': left_top_latitude,
                      'left_top_longitude': left_top_longitude,
                      'right_down_latitude': right_down_latitude,
                      'right_down_longitude': right_down_longitude,
                      'row_step': row_step,  # 非线性
                      'col_step': col_step,  # 非线性
                      'start_row_num': start_row_num,
                      'start_col_num': start_col_num,
                      'end_row_num': end_row_num,
                      'end_col_num': end_col_num
                      }
    print(indexes)
