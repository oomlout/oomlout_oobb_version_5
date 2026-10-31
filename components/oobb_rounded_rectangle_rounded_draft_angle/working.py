import copy
import importlib.util
import math
import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)


def _load_component(folder_name):
    path = os.path.join(_PROJECT_ROOT, "components", folder_name, "working.py")
    spec = importlib.util.spec_from_file_location(f"comp_{folder_name}", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load component {folder_name!r} from {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_rounded_mod = _load_component("oobb_rounded_rectangle_rounded")
_rounded_action = _rounded_mod.action

d = {}


def describe():
    global d
    d = {
        "name": "oobb_rounded_rectangle_rounded_draft_angle",
        "name_long": "OOBB Geometry Primitives: Rounded Rectangle with Draft Angle",
        "description": "Rounded rectangle with rounded top and bottom edges and side walls that taper inward toward the bottom for injection-moulding design.",
        "category": "OOBB Geometry Primitives",
        "shape_aliases": ["rounded_rectangle_rounded_draft_angle"],
        "returns": "List of geometry component dicts.",
        "variables": [
            {"name": "pos", "description": "3-element [x,y,z] position.", "type": "list", "default": "[0,0,0]"},
            {"name": "type", "description": "Geometry type: p/positive or n/negative.", "type": "string", "default": "p"},
            {"name": "size", "description": "Overall [x,y,z] dimensions of the undrafted reference shape, in mm.", "type": "list", "default": "[20,10,5]"},
            {"name": "radius", "description": "Corner radius of the base shape.", "type": "number", "default": 5},
            {"name": "radius_rounded", "description": "Rounding radius for top/bottom edges.", "type": "number", "default": 2.5},
            {"name": "draft_angle", "description": "Side-wall draft angle in degrees. Positive values taper the bottom inward relative to the top.", "type": "number", "default": 1},
            {"name": "extra", "description": "Extra variant/modifier string.", "type": "string", "default": '""'},
            {"name": "rot", "description": "Rotation [rx,ry,rz] in degrees.", "type": "list", "default": "[0,0,0]"},
            {"name": "rot_x", "description": "X rotation in degrees.", "type": "number", "default": 0},
            {"name": "rot_y", "description": "Y rotation in degrees.", "type": "number", "default": 0},
            {"name": "rot_z", "description": "Z rotation in degrees.", "type": "number", "default": 0},
        ],
    }
    return d


def define():
    global d
    if not isinstance(d, dict) or not d:
        describe()
    return copy.deepcopy(d)


def action(**kwargs):
    params = copy.deepcopy(kwargs)
    params.setdefault("type", "positive")
    params["shape"] = "oobb_rounded_rectangle_rounded_draft_angle"
    params.setdefault("draft_angle", 1)
    return [params]


def render(params):
    import opsc
    from solid2 import intersection, hull
    from solidpython_compat import apply_modifier

    p = copy.deepcopy(params)
    modifier = p.get("m", "")
    draft_angle = float(p.get("draft_angle", 1))
    size = list(p.get("size", [20, 10, 5]))
    if len(size) != 3:
        raise ValueError("size must contain [width, height, depth]")
    width, height, depth = [float(value) for value in size]
    if width <= 0 or height <= 0 or depth <= 0:
        raise ValueError("size dimensions must be greater than zero")
    if not math.isfinite(draft_angle) or draft_angle < 0 or draft_angle >= 89:
        raise ValueError("draft_angle must be finite and between 0 and 89 degrees")

    radius = float(p.get("radius", 5))
    radius_rounded = float(p.get("radius_rounded", 2.5))
    contraction = 2 * depth * math.tan(math.radians(draft_angle))
    bottom_width = width - contraction
    bottom_height = height - contraction
    if bottom_width <= 0 or bottom_height <= 0:
        raise ValueError("draft_angle and size produce a non-positive bottom width or height")

    # Build the undrafted rounded-edge form at the origin. The normal component
    # renderer applies position and rotation after this local geometry is built.
    base_params = copy.deepcopy(p)
    base_params.update({
        "pos": [0, 0, 0],
        "rot": [0, 0, 0],
        "rot_x": 0,
        "rot_y": 0,
        "rot_z": 0,
        "type": "positive",
        "draft_angle": 0,
        "m": "",
    })
    base_components = _rounded_action(**base_params)
    base_solid = opsc.opsc_get_object(base_components, mode=opsc.mode)

    # A hull between thin rounded-rectangle profiles forms the drafted envelope.
    # The top stays at the requested size; the bottom moves inward by
    # depth*tan(a) on each side for positive draft angles.
    epsilon = min(0.01, depth / 100)
    corner_radius = max(0.01, min(radius - radius_rounded, width / 2 - 0.01, height / 2 - 0.01))
    bottom_corner_radius = max(0.01, min(corner_radius, bottom_width / 2 - 0.01, bottom_height / 2 - 0.01))
    bottom_profile = {
        "type": "positive", "shape": "rounded_rectangle",
        "size": [bottom_width, bottom_height, epsilon], "r": bottom_corner_radius,
        "pos": [0, 0, 0], "m": "",
    }
    top_profile = {
        "type": "positive", "shape": "rounded_rectangle",
        "size": [width, height, epsilon], "r": corner_radius,
        "pos": [0, 0, depth - epsilon], "m": "",
    }
    envelope = hull()(
        opsc.get_opsc_item(bottom_profile),
        opsc.get_opsc_item(top_profile),
    )
    drafted_solid = intersection()(base_solid, envelope)
    return apply_modifier(drafted_solid, modifier)


def test():
    import copy
    import os
    import opsc

    folder = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(folder, "images")
    os.makedirs(images_dir, exist_ok=True)

    samples = [
        {
            "filename": "draft_0_degrees",
            "preview_rot": [60, 0, 25],
            "kwargs": {"pos": [0, 0, 0], "type": "positive", "size": [30, 20, 20], "radius": 5, "radius_rounded": 2, "draft_angle": 0},
        },
        {
            "filename": "draft_1_degree",
            "preview_rot": [60, 0, 25],
            "kwargs": {"pos": [0, 0, 0], "type": "positive", "size": [30, 20, 20], "radius": 5, "radius_rounded": 2, "draft_angle": 1},
        },
        {
            "filename": "draft_5_degrees",
            "preview_rot": [60, 0, 25],
            "kwargs": {"pos": [0, 0, 0], "type": "positive", "size": [30, 20, 20], "radius": 5, "radius_rounded": 2, "draft_angle": 5},
        },
    ]

    generated_files = []

    for sample in samples:
        kwargs = copy.deepcopy(sample["kwargs"])
        result = action(**kwargs)
        if isinstance(result, list):
            components = result
        else:
            components = [result]

        preview_rot = sample["preview_rot"]
        wrapped = components
        if preview_rot != [0, 0, 0]:
            wrapped = [{
                "type": "rotation",
                "typetype": "positive",
                "pos": [0, 0, 0],
                "rot": preview_rot,
                "objects": components,
            }]

        scad_path = os.path.join(images_dir, f"{sample['filename']}.scad")
        png_path = os.path.join(images_dir, f"{sample['filename']}.png")

        opsc.opsc_make_object(
            scad_path,
            wrapped,
            mode="true",
            save_type="none",
            overwrite=True,
            render=True,
        )
        opsc.save_to_png(scad_path, fileOut=png_path)
        # Some OpenSCAD builds require an explicit value for --render. Keep the
        # standard helper call above, then retry with the equivalent CLI flag
        # when that helper did not produce a PNG on this installation.
        if not os.path.exists(png_path):
            opsc.save_to_file(
                scad_path,
                png_path,
                extra="--render=1 --autocenter --viewall --projection o",
            )
        generated_files.append(png_path)

    return generated_files
