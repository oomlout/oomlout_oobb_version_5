import copy
import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

# BOSL2 lives in the github_belfry_bosl2_gear submodule
_BOSL2_PATH = os.path.join(
    _PROJECT_ROOT, "components", "github_belfry_bosl2_gear", "BOSL2"
)

d = {}


def describe():
    global d
    d = {}
    d["name"] = "oobb_gear_spur"
    d["name_long"] = "OOBB Motion: Spur Gear"
    d["description"] = (
        "Metric involute spur gear via BOSL2. "
        "Pressure angle fixed at 20°. Optional chamfer bevel on top and bottom faces."
    )
    d["category"] = "OOBB Motion"
    d["shape_aliases"] = ["oobb_gear_spur", "spur_gear"]
    d["returns"] = "List of geometry component dicts."
    v = []
    v.append({"name": "pos",        "description": "3-element [x,y,z] position.",                            "type": "list",   "default": "[0,0,0]"})
    v.append({"name": "rot",        "description": "Rotation [rx,ry,rz] in degrees.",                        "type": "list",   "default": "[0,0,0]"})
    v.append({"name": "type",       "description": "Geometry type: positive or negative.",                    "type": "string", "default": '"positive"'})
    v.append({"name": "teeth",      "description": "Number of gear teeth (integer >= 4).",                    "type": "number", "default": 16})
    v.append({"name": "mod",        "description": "Gear module (metric pitch). Pitch diameter = mod*teeth.", "type": "number", "default": 2})
    v.append({"name": "depth",      "description": "Gear face thickness in mm.",                              "type": "number", "default": 8})
    v.append({"name": "shaft_diam", "description": "Centre shaft bore diameter in mm (0 = no bore).",        "type": "number", "default": 0})
    v.append({"name": "backlash",   "description": "Backlash in mm.",                                        "type": "number", "default": 0})
    v.append({"name": "gear_bevel", "description": "Chamfer depth (mm) on top and bottom outer edges. 0 = flat faces.", "type": "number", "default": 0})
    d["variables"] = v
    return d


def define():
    global d
    if not isinstance(d, dict) or not d:
        describe()
    defined = {}
    defined.update(d)
    return defined


def _build_wrapper_source():
    std_path   = os.path.join(_BOSL2_PATH, "std.scad").replace("\\", "/")
    gears_path = os.path.join(_BOSL2_PATH, "gears.scad").replace("\\", "/")

    return f'''include <{std_path}>
include <{gears_path}>

module oobb_gear_spur_raw(
    teeth=16,
    gear_mod=2,
    thickness=8,
    shaft_diam=0,
    backlash=0,
    gear_bevel=0
) {{
    cp     = gear_mod * PI;
    tip_r  = outer_radius(circ_pitch=cp, teeth=teeth);
    extra  = tip_r + gear_bevel + 2;
    half_t = thickness / 2;

    difference() {{
        spur_gear(
            mod=gear_mod,
            teeth=teeth,
            thickness=thickness,
            shaft_diam=shaft_diam,
            pressure_angle=20,
            backlash=backlash,
            helical=0,
            herringbone=false,
            gear_spin=0,
            anchor=CENTER
        );
        if (gear_bevel > 0) {{
            // top face chamfer — ring with conical inner edge
            translate([0, 0, half_t - gear_bevel])
            difference() {{
                cylinder(r=extra, h=gear_bevel + 0.01);
                cylinder(r1=tip_r, r2=tip_r - gear_bevel, h=gear_bevel + 0.01);
            }}
            // bottom face chamfer — mirror of top
            translate([0, 0, -half_t - 0.01])
            difference() {{
                cylinder(r=extra, h=gear_bevel + 0.01);
                cylinder(r1=tip_r - gear_bevel, r2=tip_r, h=gear_bevel + 0.01);
            }}
        }}
    }}
}}
'''


def action(**kwargs):
    if not os.path.isdir(_BOSL2_PATH):
        raise FileNotFoundError(
            f"BOSL2 submodule not found at {_BOSL2_PATH}. "
            "Run: git submodule update --init components/github_belfry_bosl2_gear/BOSL2"
        )

    params     = copy.deepcopy(kwargs)
    pos        = copy.deepcopy(params.get("pos", [0, 0, 0]))
    rot        = copy.deepcopy(params.get("rot", [0, 0, 0]))
    inclusion  = params.get("inclusion", params.get("mode", "all"))
    if isinstance(inclusion, list):
        inclusion = "all" if inclusion == ["laser", "3dpr", "true"] else ",".join(str(i) for i in inclusion)

    teeth      = params.get("teeth", 16)
    mod        = params.get("mod", 2)
    thickness  = params.get("depth", params.get("thickness", 8))
    shaft_diam = params.get("shaft_diam", 0)
    backlash   = params.get("backlash", 0)
    gear_bevel = params.get("gear_bevel", 1)

    module_kwargs = {
        "teeth":      teeth,
        "gear_mod":   mod,
        "thickness":  thickness,
        "shaft_diam": shaft_diam,
        "backlash":   backlash,
        "gear_bevel": gear_bevel,
    }

    return {
        "type":          params.get("type", "positive"),
        "shape":         "raw_scad",
        "source":        _build_wrapper_source(),
        "module":        "oobb_gear_spur_raw",
        "module_kwargs": module_kwargs,
        "include_mode":  True,
        "pos":           pos,
        "rot":           rot,
        "color":         params.get("color", ""),
        "inclusion":     inclusion,
        "m":             params.get("m", ""),
    }


def test():
    import copy
    import os
    import opsc

    folder   = os.path.dirname(os.path.abspath(__file__))
    test_dir = os.path.join(folder, "test")
    os.makedirs(test_dir, exist_ok=True)

    samples = [
        {
            "filename":    "test_1",
            "preview_rot": [65, 0, 25],
            "kwargs": {
                "pos":       [0, 0, 0],
                "type":      "positive",
                "teeth":     16,
                "mod":       2,
                "depth":     8,
                "shaft_diam": 5,
                "gear_bevel": 0,
            },
        },
        {
            "filename":    "test_2",
            "preview_rot": [65, 0, 25],
            "kwargs": {
                "pos":       [0, 0, 0],
                "type":      "positive",
                "teeth":     24,
                "mod":       2,
                "depth":     10,
                "shaft_diam": 6,
                "gear_bevel": 1.5,
            },
        },
    ]

    generated_files = []

    for sample in samples:
        kwargs   = copy.deepcopy(sample["kwargs"])
        result   = action(**kwargs)
        components = result if isinstance(result, list) else [result]

        sample_dir = os.path.join(test_dir, sample["filename"])
        os.makedirs(sample_dir, exist_ok=True)
        scad_path = os.path.join(sample_dir, "working.scad")
        png_path  = os.path.join(sample_dir, "image.png")

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
