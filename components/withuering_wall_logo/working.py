import copy
import os
import shutil
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

_COMPONENT_ROOT = os.path.dirname(os.path.abspath(__file__))
_DEFAULT_LOGO = r"C:\od\OneDrive\docs\megacity_keyring\source_file\logo_1\image.svg"
_SCAD_LOGO = os.path.join(_COMPONENT_ROOT, "image_scad.svg")
_LOGO_SIZE_RADIUS_PERCENT = 1.4
_EPSILON = 0.01

d = {}


def _variable(name, description, value_type, default):
    return {"name": name, "description": description, "type": value_type, "default": default}


def describe():
    global d
    d = {}
    d["name"] = "withuering_wall_logo"
    d["name_long"] = "Withuering Wall Logo"
    d["description"] = (
        "Circular wall logo disk using the W squared SVG. The logo is subtracted from "
        "the top face; when depth_engraving is omitted, the logo cuts fully through."
    )
    d["category"] = "OOBB Custom Components"
    d["shape_aliases"] = ["withuering_wall_logo", "withering_wall_logo"]
    d["returns"] = "List of geometry component dicts."
    v = []
    v.append(_variable("radius", "Outer circle radius in mm.", "number", 20))
    v.append(_variable("depth", "Disk depth in mm.", "number", 3))
    v.append(_variable("depth_engraving", "Logo cut depth in mm. Defaults to depth for a full hollow cut.", "number", "(same as depth)"))
    v.append(_variable("logo_size_radius_percent", "Logo size as a multiple of the outer radius.", "number", _LOGO_SIZE_RADIUS_PERCENT))
    v.append(_variable("pos", "3-element [x,y,z] position.", "list", "[0,0,0]"))
    v.append(_variable("rot", "Rotation [rx,ry,rz] in degrees.", "list", "[0,0,0]"))
    v.append(_variable("zz", "Z anchor point: bottom, center/middle, top.", "string", '"bottom"'))
    d["variables"] = v
    return d


def define():
    global d
    if not isinstance(d, dict) or not d:
        describe()
    defined = {}
    defined.update(d)
    return defined


def _as_float(value, default):
    if value in ("", None):
        return default
    return float(value)


def _anchored_pos(params, depth):
    pos = copy.deepcopy(params.get("pos", [params.get("x", 0), params.get("y", 0), params.get("z", 0)]))
    zz = params.get("zz", "bottom")
    if zz in ("center", "middle"):
        pos[2] -= depth / 2
    elif zz == "top":
        pos[2] -= depth
    return pos


def _resolve_logo_file(path):
    path = path or _SCAD_LOGO
    path = os.path.expanduser(str(path))
    if os.path.isabs(path):
        return path
    return os.path.abspath(path)


def _copy_logo_file(source_path, cache_dir):
    if not cache_dir:
        return source_path

    os.makedirs(cache_dir, exist_ok=True)
    destination_name = "withuering_wall_logo.svg"
    destination_path = os.path.join(cache_dir, destination_name)
    if os.path.abspath(source_path) != os.path.abspath(destination_path):
        shutil.copyfile(source_path, destination_path)
    return destination_name


def action(**kwargs):
    params = copy.deepcopy(kwargs)
    depth = _as_float(params.get("depth", params.get("h", 3)), 3)
    object_type = params.get("type", "positive")
    rot = params.get("rot", [params.get("rot_x", 0), params.get("rot_y", 0), params.get("rot_z", 0)])

    logo = {
        "type": "positive",
        "shape": "withuering_wall_logo",
        "radius": _as_float(params.get("radius", params.get("r", 20)), 20),
        "depth": depth,
        "depth_engraving": _as_float(params.get("depth_engraving", None), depth),
        "logo_size_radius_percent": _as_float(params.get("logo_size_radius_percent", None), _LOGO_SIZE_RADIUS_PERCENT),
        "file": params.get("file", params.get("image", _SCAD_LOGO)),
        "pos": [0, 0, 0],
    }

    rotation = {
        "type": "rotation",
        "typetype": object_type,
        "pos": _anchored_pos(params, depth),
        "rot": rot,
        "objects": [logo],
    }
    if params.get("m", "") != "":
        rotation["m"] = params["m"]
    if params.get("inclusion", "") != "":
        rotation["inclusion"] = params["inclusion"]
    return [rotation]


def render(params):
    from solid2 import cylinder, difference, import_, linear_extrude, scale, translate

    radius = _as_float(params.get("radius", params.get("r", 20)), 20)
    depth = _as_float(params.get("depth", params.get("h", 3)), 3)
    depth_engraving = _as_float(params.get("depth_engraving", None), depth)
    depth_engraving = max(0, min(depth_engraving, depth))
    logo_file = _resolve_logo_file(params.get("file", params.get("image", _SCAD_LOGO)))
    if not os.path.isfile(logo_file):
        raise FileNotFoundError(f"withuering_wall_logo SVG not found: {logo_file}")

    logo_size_radius_percent = _as_float(params.get("logo_size_radius_percent", None), _LOGO_SIZE_RADIUS_PERCENT)
    logo_size = radius * logo_size_radius_percent
    logo_import_file = _copy_logo_file(logo_file, params.get("cache_dir"))

    disk = cylinder(r=radius, h=depth)
    logo_2d = scale([logo_size, logo_size, 1])(
        translate([-0.5, 0, 0])(
            import_(file=logo_import_file)
        )
    )

    if depth_engraving >= depth:
        cut_z = -_EPSILON
        cut_depth = depth + (_EPSILON * 2)
    else:
        cut_z = depth - depth_engraving
        cut_depth = depth_engraving + _EPSILON

    logo_cut = translate([0, 0, cut_z])(linear_extrude(height=cut_depth)(logo_2d))
    return difference()(disk, logo_cut)


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
            "preview_rot": [55, 0, 25],
            "kwargs": {"radius": 20, "depth": 3, "pos": [0, 0, 0]},
        },
        {
            "filename": "test_2",
            "preview_rot": [55, 0, 25],
            "kwargs": {"radius": 20, "depth": 4, "depth_engraving": 1.2, "pos": [0, 0, 0]},
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

        wrapped = components
        preview_rot = sample.get("preview_rot", [0, 0, 0])
        if preview_rot != [0, 0, 0]:
            wrapped = [
                {
                    "type": "rotation",
                    "typetype": "positive",
                    "pos": [0, 0, 0],
                    "rot": preview_rot,
                    "objects": components,
                }
            ]

        opsc.opsc_make_object(
            scad_path,
            wrapped,
            mode="true",
            save_type="none",
            overwrite=True,
            render=True,
        )
        opsc.save_preview_images(scad_path, sample_dir)
        generated_files.append(png_path)

    return generated_files
