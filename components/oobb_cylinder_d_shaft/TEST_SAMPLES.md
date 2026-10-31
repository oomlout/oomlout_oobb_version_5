# Test Samples

All examples use a 10 mm diameter, 12 mm long cylinder. Only `cut_d` changes.

## Sample-by-sample meaning

### Sample 1: `test_1.png`
- Intent: Uncut reference cylinder: cut_d=0 mm, remaining size 10 mm.
- preview_rot: `[55,0,25]`
- kwargs: `{"radius":5,"depth":12,"cut_d":0,"mode":"true"}`

### Sample 2: `test_2.png`
- Intent: Shallow D-flat: cut_d=1 mm, remaining flat-to-back size 9 mm.
- preview_rot: `[55,0,25]`
- kwargs: `{"radius":5,"depth":12,"cut_d":1,"mode":"true"}`

### Sample 3: `test_3.png`
- Intent: Deeper D-flat: cut_d=2 mm, remaining flat-to-back size 8 mm.
- preview_rot: `[55,0,25]`
- kwargs: `{"radius":5,"depth":12,"cut_d":2,"mode":"true"}`

### Sample 4: `test_4.png`
- Intent: Half cylinder: cut_d=5 mm reaches the centreline, remaining size 5 mm.
- preview_rot: `[55,0,25]`
- kwargs: `{"radius":5,"depth":12,"cut_d":5,"mode":"true"}`

## Folder-specific notes
- Notes: cut_d is a distance removed in millimetres, not a fraction or the remaining width. The flat faces +Y before rotation; zz defaults to center. Regenerate previews with `python -c "from components.oobb_cylinder_d_shaft.working import test; test()"`.
