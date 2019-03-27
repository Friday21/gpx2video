import gpxpy.gpx


gpx_file = open('data/太子湾.gpx', 'r')
gpx = gpxpy.parse(gpx_file)


for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            print('Point at ({0},{1}, {2}), time:{3}'.format(
                point.latitude, point.longitude, point.elevation, point.time))
