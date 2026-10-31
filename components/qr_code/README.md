# qr_code

**QR Code**

QR code geometry generated from a data string. Dark modules are extruded to the requested depth; use as a positive for a raised code or as a negative to engrave it into a face.

## Returns

List of geometry component dicts.

## Variables

| Name | Description | Type | Default |
|------|-------------|------|---------|
| data | Text or URL the QR code encodes. | string | "https://www.patreon.com" |
| size | Overall square size in mm including the quiet-zone border. | number | 30.0 |
| depth | Extrusion depth of the dark modules in mm. | number | 1.5 |
| border | Quiet-zone width in modules kept clear around the code. | number | 2 |
| error_correction | QR error correction level: l, m, q, or h. | string | "m" |
| pos | 3-element [x,y,z] position. | list | [0,0,0] |
| rot | Rotation [rx,ry,rz] in degrees. | list | [0,0,0] |
| zz | Z anchor point: bottom, center/middle, top. | string | "bottom" |
