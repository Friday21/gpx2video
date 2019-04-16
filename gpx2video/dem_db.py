from raster2xyz.raster2xyz import Raster2xyz

from mongoengine import connect, Document, IntField, StringField, PointField

connect(db='gpx', host='127.0.0.1', port=27000)


class Dem(Document):
    name = StringField(required=True)
    height = IntField(required=True)
    location = PointField(required=True)

    meta = {'collection': 'dems',
            'ordering': ['location'],
            'indexes': [
                {'fields': ['location']},
            ]}

    @classmethod
    def get_dems_from_lat_lon(cls, rec):
        """
        :param rec:[[lng1, lat1], [lng2, lat2]]
        :return:
        """
        return cls.objects.all()
        dems = cls.objects.filter(location__geo_within_box=rec).order_by('location').all()
        return dems


def create_dem_db_from_tif():
    input_raster = 'DEM30.tif'
    rtxyz = Raster2xyz()
    x, y, z = rtxyz.translate(input_raster, '')
    cnt = 0
    cnt1 = 1
    length = len(x)
    dems = []
    for i in range(length):
        long, lat, height = x[i], y[i], z[i]
        dems.append(Dem(name='杭州dem', location=[long, lat], height=height))
        cnt += 1
        if cnt == 50000:
            Dem.objects.insert(dems)
            dems = []
            print('save {}'.format(50000 * cnt1))
            cnt1 += 1
            cnt = 0


if __name__ == '__main__':
    create_dem_db_from_tif()