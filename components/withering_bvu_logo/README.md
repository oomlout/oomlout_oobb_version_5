# withering_bvu_logo

**Withering Building Volume as Utility Logo**

Rounded-square badge component using the Building Volume as Utility (BVU)
geometric SVG. The black logo regions are subtracted from the top face, making
the component suitable for a shallow recess or a contrasting-colour inlay.

The OpenSCAD import uses the local `image_scad.svg`, normalised to a 1 mm square
and containing only the original vector paths; the source SVG's white background
rectangle is intentionally omitted.

## Variables

| Name | Description | Type | Default |
|------|-------------|------|---------|
| size | Outer square side length in mm. | number | 50 |
| depth | Badge depth in mm. | number | 3 |
| depth_engraving | Logo cut depth in mm. | number | 1.5 |
| corner_radius | Plan-view corner radius in mm. | number | 4 |
| radius_rounded | Top and bottom perimeter edge radius in mm. | number | 0 |
| logo_size_percent | Logo canvas width as a fraction of badge size. | number | 0.82 |
| pos | 3-element `[x,y,z]` position. | list | `[0,0,0]` |
| rot | Rotation `[rx,ry,rz]` in degrees. | list | `[0,0,0]` |
| zz | Z anchor point: bottom, center/middle, top. | string | `"bottom"` |
