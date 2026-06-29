import copy
import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

_COMPONENT_ROOT = os.path.dirname(os.path.abspath(__file__))
_BOSL2_PATH = os.path.join(_COMPONENT_ROOT, "BOSL2")

d = {}


def describe():
    global d
    d = {}
    d["name"] = "github_belfry_bosl2_gear"
    d["name_long"] = "GitHub BelfrySCAD BOSL2: Spur Gear"
    d["description"] = (
        "BOSL2 spur_gear() wrapper — metric involute spur gears with optional helical "
        "or herringbone teeth and a centre shaft bore."
    )
    d["category"] = "External Library Wrappers"
    d["shape_aliases"] = ["github_belfry_bosl2_gear", "bosl2_spur_gear", "bosl2_gear"]
    d["returns"] = "Raw SCAD geometry component dict."
    d["source"] = "https://github.com/BelfrySCAD/BOSL2"
    d["source_file"] = "https://github.com/BelfrySCAD/BOSL2/wiki/gears.scad"
    v = []
    v.append({"name": "pos",           "description": "3-element [x,y,z] position.",                           "type": "list",   "default": "[0,0,0]"})
    v.append({"name": "rot",           "description": "Rotation [rx,ry,rz] in degrees.",                       "type": "list",   "default": "[0,0,0]"})
    v.append({"name": "type",          "description": "Geometry type: positive or negative.",                   "type": "string", "default": '"positive"'})
    v.append({"name": "teeth",         "description": "Number of gear teeth (integer >= 4).",                   "type": "number", "default": 16})
    v.append({"name": "mod",           "description": "Gear module (metric pitch). Pitch diameter = mod*teeth.", "type": "number", "default": 2})
    v.append({"name": "thickness",     "description": "Gear face thickness in mm (alias: depth).",              "type": "number", "default": 8})
    v.append({"name": "depth",         "description": "Alias for thickness.",                                   "type": "number", "default": 8})
    v.append({"name": "shaft_diam",    "description": "Centre shaft bore diameter in mm (0 = no bore).",       "type": "number", "default": 0})
    v.append({"name": "pressure_angle","description": "Tooth pressure angle in degrees.",                       "type": "number", "default": 20})
    v.append({"name": "backlash",      "description": "Backlash in mm.",                                        "type": "number", "default": 0})
    v.append({"name": "helical",       "description": "Helical angle in degrees (0 = spur gear).",              "type": "number", "default": 0})
    v.append({"name": "herringbone",   "description": "If true, produce a herringbone (double-helical) gear.",  "type": "bool",   "default": False})
    v.append({"name": "gear_spin",     "description": "Rotate the gear teeth pattern by this many degrees.",    "type": "number", "default": 0})
    v.append({"name": "mode",          "description": 'Render modes: "laser", "3dpr", "true".',                 "type": "list",   "default": '["laser","3dpr","true"]'})
    d["variables"] = v
    return d


def define():
    global d
    if not isinstance(d, dict) or not d:
        describe()
    defined = {}
    defined.update(d)
    return defined


def _bosl2_root():
    return _BOSL2_PATH


def _build_wrapper_source():
    std_path = os.path.join(_BOSL2_PATH, "std.scad").replace("\\", "/")
    gears_path = os.path.join(_BOSL2_PATH, "gears.scad").replace("\\", "/")
    return f'''include <{std_path}>
include <{gears_path}>

module github_belfry_bosl2_gear_raw(
    teeth=16,
    mod=2,
    thickness=8,
    shaft_diam=0,
    pressure_angle=20,
    backlash=0,
    helical=0,
    herringbone=false,
    gear_spin=0
) {{
    spur_gear(
        mod=mod,
        teeth=teeth,
        thickness=thickness,
        shaft_diam=shaft_diam,
        pressure_angle=pressure_angle,
        backlash=backlash,
        helical=helical,
        herringbone=herringbone,
        gear_spin=gear_spin,
        anchor=CENTER
    );
}}
'''


def action(**kwargs):
    bosl2_root = _bosl2_root()
    if not os.path.isdir(bosl2_root):
        raise FileNotFoundError(
            f"BOSL2 submodule not found at {bosl2_root}. "
            "Run: git submodule update --init components/github_belfry_bosl2_gear/BOSL2"
        )

    params = copy.deepcopy(kwargs)
    pos = copy.deepcopy(params.get("pos", [0, 0, 0]))
    rot = copy.deepcopy(params.get("rot", [0, 0, 0]))
    inclusion = params.get("inclusion", params.get("mode", "all"))
    if isinstance(inclusion, list):
        inclusion = "all" if inclusion == ["laser", "3dpr", "true"] else ",".join(str(i) for i in inclusion)

    thickness = params.get("thickness", params.get("depth", 8))

    module_kwargs = {
        "teeth":          params.get("teeth", 16),
        "mod":            params.get("mod", 2),
        "thickness":      thickness,
        "shaft_diam":     params.get("shaft_diam", 0),
        "pressure_angle": params.get("pressure_angle", 20),
        "backlash":       params.get("backlash", 0),
        "helical":        params.get("helical", 0),
        "herringbone":    params.get("herringbone", False),
        "gear_spin":      params.get("gear_spin", 0),
    }

    return {
        "type":         params.get("type", "positive"),
        "shape":        "raw_scad",
        "source":       _build_wrapper_source(),
        "module":       "github_belfry_bosl2_gear_raw",
        "module_kwargs": module_kwargs,
        "include_mode": True,
        "pos":          pos,
        "rot":          rot,
        "color":        params.get("color", ""),
        "inclusion":    inclusion,
        "m":            params.get("m", ""),
    }


def test():
    import copy
    import os
    import opsc

    folder = os.path.dirname(os.path.abspath(__file__))
    test_dir = os.path.join(folder, "test")
    os.makedirs(test_dir, exist_ok=True)

    samples = [
        {
            "filename": "test_1",
            "preview_rot": [65, 0, 25],
            "kwargs": {
                "pos": [0, 0, 0],
                "type": "positive",
                "teeth": 16,
                "mod": 2,
                "thickness": 8,
                "shaft_diam": 5,
                "mode": "true",
            },
        },
        {
            "filename": "test_2",
            "preview_rot": [65, 0, 25],
            "kwargs": {
                "pos": [0, 0, 0],
                "type": "positive",
                "teeth": 24,
                "mod": 2,
                "thickness": 10,
                "shaft_diam": 6,
                "helical": 20,
                "herringbone": True,
                "mode": "true",
            },
        },
    ]

    generated_files = []

    for sample in samples:
        kwargs = copy.deepcopy(sample["kwargs"])
        result = action(**kwargs)
        if isinstance(result, dict) and "components" in result:
            components = copy.deepcopy(result["components"])
        elif isinstance(result, list):
            components = result
        else:
            components = [result]

        sample_dir = os.path.join(test_dir, sample["filename"])
        os.makedirs(sample_dir, exist_ok=True)
        scad_path = os.path.join(sample_dir, "working.scad")
        png_path = os.path.join(sample_dir, "image.png")

        opsc.opsc_make_object(
            scad_path,
            components,
            mode="true",
            save_type="none",
            overwrite=True,
            render=True,
        )
        opsc.save_preview_images(scad_path, sample_dir)
        generated_files.append(png_path)

    return generated_files
