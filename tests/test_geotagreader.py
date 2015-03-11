from models.photo import GeoTagReader
from models.photo.utils import get_photo_fname

P_UPLOADED = 1

class TestGeoTagReader:
        
    def test_geotag_reader(self):
        fname = get_photo_fname(P_UPLOADED, 'jpg')
        gtr = GeoTagReader(fname)
        # whatever.
        assert (gtr.get_date_created() is not None)
        assert (gtr.get_lat() is not None)
        assert (gtr.get_lon() is not None)
