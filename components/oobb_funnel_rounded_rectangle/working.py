import copy


d = {}


def describe():
    global d
    d = {}
    d["name"] = "oobb_funnel_rounded_rectangle"
    d["name_long"] = "OOBB Geometry Primitives: Rounded Rectangle Funnel"
    d["description"] = "Open rounded rectangular funnel with a straight inset spout and a tapered, constant-width wall."
    d["category"] = "OOBB Geometry Primitives"
    d["shape_aliases"] = ["funnel_rounded_rectangle"]
    d["returns"] = "List containing a rotation object with positive and negative OOBB geometry."
    d["variables"] = [
        {"name": "pos", "description": "Spout-bottom position [x,y,z] in mm.", "type": "list", "default": "[0,0,0]"},
        {"name": "type", "description": "Geometry type: p/positive or n/negative.", "type": "string", "default": "p"},
        {"name": "size", "description": "Spout outer [width,height,total_depth] in mm.", "type": "list", "default": "[36,36,14]"},
        {"name": "mouth_size", "description": "Mouth outer [width,height] in mm.", "type": "list", "default": "[63,63]"},
        {"name": "spout_depth", "description": "Straight insertion depth in mm.", "type": "number", "default": 8},
        {"name": "radius", "description": "Spout outer corner radius in mm.", "type": "number", "default": 4},
        {"name": "mouth_radius", "description": "Mouth outer corner radius in mm.", "type": "number", "default": 8},
        {"name": "wall_thickness", "description": "Horizontal wall thickness in mm.", "type": "number", "default": 1.5},
        {"name": "rot", "description": "Rotation [rx,ry,rz] in degrees.", "type": "list", "default": "[0,0,0]"},
    ]
    return d


def define():
    if not d:
        describe()
    return dict(d)


def action(**kwargs):
    import opsc

    size = copy.deepcopy(kwargs.get("size", [36, 36, 14]))
    mouth_size = copy.deepcopy(kwargs.get("mouth_size", [63, 63]))
    spout_depth = kwargs.get("spout_depth", 8)
    radius = kwargs.get("radius", 4)
    mouth_radius = kwargs.get("mouth_radius", 8)
    wall_thickness = kwargs.get("wall_thickness", 1.5)
    pos = copy.deepcopy(kwargs.get("pos", [0, 0, 0]))
    rot = copy.deepcopy(kwargs.get("rot", ""))
    if rot == "":
        rot = [kwargs.get("rot_x", 0), kwargs.get("rot_y", 0), kwargs.get("rot_z", 0)]
    typ = kwargs.get("type", "p")
    slice_depth = 0.2

    if len(size) != 3 or len(mouth_size) != 2:
        raise ValueError("size must be [width,height,total_depth] and mouth_size must be [width,height]")
    if wall_thickness <= 0 or spout_depth <= slice_depth or size[2] <= spout_depth + slice_depth:
        raise ValueError("wall_thickness and spout_depth must be positive; total depth must exceed spout depth")
    if min(size[:2] + mouth_size) <= 2 * wall_thickness:
        raise ValueError("wall_thickness leaves no open passage")
    if not (wall_thickness < radius <= min(size[:2]) / 2):
        raise ValueError("spout radius must exceed the wall thickness and fit the spout")
    if not (wall_thickness < mouth_radius <= min(mouth_size) / 2):
        raise ValueError("mouth radius must exceed the wall thickness and fit the mouth")
    if mouth_size[0] < size[0] or mouth_size[1] < size[1]:
        raise ValueError("mouth dimensions must be at least as large as the spout")

    # Two very thin rounded rectangles make each tapered surface.  Hull is
    # supported by the standard OOBB object format; the walls use the same
    # rounded_rectangle primitive as the existing hollow shape.
    outer_spout = opsc.opsc_easy(
        "positive", "rounded_rectangle",
        size=[size[0], size[1], spout_depth], r=radius, pos=[0, 0, 0],
    )
    outer_taper = {
        "type": "hull", "typetype": "positive", "pos": [0, 0, 0], "rot": [0, 0, 0],
        "objects": [
            opsc.opsc_easy("positive", "rounded_rectangle", size=[size[0], size[1], slice_depth], r=radius, pos=[0, 0, spout_depth - slice_depth]),
            opsc.opsc_easy("positive", "rounded_rectangle", size=[mouth_size[0], mouth_size[1], slice_depth], r=mouth_radius, pos=[0, 0, size[2] - slice_depth]),
        ],
    }
    inner_spout = opsc.opsc_easy(
        "negative", "rounded_rectangle",
        size=[size[0] - 2 * wall_thickness, size[1] - 2 * wall_thickness, spout_depth + 0.2],
        r=radius - wall_thickness, pos=[0, 0, -0.1],
    )
    inner_taper = {
        "type": "hull", "typetype": "negative", "pos": [0, 0, 0], "rot": [0, 0, 0],
        "objects": [
            opsc.opsc_easy("positive", "rounded_rectangle", size=[size[0] - 2 * wall_thickness, size[1] - 2 * wall_thickness, slice_depth], r=radius - wall_thickness, pos=[0, 0, spout_depth - slice_depth]),
            opsc.opsc_easy("positive", "rounded_rectangle", size=[mouth_size[0] - 2 * wall_thickness, mouth_size[1] - 2 * wall_thickness, slice_depth + 0.2], r=mouth_radius - wall_thickness, pos=[0, 0, size[2] - slice_depth]),
        ],
    }
    return [{
        "type": "rotation", "typetype": typ, "pos": pos, "rot": rot,
        "objects": [outer_spout, outer_taper, inner_spout, inner_taper],
    }]


def test():
    import os
    import opsc

    folder = os.path.dirname(os.path.abspath(__file__))
    test_dir = os.path.join(folder, "test", "test_1")
    os.makedirs(test_dir, exist_ok=True)
    scad_path = os.path.join(test_dir, "working.scad")
    components = action(
        type="positive", size=[36, 36, 14], mouth_size=[63, 63],
        spout_depth=8, radius=4, mouth_radius=8, wall_thickness=1.5,
        pos=[0, 0, 14], rot=[180, 0, 0],
    )
    opsc.opsc_make_object(scad_path, components, mode="3dpr", save_type="none", overwrite=True, render=False)
    return [scad_path]
