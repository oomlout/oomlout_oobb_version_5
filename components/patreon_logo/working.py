import copy
import math
import os
import shutil
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

_COMPONENT_ROOT = os.path.dirname(os.path.abspath(__file__))
_SCAD_LOGO = os.path.join(_COMPONENT_ROOT, "image_scad.svg")
_DEFAULT_SIZE = 50.0
_DEFAULT_DEPTH = 3.0
_DEFAULT_ENGRAVING_DEPTH = 1.5
_DEFAULT_CORNER_RADIUS = 4.0
_DEFAULT_EDGE_RADIUS = 0.0
_DEFAULT_LOGO_SIZE_PERCENT = 0.82
_DEFAULT_BODY_SHAPE = "rounded_square"
_EPSILON = 0.01

d = {}


def _variable(name, description, value_type, default):
    return {"name": name, "description": description, "type": value_type, "default": default}


def describe():
    global d
    d = {}
    d["name"] = "patreon_logo"
    d["name_long"] = "Patreon Logo Badge"
    d["description"] = (
        "Circular or rounded-square badge with the Patreon logo subtracted "
        "from the top face for engraving or colour inlay."
    )
    d["category"] = "OOBB Custom Components"
    d["shape_aliases"] = ["patreon_logo"]
    d["returns"] = "List of geometry component dicts."
    v = []
    v.append(_variable("size", "Outer diameter / square side length in mm.", "number", _DEFAULT_SIZE))
    v.append(_variable("depth", "Badge depth in mm.", "number", _DEFAULT_DEPTH))
    v.append(
        _variable(
            "depth_engraving",
            "Logo cut depth in mm.",
            "number",
            _DEFAULT_ENGRAVING_DEPTH,
        )
    )
    v.append(
        _variable(
            "body_shape",
            "Badge outline: 'rounded_square' or 'circle'.",
            "string",
            f'"{_DEFAULT_BODY_SHAPE}"',
        )
    )
    v.append(
        _variable(
            "corner_radius",
            "Plan-view corner radius in mm (rounded_square only).",
            "number",
            _DEFAULT_CORNER_RADIUS,
        )
    )
    v.append(
        _variable(
            "radius_rounded",
            "Top and bottom perimeter edge radius in mm; zero keeps square edges.",
            "number",
            _DEFAULT_EDGE_RADIUS,
        )
    )
    v.append(
        _variable(
            "logo_size_percent",
            "Logo width as a fraction of the badge size.",
            "number",
            _DEFAULT_LOGO_SIZE_PERCENT,
        )
    )
    v.append(
        _variable(
            "logo_shift",
            "2-element [x,y] shift of the logo engraving in mm.",
            "list",
            "[0,0]",
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


def _get_size(params):
    value = params.get("size", params.get("side_length", params.get("diameter", params.get("width", _DEFAULT_SIZE))))
    if isinstance(value, (list, tuple)):
        value = value[0] if value else _DEFAULT_SIZE
    return _as_float(value, _DEFAULT_SIZE)


def _get_body_shape(params):
    value = str(params.get("body_shape", params.get("badge_shape", _DEFAULT_BODY_SHAPE))).lower()
    if value in ("square", "rounded_rectangle", "rounded_square"):
        return "rounded_square"
    if value in ("circle", "circular", "round"):
        return "circle"
    return _DEFAULT_BODY_SHAPE


def _get_logo_shift(params):
    value = params.get("logo_shift", [0, 0])
    if not isinstance(value, (list, tuple)):
        return [0, 0]
    values = list(value) + [0, 0]
    return [_as_float(values[0], 0), _as_float(values[1], 0)]


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
    destination_name = "patreon_logo.svg"
    destination_path = os.path.join(cache_dir, destination_name)
    if os.path.abspath(source_path) != os.path.abspath(destination_path):
        shutil.copyfile(source_path, destination_path)
    return destination_name


def action(**kwargs):
    params = copy.deepcopy(kwargs)
    size = _get_size(params)
    depth = _as_float(params.get("depth", params.get("h", _DEFAULT_DEPTH)), _DEFAULT_DEPTH)
    object_type = params.get("type", "positive")
    rot = params.get("rot", [params.get("rot_x", 0), params.get("rot_y", 0), params.get("rot_z", 0)])

    badge = {
        "type": "positive",
        "shape": "patreon_logo",
        "size": size,
        "depth": depth,
        "depth_engraving": _as_float(
            params.get("depth_engraving", None), _DEFAULT_ENGRAVING_DEPTH
        ),
        "body_shape": _get_body_shape(params),
        "corner_radius": _as_float(
            params.get("corner_radius", None), _DEFAULT_CORNER_RADIUS
        ),
        "radius_rounded": _as_float(
            params.get("radius_rounded", None), _DEFAULT_EDGE_RADIUS
        ),
        "logo_size_percent": _as_float(
            params.get("logo_size_percent", None), _DEFAULT_LOGO_SIZE_PERCENT
        ),
        "logo_shift": _get_logo_shift(params),
        "file": params.get("file", params.get("image", _SCAD_LOGO)),
        "pos": [0, 0, 0],
    }

    rotation = {
        "type": "rotation",
        "typetype": object_type,
        "pos": _anchored_pos(params, depth),
        "rot": rot,
        "objects": [badge],
    }
    if params.get("m", "") != "":
        rotation["m"] = params["m"]
    if params.get("inclusion", "") != "":
        rotation["inclusion"] = params["inclusion"]
    return [rotation]


def _rounded_square_body(size, depth, corner_radius, edge_radius):
    from solid2 import cylinder, hull, translate, union

    corner_offset = (size / 2) - corner_radius
    if edge_radius <= _EPSILON:
        return hull()(
            translate([-corner_offset, -corner_offset, 0])(cylinder(r=corner_radius, h=depth)),
            translate([corner_offset, -corner_offset, 0])(cylinder(r=corner_radius, h=depth)),
            translate([-corner_offset, corner_offset, 0])(cylinder(r=corner_radius, h=depth)),
            translate([corner_offset, corner_offset, 0])(cylinder(r=corner_radius, h=depth)),
        )

    section_depth = _EPSILON

    def rounded_section(z, inset):
        section_radius = max(corner_radius - inset, _EPSILON)
        return hull()(
            translate([-corner_offset, -corner_offset, z])(
                cylinder(r=section_radius, h=section_depth)
            ),
            translate([corner_offset, -corner_offset, z])(
                cylinder(r=section_radius, h=section_depth)
            ),
            translate([-corner_offset, corner_offset, z])(
                cylinder(r=section_radius, h=section_depth)
            ),
            translate([corner_offset, corner_offset, z])(
                cylinder(r=section_radius, h=section_depth)
            ),
        )

    edge_segments = 8
    profiles = []
    for index in range(edge_segments + 1):
        z = edge_radius * index / edge_segments
        distance_from_center = edge_radius - z
        inset = edge_radius - math.sqrt(
            max(0, edge_radius**2 - distance_from_center**2)
        )
        profiles.append((z, inset))

    body_parts = []
    for index in range(edge_segments):
        z_1, inset_1 = profiles[index]
        z_2, inset_2 = profiles[index + 1]
        body_parts.append(
            hull()(
                rounded_section(z_1, inset_1),
                rounded_section(z_2, inset_2),
            )
        )
        body_parts.append(
            hull()(
                rounded_section(depth - z_1 - section_depth, inset_1),
                rounded_section(depth - z_2 - section_depth, inset_2),
            )
        )

    body_parts.append(
        hull()(
            translate([-corner_offset, -corner_offset, edge_radius])(
                cylinder(r=corner_radius, h=depth - edge_radius * 2)
            ),
            translate([corner_offset, -corner_offset, edge_radius])(
                cylinder(r=corner_radius, h=depth - edge_radius * 2)
            ),
            translate([-corner_offset, corner_offset, edge_radius])(
                cylinder(r=corner_radius, h=depth - edge_radius * 2)
            ),
            translate([corner_offset, corner_offset, edge_radius])(
                cylinder(r=corner_radius, h=depth - edge_radius * 2)
            ),
        )
    )
    return union()(*body_parts)


def _circle_body(size, depth, edge_radius):
    from solid2 import cylinder, hull, translate, union

    radius = size / 2
    if edge_radius <= _EPSILON:
        return cylinder(r=radius, h=depth)

    section_depth = _EPSILON

    def rounded_section(z, inset):
        section_radius = max(radius - inset, _EPSILON)
        return translate([0, 0, z])(cylinder(r=section_radius, h=section_depth))

    edge_segments = 8
    profiles = []
    for index in range(edge_segments + 1):
        z = edge_radius * index / edge_segments
        distance_from_center = edge_radius - z
        inset = edge_radius - math.sqrt(
            max(0, edge_radius**2 - distance_from_center**2)
        )
        profiles.append((z, inset))

    body_parts = []
    for index in range(edge_segments):
        z_1, inset_1 = profiles[index]
        z_2, inset_2 = profiles[index + 1]
        body_parts.append(
            hull()(
                rounded_section(z_1, inset_1),
                rounded_section(z_2, inset_2),
            )
        )
        body_parts.append(
            hull()(
                rounded_section(depth - z_1 - section_depth, inset_1),
                rounded_section(depth - z_2 - section_depth, inset_2),
            )
        )

    body_parts.append(
        translate([0, 0, edge_radius])(
            cylinder(r=radius, h=depth - edge_radius * 2)
        )
    )
    return union()(*body_parts)


def render(params):
    from solid2 import difference, import_, linear_extrude, scale, translate

    size = _get_size(params)
    depth = _as_float(params.get("depth", params.get("h", _DEFAULT_DEPTH)), _DEFAULT_DEPTH)
    depth_engraving = _as_float(
        params.get("depth_engraving", None), _DEFAULT_ENGRAVING_DEPTH
    )
    depth_engraving = max(0, min(depth_engraving, depth))
    body_shape = _get_body_shape(params)
    corner_radius = _as_float(
        params.get("corner_radius", None), _DEFAULT_CORNER_RADIUS
    )
    corner_radius = max(_EPSILON, min(corner_radius, size / 2))
    edge_radius = _as_float(
        params.get("radius_rounded", None), _DEFAULT_EDGE_RADIUS
    )
    edge_radius = max(0, min(edge_radius, corner_radius, depth / 2))

    logo_file = _resolve_logo_file(params.get("file", params.get("image", _SCAD_LOGO)))
    if not os.path.isfile(logo_file):
        raise FileNotFoundError(f"patreon_logo SVG not found: {logo_file}")

    logo_size_percent = _as_float(
        params.get("logo_size_percent", None), _DEFAULT_LOGO_SIZE_PERCENT
    )
    logo_size = size * logo_size_percent
    logo_shift = _get_logo_shift(params)
    logo_import_file = _copy_logo_file(logo_file, params.get("cache_dir"))

    if body_shape == "circle":
        body = _circle_body(size, depth, edge_radius)
    else:
        body = _rounded_square_body(size, depth, corner_radius, edge_radius)

    # OpenSCAD preserves the SVG's 0..1 physical bounds. Shift both axes by
    # half a unit before scaling so the logo is centred on the body.
    logo_2d = scale([logo_size, logo_size, 1])(
        translate([-0.5, -0.5, 0])(import_(file=logo_import_file))
    )

    if depth_engraving >= depth:
        cut_z = -_EPSILON
        cut_depth = depth + (_EPSILON * 2)
    else:
        cut_z = depth - depth_engraving
        cut_depth = depth_engraving + _EPSILON

    logo_cut = translate([logo_shift[0], logo_shift[1], cut_z])(
        linear_extrude(height=cut_depth)(logo_2d)
    )
    return difference()(body, logo_cut)


def test():
    import opsc

    folder = os.path.dirname(os.path.abspath(__file__))
    test_dir = os.path.join(folder, "test")
    os.makedirs(test_dir, exist_ok=True)

    samples = [
        {
            "filename": "test_1",
            "preview_rot": [55, 0, 25],
            "kwargs": {"size": 50, "depth": 6, "corner_radius": 4, "radius_rounded": 1.5, "pos": [0, 0, 0]},
        },
        {
            "filename": "test_2",
            "preview_rot": [55, 0, 25],
            "kwargs": {
                "size": 50,
                "depth": 6,
                "body_shape": "circle",
                "radius_rounded": 1.5,
                "depth_engraving": 1.5,
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
