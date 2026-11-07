"""Apply the four-section README specification without changing assembly geometry."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
path = ROOT/'presentation/project.json'
data = json.loads(path.read_text(encoding='utf-8'))
data['readme_revision'] = '4'
data['readme_date'] = '2026-11-07'
for part in data['hardware']:
    if part['ref'] == 'H1':
        part.update(url=None, oomp_id=None, md5_6_alpha=None, short_url=None,
                    catalogue_status='pending',
                    verification='User requested OOMP record pending on 2026-11-07; no supplier link in README.')
    else:
        part['url'] = 'https://github.com/oomlout/oomp_hardware_bolt_version_5/tree/main/parts/'+part['oomp_id']
        part['short_url'] = 'https://oom.lt/a/'+part['md5_6_alpha']
        part['code_verified'] = 'Exact ID and md5_6_alpha checked in public OOMP working.yaml, 2026-11-07. Short URL follows requested format; redirect unavailable to verification tool.'
steps = [
    ('Cut and deburr four 300 mm M6 rods. Seat two M6 nuts in a short frame’s outer recesses. Thread in two rods with their ends flush.',
     'step-fixed.png', 'AI-generated CAD render: fixed-end frame, recessed nuts and two rods'),
    ('On both rods, fit a 99.67 mm sleeve, second frame, 67.67 mm sleeve, third frame and 99.67 mm sleeve. Face the last sleeve’s hex pocket toward the coupling.',
     'step-sleeves.png', 'AI-generated CAD render: three frames and long sleeves on the two rods'),
    ('Insert each M6 coupling nut into an 18 mm housing. Thread it onto the rod by approximately 6 mm.',
     'step-coupling.png', 'AI-generated CAD render: rod end, M6 coupling nut and printed housing'),
    ('Face the final frame’s hex recesses outward. Insert the M6 × 25 mm bolts. Add retaining nuts loosely, then slide on the 7 mm hex covers. Thread the bolts into the couplings.',
     'adjust.png', 'AI-generated CAD render: coupling, covers, retaining nut, final frame and adjustment bolt'),
    ('Set the span to the measured opening; nominally 335 mm. Seat the bolt heads in their recesses. Tighten the retaining nuts against the inner frame face, replace the hex covers and clip the 7 mm slotted covers over the exposed thread.',
     'end-section.png', 'AI-generated section drawing: recessed bolt head, retaining nut and end covers'),
    ('Repeat with four tall frames. Place the tall holder at the rear and the short holder at the front. Load strapped rear refills, then front reels.',
     'cell.png', 'AI-generated CAD render: both holders installed and loaded in a KALLAX cell'),
]
data['readme'].update(
    layout='four-section',
    summary='This project provides 3D-printable holders for storing 3D printer filament in an IKEA KALLAX shelving unit. Two holders store five reels at the front and five filament refills without spools on a raised row at the back.',
    hero_image='cell.png', hero_alt='AI-generated CAD render: finished filament storage in a KALLAX cell',
    details='Each holder uses four side frames and two adjustable M6 rails. The short and tall holders are independent. Nominal width: 335 mm. Rail heights: 37 and 112 mm. Print all 32 plastic pieces in black.',
    details_image='printed.png', details_alt='AI-generated CAD render: assembled printed parts, with hardware, filament and cabinet omitted',
    downloads='[Print files](parts) · [Full BOM](presentation/parts.csv) · [Assembly guide](presentation/assembly-guide.pdf) · [Build notes](presentation/README.md)',
    parts_image='exploded.png', parts_alt='AI-generated CAD render: exploded short holder with frames, sleeves and hardware',
    parts_caption='Short holder shown. The rear holder uses tall frames.',
    parts_scope='Hardware quantities for one complete cell. Double for two cells.',
    hardware_notes='Threaded rod: OOMP record pending.',
    assembly_steps=[dict(text=text,image=image,alt=alt) for text,image,alt in steps],
)
path.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print('Configured Summary / Details / Parts / Assembly.')
