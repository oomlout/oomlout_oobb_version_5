"""Keep MR106 variable lookups consistent with the CSV-backed component."""

import unittest

import oobb
from components.oobb_bearing import working


class MR106BearingTests(unittest.TestCase):
    def test_shielded_dimensions_through_public_dispatch_and_variables(self):
        # EZO MR106ZZ: bore 6, OD 10, width 3; OOBB stores radii.
        for name in ("MR106", "mr106"):
            with self.subTest(name=name):
                result = oobb.oe(shape="oobb_bearing", bearing_size=name, type="p")
                while isinstance(result, list):
                    result = result[0]
                self.assertEqual((result["id"], result["od"], result["depth"]), (3, 5, 3))
                for mode in ("true", "laser"):
                    for dimension in ("id", "od", "depth"):
                        self.assertEqual(oobb.gv(f"bearing_{name}_{dimension}", mode), result[dimension])

    def test_print_allowance_and_open_width_remain_distinct(self):
        spec = working._get_bearing_spec("MR106")
        self.assertEqual(float(spec["raw_row"]["Width OPEN"]), 2.5)
        self.assertEqual(spec["depth"], 3)
        for name in ("MR106", "mr106"):
            self.assertAlmostEqual(oobb.gv(f"bearing_{name}_od", "3dpr"), 5.05)
            self.assertEqual(oobb.gv(f"bearing_{name}_id", "3dpr"), 3)
            self.assertEqual(oobb.gv(f"bearing_{name}_depth", "3dpr"), 3)


if __name__ == "__main__":
    unittest.main()
