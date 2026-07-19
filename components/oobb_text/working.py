import copy
import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

d = {}


def describe():
    global d
    d = {}
    d["name"] = "oobb_text"
    d["name_long"] = "OOBB Geometry Primitives: Text"
    d["description"] = "Legacy OOBB text helper that creates centered extruded text with OOBB defaults."
    d["category"] = "OOBB Geometry Primitives"
    d["shape_aliases"] = ["oobb_text"]
    d["returns"] = "List of geometry component dicts."
    v = []
    v.append({"name": "pos", "description": "3-element [x,y,z] position.", "type": "list", "default": "[0,0,0]"})
    v.append({"name": "text", "description": "Text string to render.", "type": "string", "default": '""'})
    v.append({"name": "concate", "description": "Legacy abbreviation flag: keep the first character and each character after an underscore.", "type": "bool", "default": False})
    v.append({"name": "height", "description": "Extrusion height in mm.  depth and h are accepted as aliases.", "type": "number", "default": 0.3})
    v.append({"name": "depth", "description": "Alias for height, with priority over h and height when supplied.", "type": "number", "default": ""})
    v.append({"name": "h", "description": "Alias for height, used when depth is not supplied.", "type": "number", "default": ""})
    v.append({"name": "size", "description": "OpenSCAD text size.", "type": "number", "default": 7})
    v.append({"name": "font", "description": "OpenSCAD font name.", "type": "string", "default": '"Candara:Light"'})
    v.append({"name": "halign", "description": "Horizontal alignment: left, center, or right.", "type": "string", "default": '"center"'})
    v.append({"name": "valign", "description": "Vertical alignment: top, center, baseline, or bottom.", "type": "string", "default": '"center"'})
    v.append({"name": "minkowski_radius", "description": "Radius in mm of a circular 2D Minkowski expansion applied before extrusion. Zero keeps the legacy plain-text path.", "type": "number", "default": 0})
    v.append({"name": "minkowski", "description": "Legacy-friendly alias for minkowski_radius.", "type": "number", "default": 0})
    v.append({"name": "type", "description": "Geometry type/modifier context, usually positive or negative.", "type": "string", "default": '"positive"'})
    v.append({"name": "m", "description": "OpenSCAD modifier prefix, e.g. #, %, *.", "type": "string", "default": '""'})
    d["variables"] = v
    return d


def define():
    global d
    if not isinstance(d, dict) or not d:
        describe()
    defined = {}
    defined.update(d)
    return defined


def _abbreviate_text(text):
    if not text:
        return text
    text = str(text)
    return text[0] + "".join(part[0] for part in text.split("_")[1:] if part)


def action(**kwargs):
    import opsc

    params = copy.deepcopy(kwargs)

    depth = params.get("depth", None)
    h = params.get("h", None)
    height = params.get("height", None)
    if depth is not None:
        params["height"] = depth
    elif h is not None:
        params["height"] = h
    elif height is not None:
        params["height"] = height
    else:
        params["height"] = 0.3

    if params.get("concate", False) or params.get("concatenate", False):
        params["text"] = _abbreviate_text(params.get("text", ""))

    params.setdefault("type", "positive")
    params.setdefault("size", 7)
    params.setdefault("font", "Candara:Light")
    params.setdefault("valign", "center")
    params.setdefault("halign", "center")

    # Keep the zero/default case byte-for-byte compatible with the historic
    # plain text component.  In particular, do not wrap it in a Minkowski
    # operation with a zero-radius circle: OpenSCAD treats that as additional
    # geometry and it makes ordinary text needlessly expensive to render.
    minkowski_radius = params.get(
        "minkowski_radius", params.get("minkowski", 0)
    )
    try:
        minkowski_radius = float(minkowski_radius)
    except (TypeError, ValueError):
        minkowski_radius = 0
    minkowski_radius = max(0, minkowski_radius)
    params.pop("minkowski", None)
    if minkowski_radius > 0:
        params["minkowski_radius"] = minkowski_radius
        # Return the component shape directly so opsc dispatches to render().
        # A direct dict is intentional: opsc_easy filters unknown parameters.
        params["shape"] = "oobb_text"
        return [params]

    params.pop("minkowski_radius", None)
    params["shape"] = "text"
    return [opsc.opsc_easy(**params)]


def render(params):
    """Render text expanded by the requested circular Minkowski radius."""
    from solid2 import circle, linear_extrude, minkowski, text

    radius = max(0, float(params.get("minkowski_radius", 0)))
    height = params.get("height", params.get("h", params.get("depth", 0.3)))
    text_keys = {
        "text", "size", "font", "halign", "valign", "spacing",
        "direction", "language", "script",
    }
    text_params = {key: value for key, value in params.items() if key in text_keys}
    text_2d = text(**text_params)
    if radius > 0:
        text_2d = minkowski()(text_2d, circle(r=radius))
    if height != 0:
        return linear_extrude(height)(text_2d)
    return text_2d


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
            "kwargs": {"type": "positive", "text": "OOBB", "size": 10, "depth": 1.2, "pos": [0, 0, 0]},
        },
        {
            "filename": "test_2",
            "preview_rot": [65, 0, 25],
            "kwargs": {"type": "positive", "text": "bearing_plate_set", "concate": True, "h": 1, "pos": [0, 0, 0]},
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
