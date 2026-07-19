import copy
import hashlib
import os
import re
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

_COMPONENT_ROOT = os.path.dirname(os.path.abspath(__file__))
_DEFAULT_IMAGE = os.path.join(_COMPONENT_ROOT, "icon.png")
_NORMALIZED_PIXEL_WIDTH = 1000

d = {}


def _variable(name, description, value_type, default):
    return {"name": name, "description": description, "type": value_type, "default": default}


def describe():
    global d
    d = {}
    d["name"] = "oobb_surface"
    d["name_long"] = "OOBB Geometry Primitives: Surface"
    d["description"] = (
        "Creates an OpenSCAD heightmap surface from an image, normalizing the source to "
        "1000 pixels wide and scaling width, height, and relief depth in millimeters."
    )
    d["category"] = "OOBB Geometry Primitives"
    d["shape_aliases"] = ["oobb_surface", "surface"]
    d["returns"] = "List of geometry component dicts."
    v = []
    v.append(_variable("file", "Image file to turn into an OpenSCAD surface. image is accepted as an alias.", "string", '"icon.png"'))
    v.append(_variable("image", "Alias for file.", "string", ""))
    v.append(_variable("width", "Surface width in mm. If height is omitted, the image aspect ratio sets height.", "number", ""))
    v.append(_variable("height", "Surface height in mm. If width is omitted, the image aspect ratio sets width.", "number", ""))
    v.append(_variable("depth", "Relief depth in mm, mapped from OpenSCAD surface's 0..100 height range.", "number", 1))
    v.append(_variable("pos", "3-element [x,y,z] position.", "list", "[0,0,0]"))
    v.append(_variable("rot", "Rotation [rx,ry,rz] in degrees.", "list", "[0,0,0]"))
    v.append(_variable("zz", "Z anchor point: bottom, top, center/middle.", "string", '"bottom"'))
    v.append(_variable("slice_bottom", "Subtract a cube from the bottom of the heightmap to slice away the low background.", "bool", True))
    v.append(_variable("center", "Center the OpenSCAD surface around the origin in X/Y.", "bool", True))
    v.append(_variable("invert", "OpenSCAD surface invert flag. True makes darker pixels higher.", "bool", True))
    v.append(_variable("convexity", "OpenSCAD surface convexity.", "number", 10))
    v.append(_variable("type", "Geometry type: positive or negative.", "string", '"positive"'))
    v.append(_variable("m", "OpenSCAD modifier prefix, e.g. #, %, *.", "string", '""'))
    d["variables"] = v
    return d


def define():
    global d
    if not isinstance(d, dict) or not d:
        describe()
    defined = {}
    defined.update(d)
    return defined


def _resolve_image_path(path):
    if not path:
        return _DEFAULT_IMAGE
    path = os.path.expanduser(str(path))
    if os.path.isabs(path):
        return path
    component_candidate = os.path.join(_COMPONENT_ROOT, path)
    if os.path.isfile(component_candidate):
        return component_candidate
    return os.path.abspath(path)


def _as_float(value, default=None):
    if value in ("", None):
        return default
    return float(value)


def _as_bool(value, default=False):
    if value in ("", None):
        return default
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "on", "ptrue"}
    return bool(value)


def _safe_stem(path):
    stem = os.path.splitext(os.path.basename(path))[0]
    stem = re.sub(r"[^A-Za-z0-9_.-]", "_", stem)
    return stem or "surface"


def _cache_root(cache_dir):
    if cache_dir:
        return os.path.abspath(cache_dir)
    root = os.path.join(_COMPONENT_ROOT, "_surface_cache")
    os.makedirs(root, exist_ok=True)
    return root


def _normalize_image(source_path, output_dir):
    try:
        from PIL import Image
    except ImportError as exc:
        raise RuntimeError("oobb_surface requires Pillow to resize source images.") from exc

    if not os.path.isfile(source_path):
        raise FileNotFoundError(f"oobb_surface image file not found: {source_path}")

    with Image.open(source_path) as image:
        original_width, original_height = image.size
        if original_width <= 0 or original_height <= 0:
            raise ValueError(f"oobb_surface image has invalid dimensions: {source_path}")

        normalized_height = max(1, round(original_height * (_NORMALIZED_PIXEL_WIDTH / original_width)))
        resized = image.convert("RGBA").resize(
            (_NORMALIZED_PIXEL_WIDTH, normalized_height),
            Image.Resampling.LANCZOS,
        )

        digest_source = f"{os.path.abspath(source_path)}|{os.path.getmtime(source_path)}|{original_width}x{original_height}"
        digest = hashlib.sha256(digest_source.encode("utf-8")).hexdigest()[:12]
        filename = f"{_safe_stem(source_path)}_{_NORMALIZED_PIXEL_WIDTH}px_{digest}.png"
        normalized_path = os.path.join(output_dir, filename)
        resized.save(normalized_path)

    return normalized_path, _NORMALIZED_PIXEL_WIDTH, normalized_height


def _resolve_size(width, height, pixel_width, pixel_height):
    aspect = pixel_height / pixel_width
    width = _as_float(width)
    height = _as_float(height)

    if width is None and height is None:
        width = 60.0
        height = width * aspect
    elif width is None:
        width = height / aspect
    elif height is None:
        height = width * aspect

    return width, height


def _z_offset(depth, zz):
    if zz in ("center", "middle"):
        return -depth / 2
    if zz == "top":
        return -depth
    return 0


def _scad_bool(value):
    return "true" if bool(value) else "false"


def _write_surface_scad(params, local_png_path, pixel_width, pixel_height, output_dir):
    width, height = _resolve_size(params.get("width"), params.get("height"), pixel_width, pixel_height)
    depth = _as_float(params.get("depth", 1), 1)
    center = _as_bool(params.get("center", True), True)
    invert = _as_bool(params.get("invert", True), True)
    slice_bottom = _as_bool(params.get("slice_bottom", True), True)
    convexity = int(params.get("convexity", 10))
    zz = params.get("zz", "bottom")

    x_scale = width / pixel_width
    y_scale = height / pixel_height
    z_scale = depth / 100
    z_offset = _z_offset(depth, zz)

    local_png_filename = os.path.basename(local_png_path)
    module_digest = hashlib.sha256(
        f"{local_png_filename}|{width}|{height}|{depth}|{center}|{invert}|{convexity}|{zz}|{slice_bottom}".encode("utf-8")
    ).hexdigest()[:12]
    module_name = f"oobb_surface_{module_digest}"
    raw_module_name = f"{module_name}_raw"
    scad_path = os.path.join(output_dir, f"{module_name}.scad")

    clip_margin = 1
    clip_x = (-width / 2 - clip_margin) if center else -clip_margin
    clip_y = (-height / 2 - clip_margin) if center else -clip_margin
    if slice_bottom:
        if invert:
            slice_z = z_offset + depth - (abs(z_scale) * 0.1)
            subtract_height = clip_margin + (abs(z_scale) * 0.1)
            subtract_z = -slice_z - clip_margin + 0.25
        else:
            slice_z = z_offset + (abs(z_scale) * 0.1)
            subtract_z = z_offset - clip_margin
            subtract_height = slice_z - subtract_z
        body = f"""difference() {{
            {raw_module_name}();
            translate([{clip_x:.12g}, {clip_y:.12g}, {subtract_z:.12g}])
                cube([{width + clip_margin * 2:.12g}, {height + clip_margin * 2:.12g}, {subtract_height:.12g}], center = false);
        }}"""
    else:
        body = f"{raw_module_name}();"

    source = f"""module {raw_module_name}() {{
    translate([0, 0, {z_offset:.9g}])
        scale([{x_scale:.12g}, {y_scale:.12g}, {z_scale:.12g}])
            surface(file = "{local_png_filename}", center = {_scad_bool(center)}, invert = {_scad_bool(invert)}, convexity = {convexity});
}}

module {module_name}() {{
    rotate([0, 0, 0]) {{
        {body}
    }}
}}
"""
    with open(scad_path, "w", encoding="utf-8") as handle:
        handle.write(source)

    return scad_path, module_name


def action(**kwargs):
    params = copy.deepcopy(kwargs)
    params.setdefault("type", "positive")
    params.setdefault("shape", "oobb_surface")
    params.setdefault("file", params.get("image", "icon.png"))
    params.setdefault("depth", 1)
    params.setdefault("center", True)
    params.setdefault("invert", True)
    params.setdefault("slice_bottom", True)
    params.setdefault("convexity", 10)
    params.setdefault("pos", [0, 0, 0])
    return [params]


def render(params):
    from solid2 import import_scad

    source_image = _resolve_image_path(params.get("file", params.get("image", "")))
    output_dir = _cache_root(params.get("cache_dir"))
    os.makedirs(output_dir, exist_ok=True)

    local_png_path, pixel_width, pixel_height = _normalize_image(source_image, output_dir)
    scad_path, module_name = _write_surface_scad(params, local_png_path, pixel_width, pixel_height, output_dir)

    scad_object = import_scad(scad_path, use_not_include=True)
    module_fn = getattr(scad_object, module_name)
    result = module_fn()

    if params.get("cache_dir"):
        include_path = os.path.relpath(scad_path, params["cache_dir"]).replace("\\", "/")
        result.include_file_path = include_path
        result.include_string = f"use <{include_path}>;\n"

    return result


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
            "kwargs": {"type": "positive", "file": "icon.png", "width": 60, "depth": 1, "pos": [0, 0, 0]},
        },
        {
            "filename": "test_2",
            "preview_rot": [65, 0, 25],
            "kwargs": {"type": "positive", "file": "icon.png", "height": 35, "depth": 1.5, "zz": "center", "pos": [0, 0, 0]},
        },
        {
            "filename": "test_3",
            "preview_rot": [65, 0, 25],
            "kwargs": {"type": "positive", "file": "icon.png", "width": 70, "height": 35, "depth": 1, "pos": [0, 0, 0]},
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
