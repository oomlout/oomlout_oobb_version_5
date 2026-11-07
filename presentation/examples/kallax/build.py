"""Build the technical PDF, README, published PNGs and parts CSV.
Run from any working directory: python presentation/scripts/build.py
Use --render to regenerate the seven Blender scenes first.
"""
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import fitz
ROOT=Path(__file__).resolve().parents[2]
P=ROOT/'presentation'
sys.path.insert(0,str(Path(__file__).parent/'lib'))
from manual_layout import Manual,INK,GREY,ACCENT
from build_readme import build as build_readme

SHOTS=('cell','cabinet','loaded','empty','rail','exploded','adjust')
README_SHOTS=('printed','step-fixed','step-sleeves','step-coupling')

def publish_images():
    font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',30) if Path('C:/Windows/Fonts/segoeui.ttf').exists() else ImageFont.load_default(size=30)
    for shot in SHOTS+README_SHOTS:
        src=Image.open(P/'raw'/f'{shot}.png').convert('RGB')
        out=Image.new('RGB',(src.width,src.height+70),'white');out.paste(src,(0,0))
        ImageDraw.Draw(out).text((32,src.height+15),'AI-generated CAD illustration. Errors possible.',font=font,fill='#4B5350')
        out.save(P/'images'/f'{shot}.png',optimize=True)

def draw_section(m):
    """Axial section of the latest exact nominal setting (mm from fixed face)."""
    scale=10.7;cy=252
    def x(v):return 70+(v-280)*scale
    def section(a,b,outer,inner,color):
        m.rect(x(a),cy-outer*scale,(b-a)*scale,(outer-inner)*scale,color)
        m.rect(x(a),cy+inner*scale,(b-a)*scale,(outer-inner)*scale,color)
    plastic='#272B2A';metal='#A3AEAF'
    section(280,289.01,7,3.25,plastic)
    section(289.01,294.01,7,5.91425,plastic)
    section(294.01,312.01,7,5.91425,plastic)
    # Down-facing open slot; the lower wall is absent in this section.
    m.rect(x(312.01),cy-7*scale,7*scale,3.75*scale,plastic)
    section(319.01,326.01,7,5.91425,plastic)
    section(326.01,330.01,7,3.25,plastic)
    section(330.01,335.01,7,5.91425,plastic)
    section(294.01,312.01,5.77,3,metal)
    section(321.01,326.01,5.77,3,metal)
    m.rect(x(280),cy-2.7*scale,20*scale,5.4*scale,'#BCC4C4')
    m.rect(x(305.01),cy-2.7*scale,25*scale,5.4*scale,'#BCC4C4')
    m.rect(x(330.01),cy-5.77*scale,4*scale,11.54*scale,metal)
    for start,end in ((281,300),(306,330)):
        for v in range(start,end):m.line(x(v),cy-2.7*scale,x(v)+3,cy+2.7*scale,'#74817E',.6)
    for v in (294.01,312.01,319.01,326.01):
        m.line(x(v),cy-7*scale,x(v),cy-5.91425*scale,'#FFFFFF',1)
        if v!=312.01:m.line(x(v),cy+5.91425*scale,x(v),cy+7*scale,'#FFFFFF',1)
    m.dimension(x(294.01),x(312.01),144,'18 mm coupling')
    m.dimension(x(312.01),x(319.01),368,'7 mm clip')
    m.dimension(x(319.01),x(326.01),410,'7 mm hex cover')
    for v in (294.01,312.01):m.line(x(v),148,x(v),176,ACCENT)
    for v in (312.01,319.01):m.line(x(v),328,x(v),364,ACCENT)
    for v in (319.01,326.01):m.line(x(v),328,x(v),406,ACCENT)
    m.leader((x(323.5),cy-5.77*scale),708,157,'Retaining nut')
    m.leader((x(332),cy),708,235,'Recessed bolt head')
    m.leader((x(328),cy+5*scale),708,314,'Final frame')
    m.text(70,365,'Black: printed parts',10,color=GREY)
    m.text(70,386,'Grey: steel hardware',10,color=GREY)
    m.caption(70,433,'Figure 6.','Retaining nut against the inner frame face; bolt head seated in the outer recess.',760)

def make_pdf(data):
    m=Manual(P/'assembly-guide.pdf','KALLAX filament holders - revision 3')
    raw=lambda name:P/'raw'/f'{name}.png'
    m.page('KALLAX filament holders','Revision 3. 6 November 2026.')
    m.image(raw('cell'),85,144,730,415)
    m.caption(43,574,'Figure 1.','Five front reels. Five rear refills. Two independent holders, printed in black.',812)
    m.finish()

    m.page('Configuration','Two independent holders per cell. Four 300 mm M6 rods per complete cell.')
    m.image(raw('cabinet'),25,120,410,350)
    m.image(raw('empty'),444,120,425,350)
    m.caption(43,484,'Figure 2.','Two cells: four holders and eight rods.',365)
    m.caption(465,484,'Figure 3.','Four frames per holder. Short at the front; tall at the rear.',365)
    m.paragraph(43,555,'Nominal opening: 335 mm. Row centres: 187 mm. Rail heights: 37 / 112 mm.',810,11)
    m.finish()

    m.page('Parts list','One complete cell: 32 printed parts and 20 purchased hardware pieces. Double all quantities for two cells.')
    y=139
    for xx,label in ((43,'Ref.'),(86,'Type'),(156,'Part'),(390,'Specification'),(742,'Qty.'),(787,'MD5 alpha')):
        m.text(xx,y,label,9,True,color=GREY)
    y+=28;m.line(43,y-9,854,y-9)
    for part in data['printed_parts']+data['hardware']:
        m.text(43,y,part['ref'],10,color=GREY)
        m.text(86,y,'Print' if 'stl' in part else 'Hardware',9.5,color=GREY)
        name=part['name'].replace('M6 x 25 hex-head bolt, fully threaded','M6 x 25 hex-head bolt')
        target=part.get('url') or ('../'+part['stl'] if part.get('stl') else None)
        m.text(156,y,name,10.5,color=ACCENT if target else INK)
        spec=part['spec'].replace('25 mm under head; M6 x 1.0; DIN 933','Fully threaded; 25 mm under head')
        m.text(390,y,spec,9.5,color=GREY)
        m.text(751,y,part['quantity'],11,True)
        code=part.get('md5_6_alpha') or '-'
        m.text(787,y,code,10,True,color=ACCENT if code!='-' else GREY)
        if target:m.canvas.linkURL(target,(156,m.height-y-15,380,m.height-y+1),relative=0,thickness=0)
        if code!='-' and part.get('url'):
            m.canvas.linkURL(part.get('short_url') or part['url'],(787,m.height-y-15,854,m.height-y+1),relative=0,thickness=0)
        m.line(43,y+23,854,y+23,width=.3)
        y+=34
    m.paragraph(43,565,'Click a part name for its STL or hardware record. MD5 alpha codes link to OOMP. H2 includes fixed and retaining nuts.',810,10)
    m.finish()

    m.page('Assembly','Assemble both rails together. Repeat for the tall holder.')
    m.image(raw('exploded'),38,109,820,344)
    m.caption(43,457,'Figure 4.','Short holder, exploded.',810)
    m.step(43,507,1,'Seat the nuts','Seat H2 in the first frame. Thread in H1; keep the rod ends flush.',246)
    m.step(326,507,2,'Fit the sleeves','P3 / frame / P4 / frame / P3. Repeat on both rods.',246)
    m.step(609,507,3,'Fit the couplings','Insert H3 into P5. Thread onto H1 to approximately 6 mm engagement.',246)
    m.finish()

    m.page('Adjustment','One coupling and one retained bolt per rail.')
    m.image(raw('adjust'),30,108,840,300)
    m.caption(43,413,'Figure 5.','H3 coupling / P5 housing / P7 clip / P6 cover / H2 nut / frame / H4 bolt.',810)
    m.step(43,470,4,'Fit the bolts','Face the final pockets outward. Insert H4. Add H2 loosely; slide P6 onto each bolt.',246)
    m.step(326,470,5,'Set the width','Thread H4 into H3. Seat the heads. Slide P6 aside; tighten H2 against the frame; replace P6.',246)
    m.step(609,470,6,'Fit the clips','Clip P7 between P5 and P6. Keep both end fasteners recessed.',246)
    m.paragraph(43,596,'Release the bolt head from its recess before turning it.',810,9.5,GREY)
    m.finish()

    m.page('Dimensions','Axial dimensions from the fixed-end face. Millimetres.')
    draw_section(m)
    m.line(43,485,854,485)
    m.text(43,504,'335.01 mm overall',16,True)
    m.paragraph(43,532,'4 x 9 mm frames + 267.01 mm long sleeves + 18 mm coupling housing + 7 mm slotted cover + 7 mm nut cover.',390,10.5)
    m.text(483,504,'M6 x 25 mm adjustment bolt',16,True)
    m.paragraph(483,532,'Bearing face at 330.01 mm. Bolt tip at 305.01 mm: 7 mm nominal coupling engagement and 5.01 mm tip clearance. Rod engagement is 5.99 mm.',370,10.5)
    m.paragraph(43,598,'Nominal span: 335.01 mm. Measure the cell before setting the bolts.',810,9.5,GREY)
    m.finish()

    m.page('Installation','Tall holder at the rear. Short holder at the front.')
    m.image(raw('loaded'),25,118,480,380)
    m.caption(43,511,'Figure 7.','Generic reels: 200 mm diameter x 60 mm width. Five at 62 mm centres occupy 308 mm. Rear refills: 200 mm diameter x 58 mm width, with retaining straps fitted.',430)
    y=124
    for n,title,body in [
     (1,'Set the width','Fit the holders without spreading the cabinet sides. Seat the nuts and bolt heads.'),
     (2,'Position the holders','Seat all feet on the shelf. Set the row centres approximately 187 mm apart.'),
     (3,'Load the rolls','Load strapped rear refills, then front reels. Leave clearance between rolls.')]:
        y=m.step(541,y,n,title,body,310)
    m.paragraph(43,591,'Part links and source files: see the repository README.',810,9.5,GREY)
    m.finish();m.save()

def export_pages():
    doc=fitz.open(P/'assembly-guide.pdf')
    for i,page in enumerate(doc):
        pix=page.get_pixmap(matrix=fitz.Matrix(2,2),alpha=False)
        pix.save(P/'images'/f'guide-{i+1:02d}.png')
    shutil.copy2(P/'images/guide-06.png',P/'images/end-section.png')
    thumbs=[]
    for i in range(len(doc)):
        im=Image.open(P/'images'/f'guide-{i+1:02d}.png');im.thumbnail((450,338));thumbs.append(im.copy())
    contact=Image.new('RGB',(900,338*4),'#DDE0DD')
    for i,im in enumerate(thumbs):contact.paste(im,((i%2)*450,(i//2)*338))
    contact.save(P/'qa/contact-sheet.png')

def copy_beside_parts(data):
    for p in data['printed_parts']:
        target=(ROOT/p['stl']).parent
        for src,dest in [('cell.png' if p['ref'] in ('P1','P2') else 'rail.png','presentation_assembled.png'),
                         ('exploded.png','presentation_exploded.png'),('guide-04.png','assembly_guide.png'),
                         ('guide-03.png','parts_list.png'),('end-section.png','end_detail.png')]:
            shutil.copy2(P/'images'/src,target/dest)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--render',action='store_true')
    parser.add_argument('--readme-only',action='store_true',help='Refresh README images, thumbnails and CSV without rebuilding the PDF')
    parser.add_argument('--blender',default='blender')
    args=parser.parse_args()
    for directory in ('raw','images','scenes','qa'):(P/directory).mkdir(exist_ok=True)
    if args.render:
        for shot in (README_SHOTS if args.readme_only else SHOTS+README_SHOTS):
            with (P/'qa'/f'render_{shot}.log').open('w') as stream:
                subprocess.run([args.blender,'--background','--python-exit-code','1','--python',str(ROOT/'render_kallax.py'),'--',shot],stdout=stream,stderr=subprocess.STDOUT,check=True)
    data=json.loads((P/'project.json').read_text(encoding='utf-8'))
    publish_images()
    if not args.readme_only:
        make_pdf(data);export_pages()
    build_readme(ROOT,P/'templates/README.template.md')
    if not args.readme_only:
        copy_beside_parts(data)
    # Stable legacy download path resolves to the current guide as well.
    if not args.readme_only:
        shutil.copy2(P/'assembly-guide.pdf',ROOT/'output/pdf/kallax_filament_visual_assembly_guide.pdf')
    print('Built README, thumbnails, published renders and CSV.' if args.readme_only else
          'Built guide, page previews, published renders, README, thumbnails and CSV.')
