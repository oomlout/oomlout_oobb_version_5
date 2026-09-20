import copy
import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

_COMPONENT_ROOT = os.path.dirname(os.path.abspath(__file__))
_DEFAULT_DATA = "https://www.patreon.com"
_DEFAULT_SIZE = 30.0
_DEFAULT_DEPTH = 1.5
_DEFAULT_BORDER = 2
_DEFAULT_ERROR_CORRECTION = "m"

d = {}


def _variable(name, description, value_type, default):
    return {"name": name, "description": description, "type": value_type, "default": default}


def describe():
    global d
    d = {}
    d["name"] = "qr_code"
    d["name_long"] = "QR Code"
    d["description"] = (
        "QR code geometry generated from a data string. Dark modules are "
        "extruded to the requested depth; use as a positive for a raised code "
        "or as a negative to engrave it into a face."
    )
    d["category"] = "OOBB Custom Components"
    d["shape_aliases"] = ["qr_code"]
    d["returns"] = "List of geometry component dicts."
    v = []
    v.append(_variable("data", "Text or URL the QR code encodes.", "string", f'"{_DEFAULT_DATA}"'))
    v.append(_variable("size", "Overall square size in mm including the quiet-zone border.", "number", _DEFAULT_SIZE))
    v.append(_variable("depth", "Extrusion depth of the dark modules in mm.", "number", _DEFAULT_DEPTH))
    v.append(_variable("border", "Quiet-zone width in modules kept clear around the code.", "number", _DEFAULT_BORDER))
    v.append(
        _variable(
            "error_correction",
            "QR error correction level: l, m, q, or h.",
            "string",
            f'"{_DEFAULT_ERROR_CORRECTION}"',
        )
    )
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


def _get_matrix(data, error_correction):
    import qrcode
    from qrcode import constants

    levels = {
        "l": constants.ERROR_CORRECT_L,
        "m": constants.ERROR_CORRECT_M,
        "q": constants.ERROR_CORRECT_Q,
        "h": constants.ERROR_CORRECT_H,
    }
    level = levels.get(str(error_correction).lower(), constants.ERROR_CORRECT_M)
    qr = qrcode.QRCode(error_correction=level, border=0, box_size=1)
    qr.add_data(data)
    qr.make(fit=True)
    return qr.get_matrix()


def _anchored_pos(params, depth):
    pos = copy.deepcopy(params.get("pos", [params.get("x", 0), params.get("y", 0), params.get("z", 0)]))
    zz = params.get("zz", "bottom")
    if zz in ("center", "middle"):
        pos[2] -= depth / 2
    elif zz == "top":
        pos[2] -= depth
    return pos


def action(**kwargs):
    params = copy.deepcopy(kwargs)
    depth = _as_float(params.get("depth", params.get("h", _DEFAULT_DEPTH)), _DEFAULT_DEPTH)
    object_type = params.get("type", "positive")
    rot = params.get("rot", [params.get("rot_x", 0), params.get("rot_y", 0), params.get("rot_z", 0)])

    code = {
        "type": "positive",
        "shape": "qr_code",
        "data": str(params.get("data", params.get("url", _DEFAULT_DATA))),
        "size": _as_float(params.get("size", None), _DEFAULT_SIZE),
        "depth": depth,
        "border": int(_as_float(params.get("border", None), _DEFAULT_BORDER)),
        "error_correction": str(params.get("error_correction", _DEFAULT_ERROR_CORRECTION)),
        "pos": [0, 0, 0],
    }

    rotation = {
        "type": "rotation",
        "typetype": object_type,
        "pos": _anchored_pos(params, depth),
        "rot": rot,
        "objects": [code],
    }
    if params.get("m", "") != "":
        rotation["m"] = params["m"]
    if params.get("inclusion", "") != "":
        rotation["inclusion"] = params["inclusion"]
    return [rotation]


def render(params):
    from solid2 import cube, translate, union

    data = str(params.get("data", params.get("url", _DEFAULT_DATA)))
    size = _as_float(params.get("size", None), _DEFAULT_SIZE)
    depth = _as_float(params.get("depth", params.get("h", _DEFAULT_DEPTH)), _DEFAULT_DEPTH)
    border = int(_as_float(params.get("border", None), _DEFAULT_BORDER))
    error_correction = params.get("error_correction", _DEFAULT_ERROR_CORRECTION)

    matrix = _get_matrix(data, error_correction)
    module_count = len(matrix)
    total_modules = module_count + (2 * border)
    module_size = size / total_modules

    # Merge horizontal runs of dark modules so OpenSCAD receives one box per
    # run rather than one per module.
    runs = []
    for row_index, row in enumerate(matrix):
        column = 0
        while column < module_count:
            if row[column]:
                run_start = column
                while column < module_count and row[column]:
                    column += 1
                runs.append((row_index, run_start, column - run_start))
            else:
                column += 1

    parts = []
    for row_index, run_start, run_length in runs:
        x = -size / 2 + (run_start + border) * module_size
        y = size / 2 - (row_index + border + 1) * module_size
        parts.append(
            translate([x, y, 0])(
                cube([run_length * module_size, module_size, depth])
            )
        )
    return union()(*parts)


def test():
    import opsc

    folder = os.path.dirname(os.path.abspath(__file__))
    test_dir = os.path.join(folder, "test")
    os.makedirs(test_dir, exist_ok=True)

    samples = [
        {
            "filename": "test_1",
            "preview_rot": [55, 0, 25],
            "kwargs": {
                "data": "https://www.patreon.com/cw/ZoeEady",
                "size": 30,
                "depth": 1.5,
                "pos": [0, 0, 0],
            },
        },
        {
            "filename": "test_2",
            "preview_rot": [55, 0, 25],
            "kwargs": {
                "data": "https://www.patreon.com/cw/ZoeEady",
                "size": 40,
                "depth": 3,
                "border": 4,
                "pos": [0, 0, 0],
            },
        },
    ]

    generated_files = []
    for sample in samples:
        result = action(**copy.deepcopy(sample["kwargs"]))
        components = copy.deepcopy(result)
        preview_rot = sample.get("preview_rot", [0, 0, 0])
        if preview_rot != [0, 0, 0]:
            components = [
                {
                    "type": "rotation",
                    "typetype": "positive",
                    "pos": [0, 0, 0],
                    "rot": preview_rot,
                    "objects": components,
                }
            ]

        sample_dir = os.path.join(test_dir, sample["filename"])
        os.makedirs(sample_dir, exist_ok=True)
        scad_path = os.path.join(sample_dir, "working.scad")
        opsc.opsc_make_object(
            scad_path,
            components,
            mode="true",
            save_type="none",
            overwrite=True,
            render=True,
        )
        opsc.save_preview_images(scad_path, sample_dir)
        generated_files.append(os.path.join(sample_dir, "image.png"))

    return generated_files
