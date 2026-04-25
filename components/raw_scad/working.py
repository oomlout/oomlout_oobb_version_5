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
    d["name"] = "raw_scad"
    d["name_long"] = "OPSC Composite Shapes: Raw SCAD"
    d["description"] = "Imports or inlines raw OpenSCAD modules through the component system."
    d["category"] = "OPSC Composite Shapes"
    d["shape_aliases"] = ["raw_scad"]
    d["returns"] = "List of geometry component dicts."
    d["variables"] = []
    return d


def define():
    global d
    if not d:
        describe()
    defined = {}
    defined.update(d)
    return defined


def action(**kwargs):
    import opsc

    params = copy.deepcopy(kwargs)
    params.setdefault("type", "positive")
    params["shape"] = "raw_scad"
    return [opsc.opsc_easy(**params)]


def _write_raw_scad_source(source, module_name, cache_dir=None):
    import hashlib

    cache_root = cache_dir or os.path.join(_PROJECT_ROOT, "_raw_scad_cache")
    os.makedirs(cache_root, exist_ok=True)
    digest = hashlib.sha256(source.encode("utf-8")).hexdigest()[:16]
    filename = os.path.join(cache_root, f"{module_name}_{digest}.scad")
    with open(filename, "w", encoding="utf-8") as handle:
        handle.write(source)

    # Keep a stable friendly filename in output caches so normalized `use <...>`
    # lines always point at the current source rather than an older stale file.
    friendly_filename = os.path.join(cache_root, f"{module_name}.scad")
    with open(friendly_filename, "w", encoding="utf-8") as handle:
        handle.write(source)

    if cache_dir is not None:
        return friendly_filename
    return filename


def render(params):
    from solid2 import import_scad

    source = params.get("source", "")
    filename = params.get("file", "")
    module_name = params.get("module", "main")
    module_kwargs = params.get("module_kwargs", {})
    cache_dir = params.get("cache_dir", None)

    if source:
        filename = _write_raw_scad_source(source, module_name, cache_dir=cache_dir)
    if not filename:
        raise ValueError("raw_scad requires either 'source' or 'file'.")

    scad_object = import_scad(filename)
    module_fn = getattr(scad_object, module_name, None)
    if module_fn is None:
        raise ValueError(f"raw_scad module '{module_name}' not found in {filename}")

    result = module_fn(**module_kwargs)
    if cache_dir is not None:
        basename = os.path.basename(filename)
        result.include_file_path = basename
        result.include_string = f"use <{basename}>\n"
    return result


def test():
    import copy
    import os
    import opsc

    folder = os.path.dirname(os.path.abspath(__file__))
    test_dir = os.path.join(folder, "test")
    os.makedirs(test_dir, exist_ok=True)

    samples = [{'filename': 'test_1',
      'preview_rot': [35, 0, 25],
      'kwargs': {'type': 'positive',
                 'source': 'module main(){cube([12,12,12], center=true);}',
                 'module': 'main',
                 'pos': [0, 0, 0]}},
     {'filename': 'test_2',
      'preview_rot': [35, 0, 25],
      'kwargs': {'type': 'positive',
                 'source': 'module main(){difference(){cube([20,12,6], center=true); '
                           'translate([0,0,0]) cube([10,6,8], center=true);}}',
                 'module': 'main',
                 'pos': [0, 0, 0]}}]

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


