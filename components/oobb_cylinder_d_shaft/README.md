# oobb_cylinder_d_shaft

**OOBB Geometry Primitives: D-Shaft Cylinder**

Cylinder with a flat cut from the +Y side. cut_d is the material removed in mm; the remaining flat-to-back size is 2 * radius - cut_d.

## Returns

List of mode-specific rotation objects containing a cylinder minus a flat cut.

## Variables

| Name | Description | Type | Default |
|------|-------------|------|---------|
| radius | Cylinder radius in mm; r is an alias. Supply a radius, diameter, or radius_name. | number | (required unless diameter or radius_name is supplied) |
| diameter | Cylinder diameter in mm; d is an alias. Explicit radius takes precedence. | number | (optional) |
| radius_name | Mode-aware OOBB radius lookup, used when no explicit radius or diameter is supplied. | string |  |
| cut_d | Depth removed from the +Y curved edge in mm. Flat is at y = radius - cut_d before rotation. Must satisfy 0 <= cut_d < 2 * radius; 0 leaves a full cylinder. | number | 1 |
| depth | Cylinder length along local Z in mm (aliases: depth_mm, h). May be an OOBB dimension name. | number or string | 250 |
| pos | Anchor position [x,y,z] in mm. | list | [0,0,0] |
| zz | Local Z anchor: center, bottom, or top, applied before rotation. | string | center |
| type | p/positive for a solid shaft; n/negative for a D-shaped hole. | string | p |
| rot | Rotation [rx,ry,rz] in degrees about pos. Alternatively use rot_x, rot_y, rot_z. | list | [0,0,0] |
| mode | Render mode string or list: laser, 3dpr, true. | list or string | ["laser","3dpr","true"] |

## Sample Notes

cut_d is a distance removed in millimetres, not a fraction or the remaining width. The flat faces +Y before rotation; zz defaults to center. Regenerate previews with `python -c "from components.oobb_cylinder_d_shaft.working import test; test()"`.

## Usage

```python
import oobb

shaft = oobb.oobb_easy(
    shape="oobb_cylinder_d_shaft",
    type="p",
    radius=5,
    depth=12,
    cut_d=2,
    pos=[0, 0, 0],
    zz="center",
)
```

This starts with a 10 mm diameter cylinder and removes 2 mm from its +Y edge.
The flat lies at local y=3 mm, leaving 8 mm from the flat to the opposite edge.
The cylinder spans z=-6 to z=6 mm. `cut_d` stays in millimetres when the radius changes.

For a D-shaped hole, use `type="n"` and combine the returned geometry with a
positive body. The cylinder and its flat are grouped before subtraction, so the
flat cutter does not cut into surrounding parts. Use `rot=[0,0,90]` to turn the
flat toward -X, or `rot=[90,0,0]` to put the shaft axis along -Y.

Named radii resolve separately in each render mode. For example:

```python
shaft = oobb.oobb_easy(
    shape="oobb_cylinder_d_shaft",
    radius_name="hole_radius_m6",
    depth=12,
    cut_d=0.5,
    zz="bottom",
    mode="3dpr",
)
```

## Rendered examples

All four examples have radius=5 mm, depth=12 mm, zz="center", and mode="true".
The HTML documentation includes their isometric, top, and side previews and SCAD files.

| Example | cut_d (mm removed) | Flat Y (mm) | Remaining flat-to-back size (mm) |
|---------|--------------------|-------------|---------------------------------|
| test_1: full cylinder | 0 | 5 (no flat) | 10 |
| test_2: shallow flat | 1 | 4 | 9 |
| test_3: deeper flat | 2 | 3 | 8 |
| test_4: half cylinder | 5 | 0 | 5 |

## Limits

Use a positive constant radius and depth. `cut_d=0` produces an uncut cylinder;
`cut_d=radius` produces a half cylinder. Cuts deeper than the radius are allowed,
but `cut_d` must remain less than the full diameter in every requested mode.
Negative cuts, non-finite dimensions, and tapered cylinders are rejected.

## Regenerate

```powershell
python -c "from components.oobb_cylinder_d_shaft.working import test; test()"
python components/documentation.py --objects-root components --markdown
python components/documentation.py --objects-root components --json components/documentation_data.json --html-template templates/oobb_documentation_template.html --html-output components/documentation.html
```
