""" extracts lat, lon, date_created from geotagged JPG image """

import exifread
from datetime import datetime
from fractions import Fraction

EXIF_FMT = "%Y:%m:%d %H:%M:%S"

def decimal_degrees(dms):
    return dms[0] + dms[1]/60. + dms[2]/3600.

class GeoTagReader:
    
    def __init__(self, path_name):
        f = open(path_name, 'rb')
        self.tags = exifread.process_file(f)
        f.close()
        
    def get_dms(self, key):
        dms = self.tags[key]
        vals = dms.values # array of instance objects
        assert (len(vals) == 3)
        dms = []
        for val in vals:
            f = Fraction(str(val))  # convert val to a fraction
            dms.append(f.numerator) # save the numerator
        return decimal_degrees(dms)

    def get_lat(self):
        return self.get_dms('GPS GPSLatitude')
        
    def get_lon(self):
        return self.get_dms('GPS GPSLongitude')

    def get_date_created(self):
        date_str = str(self.tags['EXIF DateTimeOriginal']) 
        return datetime.strptime(date_str, EXIF_FMT)
