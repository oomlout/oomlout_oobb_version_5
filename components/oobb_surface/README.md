# oobb_surface

**OOBB Geometry Primitives: Surface**

Creates an OpenSCAD heightmap surface from an image, normalizing the source to 1000 pixels wide and scaling width, height, and relief depth in millimeters.

The source PNG is resized into the same directory as the generated SCAD module, and the SCAD references that local PNG by filename only.

## Variables

| Name | Description | Type | Default |
|------|-------------|------|---------|
| file | Image file to turn into an OpenSCAD surface. image is accepted as an alias. | string | "icon.png" |
| image | Alias for file. | string |  |
| width | Surface width in mm. If height is omitted, the image aspect ratio sets height. | number |  |
| height | Surface height in mm. If width is omitted, the image aspect ratio sets width. | number |  |
| depth | Relief depth in mm, mapped from OpenSCAD surface's 0..100 height range. | number | 1 |
| pos | 3-element [x,y,z] position. | list | [0,0,0] |
| rot | Rotation [rx,ry,rz] in degrees. | list | [0,0,0] |
| zz | Z anchor point: bottom, top, center/middle. | string | "bottom" |
| slice_bottom | Subtract a cube to slice away the background; invert=false slices the bottom, invert=true slices the top. | bool | True |
| center | Center the OpenSCAD surface around the origin in X/Y. | bool | True |
| invert | OpenSCAD surface invert flag. True makes darker pixels higher. | bool | True |
| convexity | OpenSCAD surface convexity. | number | 10 |
| type | Geometry type: positive or negative. | string | "positive" |
| m | OpenSCAD modifier prefix, e.g. #, %, *. | string | "" |

## Category

OOBB Geometry Primitives
