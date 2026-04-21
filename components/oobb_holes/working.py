import copy
import math
import os
import sys
import oobb

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)


d = {}


def describe():
    global d
    d = {}
    d["name"] = 'oobb_holes'
    d["name_long"] = 'OOBB Geometry Helpers: Hole Array'
    d["description"] = 'Places OOBB-grid-aligned screw holes across a rectangular or circular area using named hole patterns.'
    d["category"] = 'OOBB Geometry Helpers'
    d["shape_aliases"] = ['oobb_holes']
    d["returns"] = 'List of geometry component dicts.'
    v = []
    v.append({"name": 'holes', "description": 'Hole pattern(s): all, perimeter, perimeter_miss_middle, u, top, bottom, left, right, corners, single, missing_middle, just_middle, circle.', "type": 'list', "default": '["all"]'})
    v.append({"name": 'width', "description": 'Width in OOBB grid units.', "type": 'number', "default": 0})
    v.append({"name": 'height', "description": 'Height in OOBB grid units.', "type": 'number', "default": 0})
    v.append({"name": 'pos', "description": '3-element [x,y,z] position.', "type": 'list', "default": '[0,0,0]'})
    v.append({"name": 'depth', "description": 'Hole depth in mm.', "type": 'number', "default": 100})
    v.append({"name": 'radius_name', "description": 'Named radius key, e.g. m6, m3.', "type": 'string', "default": '"m6"'})
    v.append({"name": 'middle', "description": 'Include the centre hole.', "type": 'bool', "default": True})
    v.append({"name": 'size', "description": 'Grid spacing scale: oobb or oobe.', "type": 'string', "default": '"oobb"'})
    v.append({"name": 'both_holes', "description": 'Also add matching oobe half-grid holes.', "type": 'bool', "default": False})
    v.append({"name": 'circle', "description": 'Filter holes to lie inside a circle boundary.', "type": 'bool', "default": False})
    v.append({"name": 'diameter', "description": 'Diameter in OOBB units (overrides width/height).', "type": 'number', "default": 0})
    v.append({"name": 'diameter_clearance', "description": 'Clearance from circle edge (mm) when circle=True.', "type": 'number', "default": 7.5})
    v.append({"name": 'diameter_center_clearance', "description": 'Minimum distance from centre to include hole (mm).', "type": 'number', "default": 0})
    v.append({"name": 'loc', "description": 'Grid location(s) [x,y] for single pattern.', "type": 'list', "default": '[0,0]'})
    d["variables"] = v
    return d


def define():
    global d
    if not isinstance(d, dict) or not d:
        describe()
    defined_variable = {}
    defined_variable.update(d)
    return defined_variable


def _get_oobe_holes(**kwargs):
    """Inner helper â€” places half-grid (oobe) holes. Mirrors get_oobe_holes from the legacy codebase."""
    objects = []
    modes = ["laser", "3dpr", "true"]
    width = kwargs.get("width", 0)
    height = kwargs.get("height", 0)
    middle = kwargs.get("middle", True)
    pos = list(kwargs.get("pos", [0, 0, 0]))
    holes = kwargs.get("holes", ["all"])
    radius_name = kwargs.get("radius_name", "m3")
    depth = kwargs.get("depth", 100)
    diameter_center_clearance = kwargs.get("diameter_center_clearance", 0)
    m = kwargs.get("m", "")
    x = pos[0]
    y = pos[1]
    z = pos[2]

    circle = kwargs.get("circle", False)
    diameter = kwargs.get("diameter", 0)
    diameter_clearance = kwargs.get("diameter_clearance", 1.5)
    if diameter != 0:
        width = diameter
        height = diameter

    if not isinstance(holes, list):
        holes = [holes]

    for hole in holes:
        for mode in modes:
            xx = x
            yy = y
            ospe = oobb.gv("osp") / 2
            if hole == "all":
                if not circle:
                    pos_start = [
                        x + -(width * ospe / 2) + ospe / 2,
                        y + -(height * ospe / 2) + ospe / 2,
                        z,
                    ]
                    objects.extend(
                        oobb.oobb_easy_array(
                            type="negative",
                            shape="hole",
                            inclusion=mode,
                            repeats=[width, height],
                            pos_start=pos_start,
                            shift_arr=[ospe, ospe],
                            r=oobb.gv("hole_radius_m3", mode),
                        )
                    )
                else:
                    acceptable_holes = []
                    spacing = 7.5
                    pos_start = [
                        xx + -(width * spacing / 2) + spacing / 2,
                        yy + -(height * spacing / 2) + spacing / 2,
                        z,
                    ]
                    for w in range(0, math.floor(width)):
                        for h in range(0, math.floor(height)):
                            hx = pos_start[0] + w * spacing
                            hy = pos_start[1] + h * spacing
                            r = width * spacing / 2 - diameter_clearance
                            dist = math.sqrt(hx ** 2 + hy ** 2)
                            if dist <= r:
                                if middle or dist > 15:
                                    if dist >= diameter_center_clearance:
                                        acceptable_holes.append([w, h])
                    for m2 in modes:
                        for ah in acceptable_holes:
                            hx = pos_start[0] + ah[0] * spacing
                            hy = pos_start[1] + ah[1] * spacing
                            objects.extend(
                                oobb.oobb_easy(
                                    type="negative",
                                    shape="oobb_hole",
                                    pos=[hx, hy, 0],
                                    radius_name=radius_name,
                                    m=m,
                                )
                            )
    return objects


def action(**kwargs):
    import oobb
    import opsc
    """Place OOBB-grid screw holes across a widthÃ—height area using named patterns."""
    objects = []
    modes = ["laser", "3dpr", "true"]

    width = kwargs.get("width", 0)
    height = kwargs.get("height", 0)
    pos = list(kwargs.get("pos", [0, 0, 0]))
    depth = kwargs.get("depth", 100)
    radius_name = kwargs.get("radius_name", "m6")
    middle = kwargs.get("middle", True)
    size = kwargs.get("size", "oobb")
    both_holes = kwargs.get("both_holes", False)
    circle = kwargs.get("circle", False)
    diameter_full = int(kwargs.get("diameter", 0))
    diameter = diameter_full
    diameter_clearance = kwargs.get("diameter_clearance", 7.5)
    diameter_center_clearance = kwargs.get("diameter_center_clearance", 0)
    m = kwargs.get("m", "")

    if diameter_full % 1 != 0:
        diameter = diameter_full - diameter_full % 1
    if diameter != 0:
        width = diameter
        height = diameter

    holes = kwargs.get("holes", ["all"])
    if not isinstance(holes, list):
        holes = [holes]
    if isinstance(holes, bool):
        holes = ["all"] if holes else ["none"]

    x = pos[0]
    y = pos[1]
    z = pos[2]
    xx = x
    yy = y

    spacing = oobb.gv("osp")
    if size == "oobe":
        spacing = oobb.gv("osp") / 2

    if "all" in holes:
        if not circle:
            for mode in modes:
                pos_start = [
                    xx + -(width * spacing / 2) + spacing / 2,
                    yy + -(height * spacing / 2) + spacing / 2,
                    z,
                ]
                objects.extend(
                    oobb.oobb_easy_array(
                        type="negative",
                        shape="hole",
                        inclusion=mode,
                        repeats=[width, height],
                        pos_start=pos_start,
                        shift_arr=[spacing, spacing],
                        middle=middle,
                        r=oobb.gv(f"hole_radius_{radius_name}", mode),
                    )
                )
        else:
            if diameter != 0:
                width = diameter
                height = diameter
            acceptable_holes = []
            pos_start = [
                xx + -(width * spacing / 2) + spacing / 2,
                yy + -(height * spacing / 2) + spacing / 2,
                z,
            ]
            for w in range(0, math.floor(width)):
                for h in range(0, math.floor(height)):
                    hx = pos_start[0] + w * spacing
                    hy = pos_start[1] + h * spacing
                    r = width * spacing / 2 - diameter_clearance
                    if math.sqrt(hx ** 2 + hy ** 2) <= r:
                        if w == math.floor(width / 2) and h == math.floor(height / 2) and not middle:
                            pass
                        else:
                            if math.sqrt(hx ** 2 + hy ** 2) >= diameter_center_clearance:
                                acceptable_holes.append([w, h])
            for mode in modes:
                for ah in acceptable_holes:
                    hx = pos_start[0] + ah[0] * spacing
                    hy = pos_start[1] + ah[1] * spacing
                    objects.extend(
                        oobb.oobb_easy(
                            type="negative",
                            shape="oobb_hole",
                            pos=[hx, hy, 0],
                            radius_name=radius_name,
                            m=m,
                        )
                    )

    if "perimeter" in holes:
        pos_start = [
            xx + -(width * spacing / 2) + spacing / 2,
            yy + -(height * spacing / 2) + spacing / 2,
            0,
        ]
        for w in range(0, int(width)):
            for h in range(0, int(height)):
                if w == 0 or w == width - 1 or h == 0 or h == height - 1:
                    hx = pos_start[0] + w * spacing
                    hy = pos_start[1] + h * spacing
                    objects.extend(
                        oobb.oobb_easy(
                            type="negative", shape="oobb_hole", pos=[hx, hy, 0], radius_name=radius_name, m=m
                        )
                    )

    if "perimeter_miss_middle" in holes:
        pos_start = [
            xx + -(width * spacing / 2) + spacing / 2,
            yy + -(height * spacing / 2) + spacing / 2,
            0,
        ]
        for w in range(0, int(width)):
            for h in range(0, int(height)):
                if w == 0 or w == width - 1 or h == 0 or h == height - 1:
                    hx = pos_start[0] + w * spacing
                    hy = pos_start[1] + h * spacing
                    w_test = math.floor(width / 2)
                    h_test = math.floor(height / 2)
                    if h != h_test and w != w_test:
                        objects.extend(
                            oobb.oobb_easy(
                                type="negative", shape="oobb_hole", pos=[hx, hy, 0], radius_name=radius_name, m=m
                            )
                        )

    if "u" in holes:
        pos_start = [
            xx + -(width * spacing / 2) + spacing / 2,
            yy + -(height * spacing / 2) + spacing / 2,
            0,
        ]
        for w in range(0, int(width)):
            for h in range(0, int(height)):
                if w == 0 or w == width - 1 or h == 0:
                    hx = pos_start[0] + w * spacing
                    hy = pos_start[1] + h * spacing
                    objects.extend(
                        oobb.oobb_easy(
                            type="negative", shape="oobb_hole", pos=[hx, hy, 0], radius_name=radius_name, m=m
                        )
                    )

    if "top" in holes:
        pos_start = [
            xx + -(width * spacing / 2) + spacing / 2,
            yy + -(height * spacing / 2) + spacing / 2,
            z,
        ]
        for w in range(0, int(width)):
            for h in range(0, int(height)):
                if w == 0:
                    hx = pos_start[0] + w * spacing
                    hy = pos_start[1] + h * spacing
                    objects.extend(
                        oobb.oobb_easy(
                            type="negative", shape="oobb_hole", pos=[hx, hy, z], radius_name=radius_name, m=m, depth=depth
                        )
                    )

    if "bottom" in holes:
        pos_start = [
            xx + -(width * spacing / 2) + spacing / 2,
            yy + -(height * spacing / 2) + spacing / 2,
            z,
        ]
        for w in range(0, int(width)):
            for h in range(0, int(height)):
                if w == width - 1:
                    hx = pos_start[0] + w * spacing
                    hy = pos_start[1] + h * spacing
                    objects.extend(
                        oobb.oobb_easy(
                            type="negative", shape="oobb_hole", pos=[hx, hy, z], radius_name=radius_name, m=m, depth=depth
                        )
                    )

    if "right" in holes:
        pos_start = [
            xx + -(width * spacing / 2) + spacing / 2,
            yy + -(height * spacing / 2) + spacing / 2,
            z,
        ]
        for w in range(0, int(width)):
            for h in range(0, int(height)):
                if h == height - 1:
                    hx = pos_start[0] + w * spacing
                    hy = pos_start[1] + h * spacing
                    objects.extend(
                        oobb.oobb_easy(
                            type="negative", shape="oobb_hole", pos=[hx, hy, z], radius_name=radius_name, m=m, depth=depth
                        )
                    )

    if "left" in holes:
        pos_start = [
            xx + -(width * spacing / 2) + spacing / 2,
            yy + -(height * spacing / 2) + spacing / 2,
            z,
        ]
        for w in range(0, int(width)):
            for h in range(0, int(height)):
                if h == 0:
                    hx = pos_start[0] + w * spacing
                    hy = pos_start[1] + h * spacing
                    objects.extend(
                        oobb.oobb_easy(
                            type="negative", shape="oobb_hole", pos=[hx, hy, z], radius_name=radius_name, m=m, depth=depth
                        )
                    )

    if "bottom_bottom" in holes:
        pos_start = [
            xx + -(width * spacing / 2) + spacing / 2,
            yy + -(height * spacing / 2) + spacing / 2,
            0,
        ]
        for w in range(0, int(width)):
            for h in range(0, int(height)):
                if w == width - 1:
                    hx = pos_start[0] + w * spacing
                    hy = pos_start[1] + h * spacing
                    objects.extend(
                        oobb.oobb_easy(
                            type="negative", shape="oobb_hole", pos=[hx, hy, 0], radius_name=radius_name, m=m, depth=depth
                        )
                    )

    if "circle" in holes:
        pos_start = [
            xx + -(width * spacing / 2) + spacing / 2,
            yy + -(height * spacing / 2) + spacing / 2,
            0,
        ]
        circle_dif = kwargs.get("circle_dif", 0)
        for w in range(0, math.floor(width)):
            for h in range(0, math.floor(height)):
                hx = pos_start[0] + w * spacing
                hy = pos_start[1] + h * spacing
                r = ((width * spacing) - circle_dif) / 2
                if math.sqrt(hx ** 2 + hy ** 2) <= r:
                    if w == math.floor(width / 2) and h == math.floor(height / 2) and not middle:
                        pass
                    else:
                        objects.extend(
                            oobb.oobb_easy(
                                type="negative", shape="oobb_hole", pos=[hx, hy, 0], radius_name=radius_name, m=m
                            )
                        )

    if "corners" in holes or "corner" in holes:
        pos_start = [
            xx + -(width * spacing / 2) + spacing / 2,
            yy + -(height * spacing / 2) + spacing / 2,
            0,
        ]
        for w in range(0, int(width)):
            for h in range(0, int(height)):
                if (w == 0 and h == 0) or (w == 0 and h == height - 1) or \
                   (w == width - 1 and h == 0) or (w == width - 1 and h == height - 1):
                    hx = pos_start[0] + w * spacing
                    hy = pos_start[1] + h * spacing
                    objects.extend(
                        oobb.oobb_easy(
                            type="negative", shape="oobb_hole", pos=[hx, hy, 0], radius_name=radius_name, m=m
                        )
                    )

    if "single" in holes:
        locs = kwargs.get("loc", [0, 0])
        if locs == [0, 0]:
            locs = kwargs.get("location", [0, 0])
        if locs == [0, 0]:
            locs = kwargs.get("locations", [0, 0])
        if locs == [0, 0]:
            locs = kwargs.get("positions", [0, 0])
        if not isinstance(locs[0], list):
            locs = [locs]
        pos_start = [
            xx + -(width * spacing / 2) + spacing / 2,
            yy + -(height * spacing / 2) + spacing / 2,
            0,
        ]
        for loc in locs:
            hx = pos_start[0] + (loc[0] - 1) * spacing
            hy = pos_start[1] + (loc[1] - 1) * spacing
            objects.extend(
                oobb.oobb_easy(
                    type="negative", shape="oobb_hole", pos=[hx, hy, z], radius_name=radius_name, m=m, depth=depth
                )
            )

    if "missing_middle" in holes:
        pos_start = [
            xx + -(width * spacing / 2) + spacing / 2,
            yy + -(height * spacing / 2) + spacing / 2,
            0,
        ]
        for w in range(0, int(width)):
            for h in range(0, int(height)):
                if not (w == math.floor(width / 2) and h == math.floor(height / 2)):
                    hx = pos_start[0] + w * spacing
                    hy = pos_start[1] + h * spacing
                    objects.extend(
                        oobb.oobb_easy(
                            type="negative", shape="oobb_hole", pos=[hx, hy, 0], radius_name=radius_name, m=m
                        )
                    )

    if "just_middle" in holes:
        objects.extend(
            oobb.oobb_easy(type="negative", shape="oobb_hole", pos=[0, 0, 0], radius_name=radius_name, m=m)
        )

    if both_holes:
        p2 = copy.deepcopy(kwargs)
        p2["shape"] = "oobe_hole"
        p2["radius_name"] = "m3"
        p2["width"] = width * 2 - 1
        p2["height"] = height * 2 - 1
        if diameter != diameter_full:
            p2["diameter"] = (diameter_full + 0.5) * 2 - 1
        else:
            if diameter != 0:
                p2["diameter"] = diameter_full * 2 - 1
        p2["holes"] = holes
        objects.extend(_get_oobe_holes(**p2))

    return objects


def test():
    import copy
    import os
    import opsc

    folder = os.path.dirname(os.path.abspath(__file__))
    test_dir = os.path.join(folder, "test")
    os.makedirs(test_dir, exist_ok=True)

    samples = [{'filename': 'test_1',
      'preview_rot': [60, 0, 25],
      'kwargs': {'holes': ['all'],
                 'width': 3,
                 'height': 2,
                 'pos': [0, 0, 0],
                 'depth': 6,
                 'radius_name': 'm3',
                 'both_holes': False}},
     {'filename': 'test_2',
      'preview_rot': [60, 0, 25],
      'kwargs': {'holes': ['circle'],
                 'circle': True,
                 'diameter': 3,
                 'pos': [0, 0, 0],
                 'depth': 6,
                 'radius_name': 'm3'}}]

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


