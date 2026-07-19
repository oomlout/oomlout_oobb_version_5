# withuering_wall_logo

**Withuering Wall Logo**

Circular wall logo disk using the W squared SVG. The logo is centered on the disk, scaled by `logo_size_radius_percent`, and subtracted from the top face; when `depth_engraving` is omitted, the logo cuts fully through.

The OpenSCAD import uses the local `image_scad.svg`, which is pre-centered in a 1 mm square so generated SCAD can reference a copied SVG with simple scaling.

## Variables

| Name | Description | Type | Default |
|------|-------------|------|---------|
| radius | Outer circle radius in mm. | number | 20 |
| depth | Disk depth in mm. | number | 3 |
| depth_engraving | Logo cut depth in mm. Defaults to depth for a full hollow cut. | number | (same as depth) |
| logo_size_radius_percent | Logo size as a multiple of the outer radius. | number | 0.65 |
| pos | 3-element [x,y,z] position. | list | [0,0,0] |
| rot | Rotation [rx,ry,rz] in degrees. | list | [0,0,0] |
| zz | Z anchor point: bottom, center/middle, top. | string | "bottom" |
