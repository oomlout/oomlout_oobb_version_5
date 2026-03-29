import unittest
from pathlib import Path

import oobb
import oobb_base

from oobb_arch.catalog.migration_status import get_all_legacy_object_functions, get_migration_status
from oobb_arch.catalog.object_discovery import discover_objects


ROOT = Path(__file__).resolve().parents[1]
OBJECTS_ROOT = ROOT / "part_calls" / "objects"
CORE_MODULES = {
    "oobb_get_items_oobb",
    "oobb_get_items_oobb_old",
    "oobb_get_items_oobb_wire",
    "oobb_get_items_oobb_holder",
    "oobb_get_items_oobb_other",
    "oobb_get_items_oobb_bearing_plate",
}


class OobbCoreObjectMigrationTests(unittest.TestCase):
    def _core_legacy_objects(self):
        return [item for item in get_all_legacy_object_functions() if item["source_module"] in CORE_MODULES]

    def test_all_oobb_core_functions_have_folders(self):
        for item in self._core_legacy_objects():
            folder = OBJECTS_ROOT / f"oobb_object_{item['type_name']}" / "working.py"
            self.assertTrue(folder.exists(), msg=f"Missing folder for {item['function_name']}")

    def test_all_migrated_core_objects_are_discoverable(self):
        discovered = discover_objects(objects_root=OBJECTS_ROOT)
        for item in self._core_legacy_objects():
            self.assertIn(f"oobb_object_{item['type_name']}", discovered)

    def test_migration_status_shows_core_complete(self):
        status = get_migration_status(objects_root=OBJECTS_ROOT)
        migrated = set(status["objects"]["migrated"])
        for item in self._core_legacy_objects():
            self.assertIn(item["type_name"], migrated)

    def test_key_objects_have_rich_metadata(self):
        discovered = discover_objects(objects_root=OBJECTS_ROOT)
        for name in ["oobb_object_circle", "oobb_object_plate", "oobb_object_gear"]:
            self.assertIn(name, discovered)
            metadata = discovered[name].metadata
            self.assertTrue(metadata.get("description"))
            self.assertNotIn("Auto-generated scaffold", metadata.get("description", ""))
            self.assertGreaterEqual(len(metadata.get("variables", [])), 2)

    def test_dispatching_still_works(self):
        oobb_base._OBJECT_LOOKUP = None
        result = oobb_base.get_thing_from_dict(
            {"type": "plate", "width": 3, "height": 3, "thickness": 3, "size": "oobb"}
        )
        self.assertIsInstance(result, dict)
        self.assertIn("components", result)


if __name__ == "__main__":
    unittest.main()
