# Cylinder SVG inlay

Use `oobb.append_full(thing, shape="oobb_cylinder_inlay", radius=26,
depth=45, svg="markings.svg", inlay_depth=.84, part="base")`.
Repeat with `part="inlay"` using **identical parameters and transforms** for the
second colour STL. `part="combined"` previews teal and yellow.

Artwork goes on the flat end faces, flush with the original envelope. Use
`inlay_face="both"` for both ends and optionally `svg_bottom` for different
opposite-face lettering. Each SVG is viewed from outside its face; the bottom
orientation is handled automatically. `mirror=True` reflects the artwork in
that view. This does not wrap artwork around the curved cylinder wall.

Use physical SVG dimensions in mm, filled closed paths and outlined text.
`svg_center` defaults to true; `svg_scale`, `svg_rotate` and `svg_offset` place
the artwork before extrusion. OpenSCAD imports SVG vector geometry, not colour.
`inlay=False` returns an undecorated cylinder. `zz` applies locally before
`rot` and `pos`, including for horizontal cylinders.

`body_components` optionally supplies an existing OOBB body in the same local
coordinates. The accent is intersected with that body, retaining its holes,
pockets and fits. Use an axial envelope matching the body's outer faces.
Both colour volumes are complementary with zero assembly gap: print them as
one multipart object, not as separately glued inserts. STL stores geometry;
assign filament colours in the slicer.
