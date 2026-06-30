import copy
import csv
import io
import os
import re
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

_BEARING_DATA_DIR = os.path.join(_PROJECT_ROOT, "data", "bearing")
_DEFAULT_BEARING_HEADER = [
    "Size",
    "Inner Dimension",
    "Outer Dimension",
    "Width",
    "Dynamic(Cr)",
    "Static(Cor)",
    "Weight(lb)",
]

_BEARING_LOOKUP = None

d = {}


def describe():
    global d
    d = {}
    d["name"] = "oobb_bearing"
    d["name_long"] = "OOBB Mechanical Shapes: Bearing Lookup"
    d["description"] = "Lookup a bearing size from the CSV data in data/bearing and emit a matching opsc bearing object."
    d["category"] = "OPSC Mechanical Shapes"
    d["shape_aliases"] = ["oobb_bearing"]
    d["returns"] = "List of geometry component dicts."
    v = []
    v.append({"name": "pos", "description": "3-element [x,y,z] position.", "type": "list", "default": "[0,0,0]"})
    v.append({"name": "rot", "description": "Rotation [rx,ry,rz] in degrees.", "type": "list", "default": "[0,0,0]"})
    v.append({"name": "type", "description": "Geometry type: positive or negative.", "type": "string", "default": '"positive"'})
    v.append({"name": "bearing_size", "description": "Bearing size key from the CSV files, for example 606, 6701, MR104, or 60_22.", "type": "string", "default": '"606"'})
    v.append({"name": "clearance", "description": "Clearance passed through to the legacy opsc bearing object as clearance_bearing.", "type": "number", "default": 0})
    d["variables"] = v
    return d


def define():
    global d
    if not isinstance(d, dict) or not d:
        describe()
    defined_variable = {}
    defined_variable.update(d)
    return defined_variable


def _normalize_key(value):
    if value is None:
        return ""
    return re.sub(r"[^a-z0-9]+", "", str(value).strip().lower())


def _coerce_number(value, default=None):
    if value is None:
        return default
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip()
    if text == "" or text == "-":
        return default
    try:
        return float(text)
    except ValueError:
        return default


def _extract_csv_lines(raw_text):
    fenced = re.search(r"```(?:csv)?\s*(.*?)```", raw_text, flags=re.IGNORECASE | re.DOTALL)
    if fenced:
        raw_text = fenced.group(1)

    lines = []
    for line in raw_text.splitlines():
        stripped = line.strip()
        if not stripped or "," not in stripped:
            continue
        lines.append(stripped)
    return lines


def _parse_bearing_csv(path):
    with open(path, "r", encoding="utf-8-sig") as handle:
        raw_text = handle.read()

    lines = _extract_csv_lines(raw_text)
    if not lines:
        return []

    first_row = next(csv.reader([lines[0]]))
    has_header = bool(first_row) and first_row[0].strip().lower() == "size"
    buffer = io.StringIO("\n".join(lines))

    if has_header:
        reader = csv.DictReader(buffer)
        return [row for row in reader if row]

    reader = csv.reader(buffer)
    rows = []
    for raw_row in reader:
        if not raw_row:
            continue
        row = {}
        for index, header in enumerate(_DEFAULT_BEARING_HEADER):
            if index < len(raw_row):
                row[header] = raw_row[index].strip()
        rows.append(row)
    return rows


def _pick_width(row):
    for key in ("Width", "Width ZZ/2RS", "Width OPEN"):
        width = _coerce_number(row.get(key))
        if width is not None:
            return width
    return None


def _build_bearing_lookup():
    lookup = {}
    if not os.path.isdir(_BEARING_DATA_DIR):
        return lookup

    for filename in sorted(os.listdir(_BEARING_DATA_DIR)):
        if not filename.lower().endswith(".csv"):
            continue
        path = os.path.join(_BEARING_DATA_DIR, filename)
        for row in _parse_bearing_csv(path):
            bearing_size = row.get("Size") or row.get("size")
            key = _normalize_key(bearing_size)
            if not key:
                continue

            lookup[key] = {
                "bearing_size": str(bearing_size).strip(),
                "id": _coerce_number(row.get("Inner Dimension")),
                "od": _coerce_number(row.get("Outer Dimension")),
                "depth": _pick_width(row),
                "source_file": filename,
                "raw_row": row,
            }
    return lookup


def _get_bearing_spec(bearing_size):
    global _BEARING_LOOKUP
    if _BEARING_LOOKUP is None:
        _BEARING_LOOKUP = _build_bearing_lookup()

    lookup_key = _normalize_key(bearing_size)
    if lookup_key not in _BEARING_LOOKUP:
        available = sorted(spec["bearing_size"] for spec in _BEARING_LOOKUP.values())
        preview = ", ".join(available[:12])
        raise ValueError(f"Unknown bearing_size {bearing_size!r}. Available examples: {preview}")

    return copy.deepcopy(_BEARING_LOOKUP[lookup_key])


def action(**kwargs):
    import opsc

    params = copy.deepcopy(kwargs)
    bearing_size = params.pop("bearing_size", params.pop("bearing", params.pop("bearing_type", "")))
    if bearing_size in ("", None):
        raise ValueError("bearing_size is required")

    bearing_spec = _get_bearing_spec(bearing_size)

    clearance = _coerce_number(params.pop("clearance", 0), default=0)
    params.setdefault("type", "positive")
    params["shape"] = "bearing"
    params["id"] = bearing_spec["id"]/2
    params["od"] = bearing_spec["od"]/2
    params["depth"] = bearing_spec["depth"]
    #params["clearance_bearing"] = clearance

    params.pop("raw_row", None)
    params.pop("source_file", None)

    return [opsc.opsc_easy(**params)]


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
            "preview_rot": [45, 0, 25],
            "kwargs": {"type": "positive", "bearing_size": "606", "clearance": 0, "pos": [0, 0, 0]},
        },
        {
            "filename": "test_2",
            "preview_rot": [45, 0, 25],
            "kwargs": {"type": "positive", "bearing_size": "6701", "clearance": 0, "pos": [0, 0, 0]},
        },
        {
            "filename": "test_3",
            "preview_rot": [45, 0, 25],
            "kwargs": {"type": "positive", "bearing_size": "MR104", "clearance": 0.5, "pos": [0, 0, 0]},
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

        preview_rot = sample["preview_rot"]
        wrapped = components
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

        sample_dir = os.path.join(test_dir, sample["filename"])
        os.makedirs(sample_dir, exist_ok=True)
        scad_path = os.path.join(sample_dir, "working.scad")
        png_path = os.path.join(sample_dir, "image.png")

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

