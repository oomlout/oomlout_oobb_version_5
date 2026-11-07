"""Reproducible CAD-based presentation renders. Run with Blender --background --python.
All dimensions in source are millimetres; scene geometry is converted to metres.
"""
import bpy, math, json, sys
from pathlib import Path
from mathutils import Matrix, Vector
from bpy_extras.object_utils import world_to_camera_view

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'presentation'
CONFIG=json.loads((OUT/'project.json').read_text(encoding='utf-8'))
GEOMETRY=CONFIG['geometry']
assert GEOMETRY['span_mm']==335.01 and GEOMETRY['clip_mm']==7 and GEOMETRY['nut_cover_mm']==7, 'Update renderer transforms when changing the axial stack'
assert GEOMETRY['bolt_mm']==25 and GEOMETRY['coupler_mm']==18 and GEOMETRY['rod_mm']==300
for folder in ('raw','scenes','qa'):(OUT/folder).mkdir(parents=True,exist_ok=True)
SHOT=sys.argv[sys.argv.index('--')+1] if '--' in sys.argv else 'parts'
PREVIEW='--preview' in sys.argv
bpy.ops.wm.read_factory_settings(use_empty=True)
scene=bpy.context.scene
scene.render.engine='CYCLES'
scene.cycles.samples=24 if PREVIEW else 96
scene.cycles.use_denoising=True
try:
    pref=bpy.context.preferences.addons['cycles'].preferences
    pref.compute_device_type='OPTIX'; pref.refresh_devices()
    if any(d.type=='OPTIX' for d in pref.devices):
        for d in pref.devices: d.use=d.type=='OPTIX'
        scene.cycles.device='GPU'
except Exception: pass
scene.render.resolution_x=1500 if PREVIEW else 2400
scene.render.resolution_y=1250 if PREVIEW else 2000
scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'
scene.render.film_transparent=False
scene.world=bpy.data.worlds.new('Warm studio')
scene.world.use_nodes=True
scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.78,.84,1,1)
scene.world.node_tree.nodes['Background'].inputs[1].default_value=.38
scene.view_settings.view_transform='AgX'
scene.view_settings.look='AgX - Medium High Contrast'
scene.unit_settings.system='METRIC'
scene.unit_settings.length_unit='MILLIMETERS'

def material(name,hexstr,rough=.4,metal=0):
    c=[int(hexstr[i:i+2],16)/255 for i in (0,2,4)]
    c=[v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in c]
    m=bpy.data.materials.new(name);m.use_nodes=True
    p=m.node_tree.nodes.get('Principled BSDF')
    p.inputs['Base Color'].default_value=(*c,1)
    p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal
    return m
black=material('All printed parts | satin black','121212',.39)
flange=material('Generic narrow reel | charcoal plastic','242629',.36)
card=material('Recycled fibre reel','AA8C63',.76)
teal=material('OOBB turquoise | 00B1B7','00B1B7',.36)
yellow=material('OOBB sunflower | FEC601','FEC601',.37)
dark=material('Black filament','202124',.35)
white=material('White shelf laminate','E9E7E1',.43)
paper=material('Warm white studio floor','EEEAE1',.72)
steel=material('Zinc plated steel','AAB1BA',.27,.82)
labelmat=material('Reel label paper','F2EFE6',.8)

def V(p):return Vector(p)*.001
def finish(o,name,mat):
    o.name=name;o.data.materials.append(mat);return o
def bevel(o,w=.45):
    b=o.modifiers.new('Small real edge highlights','BEVEL');b.width=w*.001;b.segments=3
    b=o.modifiers.new('Weighted normals','WEIGHTED_NORMAL');b.keep_sharp=True
    return o
def cube(name,loc,size,mat,b=.5):
    bpy.ops.mesh.primitive_cube_add(size=1,location=V(loc));o=bpy.context.object
    o.dimensions=V(size);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    finish(o,name,mat)
    if b:bevel(o,b)
    return o
def cyl(name,loc,r,depth,mat,axis='X',n=96):
    bpy.ops.mesh.primitive_cylinder_add(vertices=n,radius=r*.001,depth=depth*.001,location=V(loc))
    o=bpy.context.object
    if axis=='X':o.rotation_euler[1]=math.pi/2
    if axis=='Y':o.rotation_euler[0]=math.pi/2
    finish(o,name,mat)
    for f in o.data.polygons:f.use_smooth=len(f.vertices)==4
    return o
def ring(name,loc,ro,ri,length,mat,n=128,axis='X'):
    vs=[];fs=[]
    for xx,rr in [(-length/2,ro),(length/2,ro),(-length/2,ri),(length/2,ri)]:
        for i in range(n):
            a=2*math.pi*i/n;vs.append((xx*.001,rr*math.cos(a)*.001,rr*math.sin(a)*.001))
    for i in range(n):
        j=(i+1)%n
        fs.extend([(i,j,n+j,n+i),(2*n+i,3*n+i,3*n+j,2*n+j),(i,2*n+i,2*n+j,j),(n+i,n+j,3*n+j,3*n+i)])
    me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update()
    o=bpy.data.objects.new(name,me);scene.collection.objects.link(o);o.location=V(loc)
    if axis=='Z':o.rotation_euler[1]=-math.pi/2
    finish(o,name,mat)
    for f in me.polygons:f.use_smooth=f.index%4<2
    return o

cache={}
def cad(part,name,loc=(0,0,0),rot=None):
    if part not in cache:
        bpy.ops.wm.stl_import(filepath=str(ROOT/'scad_output'/part/'3dpr.stl'))
        o=bpy.context.object;o.data.transform(Matrix.Scale(.001,4));o.data.materials.clear();o.data.materials.append(black)
        cache[part]=o.data;bpy.data.objects.remove(o,do_unlink=True)
    o=bpy.data.objects.new(name,cache[part]);scene.collection.objects.link(o);o.location=V(loc)
    if rot is not None:o.rotation_euler=rot
    bevel(o,.15)
    return o
SHORT='side_10_width_3_height_9_mm_depth_short_extra'
TALL='side_10_width_8_height_9_mm_depth_short_extra'
def spacer(length,loc,extra='',reverse=False,name='Printed sleeve'):
    part='spacer_1_width_1_height_'+str(length).replace('.','_')+'_mm_depth'+('_'+extra+'_extra' if extra else '')
    # Align every hex pocket with the side-frame pockets, including reversed sleeves.
    rot=Matrix(((0,0,-1),(1,0,0),(0,-1,0))) if reverse else Matrix(((0,0,1),(1,0,0),(0,1,0)))
    return cad(part,name,loc,rot.to_euler())

def thread(name,x,y,z,length):
    cyl(name+' core',(x,y,z),2.48,length,steel)
    # 1 mm pitch, continuous steel crest. A visual thread, not manufacturing geometry.
    cu=bpy.data.curves.new(name+' helical crest','CURVE');cu.dimensions='3D';cu.resolution_u=1;cu.bevel_depth=.24*.001;cu.bevel_resolution=2
    sp=cu.splines.new('POLY');n=int(length*14);sp.points.add(n)
    for i in range(n+1):
        t=i/n;xx=x-length/2+t*length;a=t*length*2*math.pi
        sp.points[i].co=(*(V((xx,y+2.72*math.cos(a),z+2.72*math.sin(a)))),1)
    o=bpy.data.objects.new(name,cu);scene.collection.objects.link(o);cu.materials.append(steel)

def spool(x,y,z,col,index=0):
    # Narrow generic non-Bambu reel: 200 mm diameter x 60 mm overall width.
    shell=card if index in (1,4) else flange
    ring('Reel %d | hollow hub'%index,(x,y,z),42,26,56,shell)
    ring('Reel %d | wound filament'%index,(x,y,z),91,42,52,col)
    for sign in (-1,1):
        o=ring('Reel %d | side flange'%index,(x+sign*28.5,y,z),100,26,3,shell)
        bevel(o,.4)
        # Recessed rim and hub rings give the side faces definition.
        ring('Reel flange outer bead',(x+sign*30.1,y,z),98,96,.45,shell)
        ring('Reel hub reinforcement',(x+sign*30.2,y,z),36,26,.5,shell)
    # Fine turns catch highlights across the filament's front edge.
    for j in range(53):
        xx=x-25.5+j*.98
        ring('Wound filament turn',(xx,y,z),91.35,90.95,.48,col,n=96)
    # Small unbranded material tag on the visible flange.
    cube('Plain reel stock label',(x+30.4,y-53,z+47),(.28,38,19),labelmat,.1)

def refill(x,y,z,col,index=0):
    # Refill coil with an open centre and retaining straps; no reel / flanges / hub.
    ring('Refill %d | spool-free filament coil'%index,(x,y,z),100,47,58,col)
    for j in range(59):
        ring('Refill winding',(x-28.5+j*.98,y,z),100.35,99.95,.48,col,n=96)
    for a in (0,2*math.pi/3,4*math.pi/3):
        ca,sa=math.cos(a),math.sin(a)
        for r in (46.5,100.7):
            o=cube('Refill retaining band',(x,y+r*ca,z+r*sa),(60,1.1,4),flange,.2)
            o.rotation_euler[0]=a
        for xx in (x-29.5,x+29.5):
            o=cube('Refill band over coil face',(xx,y+73.6*ca,z+73.6*sa),(1.1,54.2,4),flange,.2)
            o.rotation_euler[0]=a

def shelf(n=1):
    inner=335;thin=16;outer=41
    width=n*inner+(n-1)*thin+2*outer
    depth=390
    for x in (-width/2+outer/2,width/2-outer/2):
        cube('KALLAX outer side',(x,0,width/2),(outer,depth,width),white,1.1)
    for z in (outer/2,width-outer/2):
        cube('KALLAX outer top / bottom',(0,0,z),(width-2*outer,depth,outer),white,1.1)
    for i in range(1,n):
        z=outer+i*inner+(i-1)*thin+thin/2
        cube('KALLAX horizontal divider',(0,0,z),(width-2*outer,depth,thin),white,.7)
        x=-width/2+outer+i*inner+(i-1)*thin+thin/2
        cube('KALLAX vertical divider',(x,0,width/2),(thin,depth,width-2*outer),white,.7)
    return width,outer

def lighting(target,size):
    # Large softboxes relative to the subject keep black plastic readable.
    for name,delta,power,scale in [('Key',(-.65,-.8,1.2),750,1),('Fill',(.8,-.35,.65),480,.8),('Rim',(.15,.8,1.05),900,.75)]:
        bpy.ops.object.light_add(type='AREA',location=V(target)+Vector(delta)*size)
        l=bpy.context.object;l.name=name;l.data.energy=power*size*size*.035;l.data.shape='DISK';l.data.size=scale*size
        l.rotation_euler=(V(target)-l.location).to_track_quat('-Z','Y').to_euler()
def camera(target,offset,scale):
    bpy.ops.object.camera_add(location=V(target)+V(offset));o=bpy.context.object
    o.rotation_euler=(V(target)-o.location).to_track_quat('-Z','Y').to_euler();o.data.type='ORTHO';o.data.ortho_scale=scale*.001;o.data.lens=50
    scene.camera=o

def parts_scene():
    cad(SHORT,'Short side frame',(-100,0,1))
    cad(TALL,'Tall side frame',(80,40,1))
    for k,(length,extra) in enumerate([(99.67,'one_end_nut'),(67.67,'one_end_nut'),(18,'full_nut'),(7,'full_nut'),(9,'slotted')]):
        spacer(length,([-180,-60,40,90,130][k],-100,9),extra)
    camera((0,-5,10),(350,-520,650),445)
    lighting((0,0,0),.65)

def coupling(x,y,z,length=18,name=None):
    # M6 coupling nut, render assumption: 18 mm long, 10 mm across flats.
    o=ring(name or ('M6 coupling nut' if length==18 else 'M6 captive fixed-end nut'),(x,y,z),10/math.sqrt(3),2.55,length,steel,n=96)
    for v in list(o.data.vertices)[:192]:
        a=math.atan2(v.co.z,v.co.y)
        r=.005/math.cos((a+math.pi/6)%(math.pi/3)-math.pi/6)
        v.co.y=r*math.cos(a);v.co.z=r*math.sin(a)
    o.rotation_euler[0]=math.pi/6  # hex vertices match the source pocket orientation
    bevel(o,.2)
    return o

def rail(cx,y,z,explode=0,expose=False):
    # 4 frames + 3 long sleeves + 18 mm coupling housing + 7 mm clip + 7 mm nut cover.
    # The fixed nut and adjusting bolt head are both seated in OUTWARD-facing pockets.
    a=cx-167.505
    thread('M6 x 300 mm threaded rod',a+150,y,z,300)
    if not expose:
        spacer(99.67,(a+9-explode*2,y,z),'one_end_nut',name='A | 99.67 mm sleeve')
        spacer(67.67,(a+117.67,y,z),'one_end_nut',name='B | 67.67 mm sleeve')
        spacer(99.67,(a+294.01+explode*2,y,z),'one_end_nut',True,name='A | 99.67 mm sleeve')
        spacer(18,(a+294.01+explode*3,y,z),'full_nut',name='C | 18 mm coupling housing')
        clip=spacer(7,(a+312.01+explode*4,y,z),'slotted',name='D | 7 mm slip-on cover')
        clip.rotation_euler=Matrix(((0,0,1),(-1,0,0),(0,-1,0))).to_euler()  # slot down
        spacer(7,(a+319.01+explode*5,y,z),'full_nut',name='E | 7 mm retaining nut cover')
    coupling(a+2.5-explode*4,y,z,5)
    coupling(a+303.01+explode*3,y,z)
    coupling(a+323.51+explode*5,y,z,5,name='M6 adjustment bolt retaining nut')
    adjustment_bolt(a+330.01+explode*6,y,z)

def adjustment_bolt(under_head,y,z,length=25):
    thread('M6 x 25 adjustment bolt',under_head-length/2,y,z,length)
    head=cyl('Adjustment bolt | 4 mm hex head',(under_head+2,y,z),10/math.sqrt(3),4,steel,n=6)
    head.rotation_euler=SIDE_ROT
    bevel(head,.18)

SIDE_ROT=Matrix(((0,0,1),(1,0,0),(0,1,0))).to_euler()
END_ROT=Matrix(((0,0,-1),(-1,0,0),(0,1,0))).to_euler()
def cradle(cx=0,cy=0,bz=0,tall=False,explode=0):
    h=119 if tall else 44; up=59.5 if tall else 22
    z=bz+(112 if tall else 37)
    for i,xx in enumerate((0,108.67,185.34,335.01)):
        x=cx-167.505+xx+(-3,-1,1,5)[i]*explode
        cad(TALL if tall else SHORT,'Tall side frame' if tall else 'Short side frame',(x,cy,bz+up),END_ROT if i==3 else SIDE_ROT)
    for y in (-67.5,67.5):rail(cx,cy+y,z,explode)

def hardware_scene():
    scene.render.resolution_y=690 if PREVIEW else 1100
    cradle(explode=12)
    camera((5,0,30),(460,-700,430),570);lighting((0,0,25),.85)

def rail_scene():
    scene.render.resolution_y=560 if PREVIEW else 900
    # Parts separated on the rail axis; one coupling, two ordinary nuts per rail.
    thread('M6 x 300 mm threaded rod',-30,0,80,300)
    coupling(-206,-15,30,5)
    spacer(99.67,(-185,-15,30),'one_end_nut')
    spacer(67.67,(-65,-15,30),'one_end_nut')
    spacer(99.67,(122,-15,30),'one_end_nut',True)
    spacer(18,(147,-15,30),'full_nut')
    coupling(190,-15,30)
    spacer(7,(218,-15,30),'slotted')
    spacer(7,(239,-15,30),'full_nut')
    coupling(263,-15,30,5,name='M6 adjustment bolt retaining nut')
    adjustment_bolt(314,-15,30)
    camera((38,-10,47),(260,-1000,510),690);lighting((0,0,40),.85)

def adjust_scene():
    scene.render.resolution_y=656 if PREVIEW else 1050
    # A physically aligned exploded detail of the captive coupling and bolt.
    spacer(99.67,(0,0,0),'one_end_nut',True)
    coupling(22,0,0)
    spacer(18,(43,0,0),'full_nut')
    spacer(7,(72,0,0),'slotted')
    spacer(7,(91,0,0),'full_nut')
    coupling(113,0,0,5,name='M6 adjustment bolt retaining nut')
    cad(SHORT,'End frame | outward-facing bolt recess',(140,67.5,-15),END_ROT)
    adjustment_bolt(175,0,0)
    thread('Rod end enters coupling',-42,0,0,114)
    for obj in list(scene.objects):
        if obj.type in ('MESH','CURVE'):obj.location.z+=.045
    camera((42,20,50),(230,-440,210),350);lighting((10,0,45),.5)

def empty_scene():
    cradle()
    cradle(0,187,0,True)
    camera((0,85,70),(450,-700,470),540);lighting((0,85,70),.9)

def printed_scene():
    empty_scene()
    for obj in scene.objects:
        if obj.type in ('MESH','CURVE') and steel in list(obj.data.materials):
            obj.hide_render = True

def fixed_end_scene():
    a=-167.505
    cad(SHORT,'First short frame',(a,0,22),SIDE_ROT)
    for y in (-67.5,67.5):
        thread('M6 x 300 mm threaded rod',a+150,y,37,300)
        coupling(a+2.5,y,37,5)
    scene.render.resolution_y=1400
    camera((-10,0,25),(430,-650,390),440);lighting((0,0,25),.7)

def sleeves_scene():
    cradle()
    # Leave the first three frames, both rods, fixed nuts and long sleeves.
    for obj in scene.objects:
        if obj.type not in ('MESH','CURVE'):continue
        keep=(obj.name.startswith(('A |','B |','M6 x 300','M6 captive fixed')) or
              (obj.name.startswith('Short side frame') and obj.location.x < .1))
        obj.hide_render=not keep
    scene.render.resolution_y=1400
    camera((0,0,25),(430,-650,390),440);lighting((0,0,25),.7)

def coupling_scene():
    spacer(99.67,(0,0,0),'one_end_nut',True)
    thread('Rod end',-30,0,0,90)
    coupling(35,0,0)
    spacer(18,(65,0,0),'full_nut')
    for obj in scene.objects:
        if obj.type in ('MESH','CURVE'):obj.location.z+=.025
    scene.render.resolution_y=1250
    camera((-15,0,25),(160,-420,180),230);lighting((-15,0,25),.45)

if SHOT=='parts':parts_scene()
elif SHOT=='exploded':hardware_scene()
elif SHOT=='rail':rail_scene()
elif SHOT=='empty':empty_scene()
elif SHOT=='printed':printed_scene()
elif SHOT=='step-fixed':fixed_end_scene()
elif SHOT=='step-sleeves':sleeves_scene()
elif SHOT=='step-coupling':coupling_scene()
elif SHOT=='adjust':adjust_scene()
elif SHOT=='cabinet':
    w,b=shelf(4)
    for cell,colset in [((1,1),(teal,yellow,dark,teal,yellow)),((2,2),(yellow,teal,dark,yellow,teal))]:
        c,r=cell;cx=-w/2+b+c*351+167.5;bz=b+r*351
        cradle(cx,-93.5,bz)
        cradle(cx,93.5,bz,True)
        for i,col in enumerate(colset):
            spool(cx+(i-2)*62,-93.5,bz+120.01,col,i)
            refill(cx+(i-2)*62,93.5,bz+195.01,colset[4-i],i)
    camera((0,0,w*.49),(1500,-4600,1300),2250);lighting((0,0,w*.5),2.7)
elif SHOT=='cell':
    w,b=shelf(1)
    cradle(0,-93.5,b)
    cradle(0,93.5,b,True)
    cols=(teal,yellow,dark,teal,yellow)
    for i,col in enumerate(cols):
        spool((i-2)*62,-93.5,b+120.01,col,i)
        refill((i-2)*62,93.5,b+195.01,cols[4-i],i)
    camera((0,-20,214),(260,-1000,220),740);lighting((0,0,210),.85)
elif SHOT=='loaded':
    cradle(0,-93.5)
    cradle(0,93.5,0,True)
    cols=(teal,yellow,dark,teal,yellow)
    for i,col in enumerate(cols):
        spool((i-2)*62,-93.5,120.01,col,i)
        refill((i-2)*62,93.5,195.01,cols[4-i],i)
    camera((0,0,140),(450,-800,470),540);lighting((0,0,130),.9)
else:raise ValueError(SHOT)
cube('Studio floor',(0,0,-10),(20000,20000,20),paper,0)
scene.render.filepath=f'//../raw/{SHOT}.png'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'scenes'/f'{SHOT}.blend'),relative_remap=False)
bpy.ops.render.render(write_still=True)
