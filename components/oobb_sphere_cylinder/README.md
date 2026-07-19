# oobb_sphere_cylinder

**OOBB Geometry Primitives: Sphere Cylinder**

OOBB cylinder wrapper that can emit either a normal `cylinder` or the rounded `sphere_cylinder` shape.

## Returns

List of geometry component dicts.

## Variables

| Name | Description | Type | Default |
|------|-------------|------|---------|
| pos | 3-element [x,y,z] position. | list | [0,0,0] |
| depth | Cylinder height in mm. | number | 250 |
| radius_name | Named radius for mode-aware lookup. | string | "" |
| radius | Explicit radius in mm. | number | 0 |
| radius_rounded | Rounded edge radius in mm for sphere_cylinder style. | number | 1 |
| style | Output style: sphere_cylinder or cylinder. | string | "sphere_cylinder" |
| zz | Z anchor point: center, bottom, top. | string | "center" |
| mode | Render modes: laser, 3dpr, true. | list | ["laser","3dpr","true"] |

## Sample Notes

show rounded, plain cylinder, and radius_name usage.
