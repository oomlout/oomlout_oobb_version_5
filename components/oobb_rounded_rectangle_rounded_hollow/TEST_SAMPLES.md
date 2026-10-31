# Test Samples

## Samples

### Sample 1: `test_1`
- Intent: hollow rounded rectangle with a standard wall.
- preview_rot: `[0, 0, 0]`
- kwargs: `{'pos': [0, 0, 0], 'type': 'positive', 'size': [30, 20, 8], 'radius': 5, 'wall_thickness': 1.2, 'rot': [0, 0, 0]}`
- Implementation rule: the default edge radius is half the wall thickness (0.6 mm); the inner top edge stays square so the outer bead covers it.

### Sample 2: `test_2`
- Intent: thin-wall hollow rounded rectangle.
- preview_rot: `[0, 0, 0]`
- kwargs: `{'pos': [0, 0, 0], 'type': 'positive', 'size': [36, 24, 10], 'radius': 6, 'wall_thickness': 0.8, 'rot': [0, 0, 0]}`
- Implementation rule: the default edge radius is half the wall thickness (0.4 mm); the inner top edge stays square so the outer bead covers it.

### Sample 3: `test_3`
- Intent: tube with a 1.5 mm solid top cap.
- preview_rot: `[0, 0, 0]`
- kwargs: `{'pos': [0, 0, 0], 'type': 'positive', 'size': [30, 20, 8], 'radius': 5, 'wall_thickness': 1.2, 'depth_top': 1.5, 'rot': [0, 0, 0]}`
- Implementation rule: the cavity ends below the top face, leaving a solid cap equal to depth_top.

### Sample 4: `test_4`
- Intent: tube with solid top and bottom caps.
- preview_rot: `[0, 0, 0]`
- kwargs: `{'pos': [0, 0, 0], 'type': 'positive', 'size': [30, 20, 8], 'radius': 5, 'wall_thickness': 1.2, 'depth_top': 1.2, 'depth_bottom': 1.2, 'rot': [0, 0, 0]}`
- Implementation rule: the cavity is inset from both ends, leaving solid caps equal to depth_top and depth_bottom.

## Folder-specific notes

- Notes: zero cap depths leave a through-tube; positive depths add solid end caps. The outer roundover defaults to half the wall thickness, leaving the inner top edge square beneath the bead.
