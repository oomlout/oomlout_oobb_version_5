# patreon_logo

**Patreon Logo Badge**

Circular or rounded-square badge with the Patreon logo subtracted from the top face for engraving or colour inlay.

## Returns

List of geometry component dicts.

## Variables

| Name | Description | Type | Default |
|------|-------------|------|---------|
| size | Outer diameter / square side length in mm. | number | 50.0 |
| depth | Badge depth in mm. | number | 3.0 |
| depth_engraving | Logo cut depth in mm. | number | 1.5 |
| body_shape | Badge outline: 'rounded_square' or 'circle'. | string | "rounded_square" |
| corner_radius | Plan-view corner radius in mm (rounded_square only). | number | 4.0 |
| radius_rounded | Top and bottom perimeter edge radius in mm; zero keeps square edges. | number | 0.0 |
| logo_size_percent | Logo width as a fraction of the badge size. | number | 0.82 |
| logo_shift | 2-element [x,y] shift of the logo engraving in mm. | list | [0,0] |
| pos | 3-element [x,y,z] position. | list | [0,0,0] |
| rot | Rotation [rx,ry,rz] in degrees. | list | [0,0,0] |
| zz | Z anchor point: bottom, center/middle, top. | string | "bottom" |
