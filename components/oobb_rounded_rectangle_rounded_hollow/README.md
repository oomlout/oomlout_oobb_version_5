# oobb_rounded_rectangle_rounded_hollow

**OOBB Geometry Primitives: Hollow Rounded Rectangle with Rounded Edges**

Hollow rounded rectangle with rounded outer top and bottom edges. Optional depth_top and depth_bottom values add solid end caps; zero keeps that end open. The default edge radius is half the wall thickness so the edge is covered by the bead.

## Returns

List containing positive outer and negative inner rounded-rectangle geometry.

## Variables

| Name | Description | Type | Default |
|------|-------------|------|---------|
| pos | 3-element [x,y,z] position. | list | [0,0,0] |
| type | Geometry type: p/positive or n/negative. | string | p |
| size | Outer [x,y,z] dimensions in mm. | list | [30,20,8] |
| radius | Plan-view corner radius of the outer shape. | number | 5 |
| radius_rounded | Outer top and bottom edge rounding radius in mm; defaults to half wall_thickness. | number | 0.6 |
| wall_thickness | Side wall thickness in mm; also offsets the inner corner and edge radii. | number | 1.2 |
| depth_top | Solid top cap thickness in mm; zero leaves the top open. | number | 0 |
| depth_bottom | Solid bottom cap thickness in mm; zero leaves the bottom open. | number | 0 |
| rot | Rotation [rx,ry,rz] in degrees. | list | [0,0,0] |
| rot_x | X rotation in degrees. | number | 0 |
| rot_y | Y rotation in degrees. | number | 0 |
| rot_z | Z rotation in degrees. | number | 0 |

## Sample Notes

zero cap depths leave a through-tube; positive depths add solid end caps. The outer roundover defaults to half the wall thickness, leaving the inner top edge square beneath the bead.
