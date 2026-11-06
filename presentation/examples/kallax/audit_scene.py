"""Read-only Blender audit of counts, source meshes and captive hardware positions.
blender --background --python-exit-code 1 --python presentation/scripts/audit_scene.py
"""
import bpy,json
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2]
P=ROOT/'presentation'
data=json.loads((P/'project.json').read_text(encoding='utf-8'))
report={}
for shot,multiplier in [('cell',1),('empty',1),('loaded',1),('cabinet',2)]:
    bpy.ops.wm.open_mainfile(filepath=str(P/'scenes'/f'{shot}.blend'))
    objects=list(bpy.context.scene.objects)
    expected={'Short side frame':4,'Tall side frame':4,'M6 coupling nut':4,
              'M6 captive fixed-end nut':4,'M6 adjustment bolt retaining nut':4,
              'Adjustment bolt |':4,'M6 x 300 mm threaded rod core':4,
              'D | 7 mm slip-on cover':4,'E | 7 mm retaining nut cover':4}
    counts={name:sum(o.name.startswith(name) for o in objects) for name in expected}
    assert all(counts[n]==expected[n]*multiplier for n in expected),(shot,counts)
    if multiplier==1:
        positions={'Adjustment bolt |':(162.505,166.505),
                   'M6 captive fixed-end nut':(-167.505,-162.505),
                   'M6 adjustment bolt retaining nut':(153.505,158.505),
                   'D | 7 mm slip-on cover':(144.505,151.505),
                   'E | 7 mm retaining nut cover':(151.505,158.505)}
        for prefix,(lo,hi) in positions.items():
            for obj in objects:
                if obj.name.startswith(prefix):
                    xs=[(obj.matrix_world@Vector(v)).x*1000 for v in obj.bound_box]
                    assert abs(min(xs)-lo)<.02 and abs(max(xs)-hi)<.02,(obj.name,xs)
    report[shot]=counts
g=data['geometry'];stack=g['axial_stack']
assert abs(sum(b-a for _,a,b in stack)-g['span_mm'])<1e-6
assert all(abs(stack[i][2]-stack[i+1][1])<1e-6 for i in range(len(stack)-1))
assert g['clip_mm']+g['nut_cover_mm']==14
report['status']='PASS'
report['scope']='Counts, nominal stack and axial bounds. This is not a physical fit or load test.'
(P/'qa/scene-audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('PASS: 4 short + 4 tall, 4 couplings, 8 ordinary nuts, 4 bolts, 4 rods, 4 of each 7 mm cover per cell')
