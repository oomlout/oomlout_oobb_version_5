"""Thin-wall 0.8 mm nozzle tubs; original Gridfinity components are read-only dependencies."""
import copy
import math
from pathlib import Path
from components.gridfinity_tray_quarter_increment import working as quarter

NAME = "gridfinity_tub_nozzle_08_no_lip"
WRAPPER = str(Path(__file__).with_name("tub.scad"))

def metadata(lipped=False):
    name = "gridfinity_tub_nozzle_08_lipped" if lipped else NAME
    values = [
        ("gridfinity_width", "X footprint in Gridfinity units; width is an alias.", 2),
        ("gridfinity_height", "Y footprint in Gridfinity units; height is an alias.", 1),
        ("gridfinity_depth", "Total height including any lip in 7 mm units; depth is an alias, not mm.", 16.5/7),
        ("wall_thickness", "Thin wall for one nominal 0.9 mm extrusion.", 0.9),
        ("floor_thickness", "Efficient floor, nominal mm; includes 0.01 mm Boolean allowance.", 1.0),
    ]
    return dict(name=name, name_long="Gridfinity: 0.8 mm nozzle tub " + ("lipped" if lipped else "no lip"),
        shape_aliases=[name], category="Gridfinity", returns="Raw SCAD geometry component dict.",
        description="Efficient thin-wall tub with exactly one existing countersunk M3 label receiver.",
        notes=["42 mm XY pitch, 7 mm Z units, standard feet and 0.5 mm footprint clearance.",
               "Whole/half footprints; quarter increments on one axis. Minimum footprint 0.5 x 0.5.",
               "Default depth is 16.5/7 units. Both variants have nominal total height depth*7, including the lip.",
               "0.9 mm walls and 1 mm recessed floor target a 0.8 nozzle with 0.9 line width.",
               "label_mount accepts corner, along_wall_offset_mm and rim_lift_mm as in tray_2.",
               "Half-height bins use the short-end mount; lipped receivers are lowered to clear stacked feet.",
               "Lipped rim retains the full original upper chamfer: 1.9 mm peak thickness, a 0.4 mm flat inner face, and a 45-degree underside to the thin wall."],
        variables=[dict(name=n, description=d, type="number", default=v) for n,d,v in values]
            + [dict(name="label_mount", description="Optional existing tray_2 mount placement overrides.", type="dict", default={}),
               dict(name="pos", description="XYZ translation in mm.", type="list", default=[0,0,0]),
               dict(name="rot", description="XYZ rotation in degrees.", type="list", default=[0,0,0])])

def describe():
    return metadata()

def define():
    return metadata()

def _finite(value, name):
    if isinstance(value, bool):
        raise ValueError(name + " must be a finite number")
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(name + " must be a finite number")
    return value

def make(lipped, **kwargs):
    sizes = {}
    for key, alias, default, pitch in [("gridfinity_width","width",2,42),
                                      ("gridfinity_height","height",1,42),
                                      ("gridfinity_depth","depth",16.5/7,7)]:
        value = kwargs.get(key, kwargs.get(alias, default))
        sizes[key] = _finite(quarter._units(value, pitch), key)
    w,h,d = [sizes[k] for k in ("gridfinity_width","gridfinity_height","gridfinity_depth")]
    quarter.action(**sizes)  # Validate fractional feet without altering their implementation.
    if min(w,h)<0.5 or d*7<16.5:
        raise ValueError("The existing label mount requires at least 0.5 x 0.5 units and 16.5 mm total height")
    wall = _finite(kwargs.get("wall_thickness",0.9), "wall_thickness")
    floor = _finite(kwargs.get("floor_thickness",1.0), "floor_thickness")
    if not 0.8<=wall<=1.6 or not 0.8<=floor<=2:
        raise ValueError("Use 0.8–1.6 mm walls and 0.8–2.0 mm floors")
    mount = copy.deepcopy(kwargs.get("label_mount",{}))
    half = h == 0.5
    corner = mount.get("corner",1 if half else 0)
    offset = _finite(mount.get("along_wall_offset_mm",-3.25 if half else -1), "label offset")
    lift = _finite(mount.get("rim_lift_mm",-2.15 if lipped else (1.8 if half else 0)), "label lift")
    if isinstance(corner,bool) or corner not in (0,1,2,3):
        raise ValueError("label corner must be 0, 1, 2 or 3")
    # Keep the whole pad on the selected straight wall and above the foot profile.
    along = (w if corner%2==0 else h)*42
    minimum = 4.1 if lipped else 6.2
    maximum = d*7-3.75-.2-8.4 if lipped else d*7-8.4
    if not 4.8 <= 10.25+offset <= along-4.8 or not minimum-1e-7 <= d*7-10.2+lift <= maximum+1e-7:
        raise ValueError("Label placement must remain on the wall, above the base and below the rim")
    fn = _finite(kwargs.get("fn",64), "fn")
    if fn<24 or fn!=int(fn):
        raise ValueError("fn must be an integer of at least 24")
    # These purpose-specific components deliberately expose no base/pitch/lip overrides.
    for key in ("pitch","clearance","lip_style","flat_base","efficient_floor","enable_magnets","enable_screws"):
        if key in kwargs:
            raise ValueError(key + " is fixed by this component; use the original raw component for arbitrary geometry")
    return dict(type=kwargs.get("type",kwargs.get("t","positive")), shape="raw_scad",
        file=WRAPPER, module="gridfinity_tub_nozzle_08",
        module_kwargs=dict(**sizes,lipped=lipped,wall_thickness=wall,floor_thickness=floor,
            label_corner=corner,label_offset=offset,label_lift=lift,fn=int(fn)),
        pos=copy.deepcopy(kwargs.get("pos",[0,0,0])),rot=copy.deepcopy(kwargs.get("rot",[0,0,0])),
        inclusion=kwargs.get("inclusion","all"),m=kwargs.get("m",""))

def action(**kwargs):
    return make(False, **kwargs)
