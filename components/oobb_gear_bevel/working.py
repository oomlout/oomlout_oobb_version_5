"""Straight right-angle bevel gear, using the existing BOSL2 submodule."""

import copy
import math
import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)
_BOSL2_PATH = os.path.join(_PROJECT_ROOT, "components", "github_belfry_bosl2_gear", "BOSL2")


def describe():
    variables = [
        ("teeth", "Gear tooth count, integer >= 3.", "number", 40),
        ("mate_teeth", "Mating tooth count; defaults to teeth (1:1 mitre pair).", "number", 40),
        ("mod", "Outer module; alias: module. Pitch diameter = mod * teeth.", "number", 1.5),
        ("depth", "Exact thickness between flat bottom and top cuts, in mm. No straight backing.", "number", 9),
        ("face_width", "Generated cone width, automatically long enough to span the depth before trimming.", "number", None),
        ("base_chamfer", "Bed-circle inset below the tooth-root circle; default 0.8 mm at mod 1.5, scaled with module.", "number", 0.8),
        ("underside_angle", "Underside ramp angle measured from the print bed, 45 to less than 90 degrees.", "number", 45),
        ("shaft_diam", "Bore diameter in mm; 0 leaves OOBB holes to the caller.", "number", 0),
        ("pressure_angle", "Tooth pressure angle in degrees.", "number", 20),
        ("backlash", "Tangential tooth thinning in mm, applied to each gear.", "number", 0.2),
        ("clearance", "Dedendum clearance in mm; defaults to mod/4.", "number", None),
        ("gear_spin", "Tooth phase about the local Z axis in degrees.", "number", 0),
        ("anchor", "center, bottom, pitchbase or apex. Teeth face local +Z.", "string", "center"),
        ("pos", "Position [x,y,z] in mm.", "list", [0, 0, 0]),
        ("rot", "Rotation [rx,ry,rz] in degrees, applied before pos.", "list", [0, 0, 0]),
        ("mode", "laser, 3dpr, true, all, or a list of modes.", "list", ["laser", "3dpr", "true"]),
    ]
    return {
        "name": "oobb_gear_bevel", "name_long": "OOBB Motion: Straight Bevel Gear",
        "description": "Flat-top straight bevel gear with a circular bed footprint and a 45 degree underside ramp to the teeth; no pedestal.",
        "category": "OOBB Motion", "shape_aliases": ["oobb_gear_bevel", "bevel_gear"],
        "returns": "List containing a raw SCAD geometry component.",
        "source": "https://github.com/BelfrySCAD/BOSL2/wiki/gears.scad#functionmodule-bevel_gear",
        "variables": [{"name": n, "description": d, "type": t, "default": v} for n, d, t, v in variables],
    }


def define():
    return describe()


def _number(name, value, minimum=0, strict=False):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{name} must be a finite number")
    if value < minimum or (strict and value == minimum):
        raise ValueError(f"{name} must be {'greater than' if strict else 'at least'} {minimum}")
    return value


def dimensions(**kwargs):
    """Validated dimensions, also usable by part generators for safe hole placement."""
    teeth = _number("teeth", kwargs.get("teeth", 40), 3)
    mate_teeth = _number("mate_teeth", kwargs.get("mate_teeth", teeth), 3)
    if int(teeth) != teeth or int(mate_teeth) != mate_teeth:
        raise ValueError("teeth and mate_teeth must be integers")
    if kwargs.get("shaft_angle", 90) != 90:
        raise ValueError("oobb_gear_bevel currently supports shaft_angle=90 only")
    mod = _number("mod", kwargs.get("mod", kwargs.get("module", 1.5)), strict=True)
    depth = _number("depth", kwargs.get("depth", 9), strict=True)
    pressure_angle = _number("pressure_angle", kwargs.get("pressure_angle", 20), strict=True)
    if pressure_angle >= 45:
        raise ValueError("pressure_angle must be less than 45 degrees")
    backlash = _number("backlash", kwargs.get("backlash", 0.2))
    if backlash >= math.pi * mod / 2:
        raise ValueError("backlash must be less than half the circular pitch")
    clearance = _number("clearance", kwargs.get("clearance", mod / 4))
    shaft_diam = _number("shaft_diam", kwargs.get("shaft_diam", 0))
    angle = math.atan2(teeth, mate_teeth)
    pitch_radius = teeth * mod / 2
    cone_distance = pitch_radius / math.sin(angle)
    # Start the flat bed at the outer heel's tooth tips, rather than adding a
    # backing below its sloping underside. Generate past the top plane and trim.
    dedendum = mod + clearance
    minimum_face_width = (depth + (mod + dedendum) * math.sin(angle)) / (
        math.cos(angle) + dedendum * math.sin(angle) / cone_distance
    ) + 0.2
    face_width = _number("face_width", kwargs.get("face_width", minimum_face_width), strict=True)
    if face_width < minimum_face_width - 1e-9:
        raise ValueError("face_width is too short to span the full part depth with a flat top")
    if face_width >= cone_distance:
        raise ValueError("Full-depth bevel reaches the pitch apex; increase gear diameter or reduce depth")
    # Deliberately conservative: smaller than the root radius on the tilted face.
    inner_root_radius = (pitch_radius - mod - clearance) * (1 - face_width / cone_distance)
    if inner_root_radius <= 0 or shaft_diam >= 2 * inner_root_radius:
        raise ValueError("shaft_diam leaves no material inside the small-end tooth roots")
    base_chamfer = _number("base_chamfer", kwargs.get("base_chamfer", mod * 8 / 15))
    if base_chamfer >= min(depth / 4, inner_root_radius):
        raise ValueError("base_chamfer must be smaller than depth/4 and the inner root radius")
    underside_angle = _number("underside_angle", kwargs.get("underside_angle", 45), 45)
    if underside_angle >= 90:
        raise ValueError("underside_angle must be less than 90 degrees")
    return {
        "teeth": int(teeth), "mate_teeth": int(mate_teeth), "gear_mod": mod,
        "depth": depth, "face_width": face_width, "shaft_diam": shaft_diam,
        "pressure_angle": pressure_angle, "backlash": backlash, "clearance": clearance,
        "pitch_angle": math.degrees(angle), "cone_distance": cone_distance,
        "inner_root_radius": inner_root_radius,
        "base_chamfer": base_chamfer,
        "underside_angle": underside_angle,
    }


def _build_wrapper_source():
    std_path = os.path.join(_BOSL2_PATH, "std.scad").replace("\\", "/")
    gears_path = os.path.join(_BOSL2_PATH, "gears.scad").replace("\\", "/")
    return f'''include <{std_path}>
include <{gears_path}>

function oobb_gear_bevel_face_width(teeth=40,mate_teeth=40,gear_mod=1.5,depth=9,clearance=0.375) =
    let(delta=atan(teeth/mate_teeth),R=gear_mod*teeth/2/sin(delta),d=gear_mod+clearance)
    (depth+(gear_mod+d)*sin(delta))/(cos(delta)+d*sin(delta)/R)+0.2;

// Measure the outer heel separately so the whole visible side is bevelled.
// This also gives callers a common reference for positioning centered STLs.
function oobb_gear_bevel_base_z(teeth=40,mate_teeth=40,gear_mod=1.5,
    pressure_angle=20,backlash=0.2,clearance=0.375,gear_spin=0) =
    let(heel=bevel_gear(mod=gear_mod,teeth=teeth,mate_teeth=mate_teeth,
        shaft_angle=90,face_width=0.0001,backing=0,spiral=0,cutter_radius=0,
        pressure_angle=pressure_angle,backlash=backlash,clearance=clearance,
        gear_spin=gear_spin,anchor="pitchbase"))
    pointlist_bounds(heel[0])[1].z;

module oobb_gear_bevel_raw(teeth=40,mate_teeth=40,gear_mod=1.5,depth=9,
    face_width=undef,shaft_diam=0,pressure_angle=20,backlash=0.2,
    clearance=0.375,gear_spin=0,anchor="center",base_chamfer=undef,underside_angle=45) {{
    fw=is_undef(face_width) ? oobb_gear_bevel_face_width(teeth,mate_teeth,gear_mod,depth,clearance) : face_width;
    chamfer=is_undef(base_chamfer) ? gear_mod*8/15 : base_chamfer;
    bare=bevel_gear(mod=gear_mod,teeth=teeth,mate_teeth=mate_teeth,
        shaft_angle=90,face_width=fw,backing=0,spiral=0,cutter_radius=0,
        pressure_angle=pressure_angle,backlash=backlash,clearance=clearance,
        gear_spin=gear_spin,anchor="pitchbase");
    base=oobb_gear_bevel_base_z(teeth,mate_teeth,gear_mod,
        pressure_angle,backlash,clearance,gear_spin);
    delta=atan(teeth/mate_teeth);
    apex=gear_mod*teeth/2/tan(delta);
    shift=anchor=="center" ? -base-depth/2
         : anchor=="bottom" ? -base
         : anchor=="apex" ? -apex : 0;
    extent=2*(gear_mod*teeth+depth);
    foot=projection(bare,cut=true,z=base+0.0001);
    root_radius=min([for(p=foot[0]) norm(p)]);
    bed_radius=root_radius-chamfer;
    assert(bed_radius>shaft_diam/2,"Underside ramp leaves no bed footprint around the shaft");
    translate([0,0,shift])
      difference() {{
        intersection() {{
            vnf_polyhedron(bare,convexity=12);
            translate([-extent,-extent,base]) cube([2*extent,2*extent,depth]);
            // Remove the material below a true radial ramp. The teeth start
            // above the bed, while the central body stays directly on it.
            translate([0,0,base])
                cylinder(r1=bed_radius,r2=bed_radius+depth/tan(underside_angle),
                    h=depth,$fn=max($fn,teeth*4));
        }}
        if(shaft_diam>0) cylinder(d=shaft_diam,h=4*(depth+apex),center=true);
      }}
}}
'''


def action(**kwargs):
    for filename in ("std.scad", "gears.scad"):
        if not os.path.isfile(os.path.join(_BOSL2_PATH, filename)):
            raise FileNotFoundError("BOSL2 is missing. Run git submodule update --init components/github_belfry_bosl2_gear/BOSL2")
    dims = dimensions(**kwargs)
    anchor = kwargs.get("anchor", "center")
    if anchor not in ("center", "bottom", "pitchbase", "apex"):
        raise ValueError("anchor must be center, bottom, pitchbase or apex")
    gear_spin = kwargs.get("gear_spin", 0)
    if isinstance(gear_spin, bool) or not isinstance(gear_spin, (int, float)) or not math.isfinite(gear_spin):
        raise ValueError("gear_spin must be a finite number")
    modes = kwargs.get("inclusion", kwargs.get("mode", "all"))
    modes = [modes] if isinstance(modes, str) else list(modes)
    if not modes or any(m not in ("all", "laser", "3dpr", "true") for m in modes):
        raise ValueError("mode must contain all, laser, 3dpr or true")
    inclusions = ["all"] if "all" in modes else list(dict.fromkeys(modes))
    module_kwargs = {key: dims[key] for key in (
        "teeth", "mate_teeth", "gear_mod", "depth", "face_width", "shaft_diam",
        "pressure_angle", "backlash", "clearance",
        "base_chamfer", "underside_angle",
    )}
    module_kwargs["gear_spin"] = gear_spin
    module_kwargs["anchor"] = anchor
    component = {
        "type": kwargs.get("type", "positive"), "shape": "raw_scad",
        "source": _build_wrapper_source(), "module": "oobb_gear_bevel_raw",
        "module_kwargs": module_kwargs, "include_mode": True,
        "pos": copy.deepcopy(kwargs.get("pos", [0, 0, 0])),
        "rot": copy.deepcopy(kwargs.get("rot", [kwargs.get("rot_x", 0), kwargs.get("rot_y", 0), kwargs.get("rot_z", 0)])),
        "color": kwargs.get("color", ""), "m": kwargs.get("m", ""),
    }
    return [dict(copy.deepcopy(component), inclusion=mode) for mode in inclusions]


def test():
    import opsc

    generated = []
    for scale, mod, bore in (("big", 1.5, 6.5), ("little", 0.75, 3.6)):
        folder = os.path.join(os.path.dirname(__file__), "test", scale)
        os.makedirs(folder, exist_ok=True)
        path = os.path.join(folder, "working.scad")
        opsc.opsc_make_object(path, action(teeth=50, mod=mod, depth=6, shaft_diam=bore),
                              mode="3dpr", save_type="none", render=False)
        opsc.save_preview_images(path, folder)
        generated.append(os.path.join(folder, "image.png"))
    return generated
