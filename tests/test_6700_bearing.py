"""6700 support in both CSV-backed components and legacy OOBB variables."""
import unittest
import oobb


class Bearing6700Tests(unittest.TestCase):
    def test_dimensions(self):
        result = oobb.oe(shape="oobb_bearing", bearing_size="6700", type="p")
        while isinstance(result,list):
            result=result[0]
        self.assertEqual((result["id"],result["od"],result["depth"]),(5,7.5,4))
        for mode in ("true","laser"):
            for key,value in (("id",5),("od",7.5),("depth",4)):
                self.assertEqual(oobb.gv("bearing_6700_"+key,mode),value)


if __name__=="__main__":
    unittest.main()
