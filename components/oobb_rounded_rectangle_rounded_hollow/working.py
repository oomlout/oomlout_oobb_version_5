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
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_rounded_mod = _load_component("oobb_rounded_rectangle_rounded")
_rounded_rectangle_rounded = _rounded_mod.action

d = {}


def describe():
    global d
    d = {
        "name": "oobb_rounded_rectangle_rounded_hollow",
        "name_long": "OOBB Geometry Primitives: Hollow Rounded Rectangle with Rounded Edges",
        "description": "Hollow rounded rectangle with rounded outer top and bottom edges. Optional depth_top and depth_bottom values add solid end caps; zero keeps that end open. The default edge radius is half the wall thickness so the edge is covered by the bead.",
        "category": "OOBB Geometry Primitives",
        "shape_aliases": ["rounded_rectangle_rounded_hollow"],
        "returns": "List containing positive outer and negative inner rounded-rectangle geometry.",
        "variables": [
            {"name": "pos", "description": "3-element [x,y,z] position.", "type": "list", "default": "[0,0,0]"},
            {"name": "type", "description": "Geometry type: p/positive or n/negative.", "type": "string", "default": "p"},
            {"name": "size", "description": "Outer [x,y,z] dimensions in mm.", "type": "list", "default": "[30,20,8]"},
            {"name": "radius", "description": "Plan-view corner radius of the outer shape.", "type": "number", "default": 5},
            {"name": "radius_rounded", "description": "Outer top and bottom edge rounding radius in mm; defaults to half wall_thickness.", "type": "number", "default": 0.6},
            {"name": "radius_lip_inner", "description": "Inner rounding at open ends only; zero preserves the square inner lip. Requires Shapely >= 2.1.", "type": "number", "default": 0},
            {"name": "lip_opening", "description": "Optional local XY polygon of the combined cavity and channels, for continuous inner lip rounding.", "type": "list", "default": []},
            {"name": "wall_thickness", "description": "Side wall thickness in mm; also offsets the inner corner and edge radii.", "type": "number", "default": 1.2},
            {"name": "depth_top", "description": "Solid top cap thickness in mm; zero leaves the top open.", "type": "number", "default": 0},
            {"name": "depth_bottom", "description": "Solid bottom cap thickness in mm; zero leaves the bottom open.", "type": "number", "default": 0},
            {"name": "rot", "description": "Rotation [rx,ry,rz] in degrees.", "type": "list", "default": "[0,0,0]"},
            {"name": "rot_x", "description": "X rotation in degrees.", "type": "number", "default": 0},
            {"name": "rot_y", "description": "Y rotation in degrees.", "type": "number", "default": 0},
            {"name": "rot_z", "description": "Z rotation in degrees.", "type": "number", "default": 0},
        ],
    }
    return d


def define():
    if not d:
        describe()
    return dict(d)


def action(**kwargs):
    size = copy.deepcopy(kwargs.get("size", [30, 20, 8]))
    radius = kwargs.get("radius", 5)
    wall_thickness = kwargs.get("wall_thickness", 1.2)
    radius_rounded = kwargs.get("radius_rounded", wall_thickness / 2)
    radius_lip_inner = kwargs.get("radius_lip_inner", 0)
    depth_top = kwargs.get("depth_top", 0)
    depth_bottom = kwargs.get("depth_bottom", 0)
    if len(size) != 3:
        raise ValueError("size must be [width,height,depth]")
    if wall_thickness <= 0:
        raise ValueError("wall_thickness must be positive")
    if depth_top < 0 or depth_bottom < 0:
        raise ValueError("depth_top and depth_bottom must be non-negative")
    if depth_top + depth_bottom >= size[2]:
        raise ValueError("depth_top and depth_bottom must leave a hollow cavity")
    if min(size[0] - 2 * wall_thickness, size[1] - 2 * wall_thickness) <= 0:
        raise ValueError("wall_thickness leaves no inner opening")
    if not (wall_thickness < radius <= min(size[:2]) / 2):
        raise ValueError("radius must exceed wall_thickness and fit within the outer shape")
    if not (0 < radius_rounded < size[2] / 2):
        raise ValueError("radius_rounded must be positive and less than half the depth")
    if not math.isfinite(radius_lip_inner) or radius_lip_inner < 0:
        raise ValueError("radius_lip_inner must be finite and non-negative")
    if radius_lip_inner and radius_lip_inner + radius_rounded > wall_thickness + 1e-9:
        raise ValueError("Inner and outer lip radii must fit within wall_thickness")
    if radius_lip_inner and (depth_top and depth_bottom or 2*radius_lip_inner >= size[2]-depth_top-depth_bottom):
        raise ValueError("Inner lip rounding requires an open end and enough cavity depth")

    common = copy.deepcopy(kwargs)
    common["size"] = size
    common["radius"] = radius
    common["radius_rounded"] = radius_rounded
    common["wall_thickness"] = wall_thickness
    outer_kwargs = copy.deepcopy(common)
    outer_kwargs["type"] = "positive"
    outer = _rounded_rectangle_rounded(**outer_kwargs)

    inner_kwargs = copy.deepcopy(common)
    inner_kwargs["type"] = "positive"
    cavity_start = depth_bottom - (0.1 if depth_bottom == 0 else 0)
    cavity_end = size[2] - depth_top + (0.1 if depth_top == 0 else 0)
    cavity_depth = cavity_end - cavity_start
    inner_kwargs["size"] = [
        size[0] - 2 * wall_thickness,
        size[1] - 2 * wall_thickness,
        cavity_depth,
    ]
    inner_kwargs["radius"] = radius - wall_thickness
    inner_radius_rounded = max(0, radius_rounded - wall_thickness)
    inner_pos = copy.deepcopy(kwargs.get("pos", [0, 0, 0]))
    inner_rot = outer[0]["rot"]
    rx, ry, rz = [math.radians(value) for value in inner_rot]
    # Rotate the local bottom-cap offset into the same world position used by
    # the separately wrapped inner cutter.
    offset_x = cavity_start * (math.sin(ry) * math.cos(rx) * math.cos(rz) + math.sin(rx) * math.sin(rz))
    offset_y = cavity_start * (math.sin(ry) * math.cos(rx) * math.sin(rz) - math.sin(rx) * math.cos(rz))
    offset_z = cavity_start * math.cos(ry) * math.cos(rx)
    inner_pos[0] += offset_x
    inner_pos[1] += offset_y
    inner_pos[2] += offset_z
    inner_kwargs["pos"] = inner_pos
    if inner_radius_rounded > 0:
        inner_kwargs["radius_rounded"] = inner_radius_rounded
        inner = _rounded_rectangle_rounded(**inner_kwargs)
        inner = [dict(item, typetype="negative") for item in inner]
    else:
        import opsc

        inner_shape = opsc.opsc_easy(
            "positive",
            "rounded_rectangle",
            size=inner_kwargs["size"],
            r=inner_kwargs["radius"],
            pos=[0, 0, 0],
        )
        inner = [{
            "type": "rotation",
            "typetype": "negative",
            "pos": copy.deepcopy(outer[0]["pos"]),
            "rot": copy.deepcopy(outer[0]["rot"]),
            "objects": [inner_shape],
        }]

    if radius_lip_inner:
        import opsc
        from shapely.geometry import MultiPoint, Polygon

        outline = kwargs.get("lip_opening")
        if outline:
            opening = Polygon(outline)
        else:
            half_x, half_y = size[0]/2 - radius, size[1]/2 - radius
            opening = MultiPoint([(x, y) for x in (-half_x, half_x)
                                  for y in (-half_y, half_y)]).convex_hull.buffer(
                                      radius-wall_thickness, quad_segs=24)
        points, faces = make_inner_lip_mesh(opening, radius_lip_inner)
        for end in ("bottom", "top"):
            if (depth_bottom if end == "bottom" else depth_top) != 0:
                continue
            cutter_points = points
            cutter_faces = faces
            if end == "top":
                cutter_points = [[x, y, size[2]-z] for x, y, z in points]
                cutter_faces = [face[::-1] for face in faces]
            cutter = opsc.opsc_easy(
                "positive", "raw_scad", module="oobb_inner_lip_mesh",
                source="module oobb_inner_lip_mesh(points, faces) { polyhedron(points=points, faces=faces, convexity=10); }",
                module_kwargs={"points": cutter_points, "faces": cutter_faces},
            )
            inner.append({"type": "rotation", "typetype": "negative",
                          "pos": copy.deepcopy(outer[0]["pos"]),
                          "rot": copy.deepcopy(outer[0]["rot"]), "objects": [cutter]})

    requested_type = kwargs.get("type", "p")
    if requested_type in ("n", "negative"):
        return [dict(item, typetype="negative") for item in outer] + [
            dict(item, typetype="positive") for item in inner
        ]
    return outer + inner


def make_inner_lip_mesh(opening, radius, segments=16):
    """Flare one complete opening with a circular inside-edge profile.

    Triangulate each narrow annulus without convexifying the opening: a hull
    would cut straight across concave rib-channel junctions. Below the open
    end is a small overlap; above radius the normal cavity is unchanged.
    """
    from shapely import constrained_delaunay_triangles
    from shapely.geometry.polygon import orient

    if not opening.is_valid or opening.geom_type != "Polygon" or opening.interiors:
        raise ValueError("lip_opening must be one valid polygon without holes")
    rings = []
    for i in range(segments + 1):
        angle = math.pi*i/(2*segments)
        offset = radius*(1-math.sin(angle)) if i < segments else 0
        height = radius*(1-math.cos(angle))
        polygon = opening.buffer(offset, quad_segs=12).simplify(1e-10, preserve_topology=True)
        rings.append((orient(polygon, sign=1), height))

    points, faces, indices = [], [], {}

    def key(x, y):
        return round(x, 10), round(y, 10)

    def vertex(x, y, z):
        value = (*key(x, y), round(z, 10))
        if value not in indices:
            indices[value] = len(points)
            # Keep the original coordinates for coincident cavity boundaries;
            # rounding the stored vertices creates microscopic Boolean slivers.
            points.append([x, y, z])
        return indices[value]

    def triangles(polygon, heights, reverse=False):
        for triangle in constrained_delaunay_triangles(polygon).geoms:
            coords = list(orient(triangle, sign=1).exterior.coords)[:3]
            face = [vertex(x, y, heights[key(x, y)]) for x, y in coords]
            faces.append(face[::-1] if reverse else face)

    base = rings[0][0]
    bottom = -0.02
    triangles(base, {key(x, y): bottom for x, y in base.exterior.coords}, reverse=True)
    coords = list(base.exterior.coords)
    for (ax, ay), (bx, by) in zip(coords, coords[1:]):
        a, b = vertex(ax, ay, bottom), vertex(bx, by, bottom)
        c, d = vertex(bx, by, 0), vertex(ax, ay, 0)
        faces.extend([[a, b, c], [a, c, d]])
    for (outer_ring, low), (inner_ring, high) in zip(rings, rings[1:]):
        heights = {key(x, y): low for x, y in outer_ring.exterior.coords}
        heights.update({key(x, y): high for x, y in inner_ring.exterior.coords})
        triangles(outer_ring.difference(inner_ring), heights)
    top, height = rings[-1]
    triangles(top, {key(x, y): height for x, y in top.exterior.coords})
    # OpenSCAD uses clockwise faces when viewed from outside.
    return points, [face[::-1] for face in faces]


def test():
    import os
    import opsc

    folder = os.path.dirname(os.path.abspath(__file__))
    test_dir = os.path.join(folder, "test")
    os.makedirs(test_dir, exist_ok=True)
    samples = [
        {
            "filename": "test_1",
            "preview_rot": [0, 0, 0],
            "kwargs": {"pos": [0, 0, 0], "type": "positive", "size": [30, 20, 8], "radius": 5, "wall_thickness": 1.2, "rot": [0, 0, 0]},
        },
        {
            "filename": "test_2",
            "preview_rot": [0, 0, 0],
            "kwargs": {"pos": [0, 0, 0], "type": "positive", "size": [36, 24, 10], "radius": 6, "wall_thickness": 0.8, "rot": [0, 0, 0]},
        },
        {
            "filename": "test_3",
            "preview_rot": [0, 0, 0],
            "kwargs": {"pos": [0, 0, 0], "type": "positive", "size": [30, 20, 8], "radius": 5, "wall_thickness": 1.2, "depth_top": 1.5, "rot": [0, 0, 0]},
        },
        {
            "filename": "test_4",
            "preview_rot": [0, 0, 0],
            "kwargs": {"pos": [0, 0, 0], "type": "positive", "size": [30, 20, 8], "radius": 5, "wall_thickness": 1.2, "depth_top": 1.2, "depth_bottom": 1.2, "rot": [0, 0, 0]},
        },
    ]

    generated_files = []
    for sample in samples:
        components = action(**copy.deepcopy(sample["kwargs"]))
        wrapped = components
        if sample["preview_rot"] != [0, 0, 0]:
            wrapped = [{
                "type": "rotation",
                "typetype": "positive",
                "pos": [0, 0, 0],
                "rot": sample["preview_rot"],
                "objects": components,
            }]
        sample_dir = os.path.join(test_dir, sample["filename"])
        os.makedirs(sample_dir, exist_ok=True)
        scad_path = os.path.join(sample_dir, "working.scad")
        opsc.opsc_make_object(
            scad_path,
            wrapped,
            mode="true",
            save_type="none",
            overwrite=True,
            render=True,
        )
        opsc.save_preview_images(scad_path, sample_dir)
        generated_files.append(os.path.join(sample_dir, "image.png"))
    return generated_files
