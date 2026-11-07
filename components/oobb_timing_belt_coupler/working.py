"""Solid-base belt buckle with upright wrap posts and movable clamp jaws.

X is belt travel, Y is the fold plane, Z is belt width. Both cheeks print
flat on Z=0. Transverse screws close the throats; draw_tensioner adds a
pair of side-mounted M3 screws between two identical belt ends.
"""

import copy
import math


# Nominal starting values, not a substitute for measuring a particular belt.
# Adding a profile requires no geometry changes. Static fold radii are design
# allowances, not manufacturer-rated running pulley radii.
BELT_PROFILES = {
    "gt2": {"pitch": 2, "belt_thickness": 1.52, "tooth_height": 0.76,
            "bend_radius": 2, "screw_size": "m3"},
    "htd5m": {"pitch": 5, "belt_thickness": 3.81, "tooth_height": 2.06,
              "bend_radius": 5, "screw_size": "m4"},
}


def describe():
    return {
        "name": "oobb_timing_belt_coupler",
        "name_long": "OOBB Motion: Open Timing Belt Coupler",
        "description": "Recessed belt-loop bases, screw-tightened jaws, and optional matching M3 draw-tensioner ends.",
        "category": "OOBB Motion", "shape_aliases": ["timing_belt_coupler"],
        "returns": "List of geometry component dictionaries.",
        "variables": [
            {"name": name, "type": kind, "default": default, "description": description}
            for name, kind, default, description in [
                ("style", "string", "fold_back", "fold_back: shared jaw; fold_back_independent: separate jaws; draw_tensioner: matching single-belt ends with axial M3 adjustment."),
                ("guide_extension", "number", "one belt pitch", "Extra length of the guide and surrounding taper, preserving channel clearance."),
                ("adjustment_gap", "number", 6, "draw_tensioner only: end separation from 2 to 10 mm; two M3 side draw screws."),
                ("channel_depth", "number", 1, "Depth of the loop track cut into the base, retaining at least 1.5 mm floor."),
                ("base_thickness", "number", 3, "Continuous flat floor beneath posts and jaws."),
                ("slide_clearance", "number", 0.25, "Clearance under the moving jaws above the base."),
                ("belt_profile", "string", "gt2", "gt2, htd5m (alias htd5), or a new registry entry."),
                ("depth", "number", 6, "Nominal belt width in mm; belt_width is also accepted."),
                ("overlap_teeth", "number", 5, "Whole pitches clamped on each side, at least three."),
                ("compression_gap", "number", 0.5, "Closing travel between the two cheeks, along Y."),
                ("belt_dimensions", "dict", {}, "Explicit profile overrides, or full dimensions for a new profile."),
                ("layout", "string", "print", "print, assembled, exploded, lower/upper, section; draw_tensioner also supports end_print and end_assembled."),
                ("pos", "list", [0, 0, 0], "Whole-component translation after layout."),
                ("rot", "list", [0, 0, 0], "Whole-component rotation after layout."),
            ]
        ],
    }


def define():
    return describe()


def _number(name, value, minimum=0, strict=False):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{name} must be a finite number")
    if value < minimum or (strict and value == minimum):
        raise ValueError(f"{name} must be {'greater than' if strict else 'at least'} {minimum}")
    return float(value)


def dimensions(**kwargs):
    import oobb

    if kwargs.get("style") == "draw_tensioner":
        return _tensioner_dimensions(**kwargs)

    profile = kwargs.get("belt_profile", "gt2")
    if profile == "htd5":
        profile = "htd5m"
    if not isinstance(profile, str) or not profile:
        raise ValueError("belt_profile must be a nonempty name")
    overrides = kwargs.get("belt_dimensions", {})
    if not isinstance(overrides, dict):
        raise ValueError("belt_dimensions must be a dictionary")
    spec = copy.deepcopy(BELT_PROFILES.get(profile, {}))
    spec.update(overrides)
    for key in ["pitch", "belt_thickness", "tooth_height", "bend_radius"]:
        if key not in spec and key not in kwargs:
            raise ValueError(f"Unknown belt profile {profile}: provide belt_dimensions.{key}")
        spec[key] = _number(key, kwargs.get(key, spec.get(key)), strict=True)
    if spec["tooth_height"] >= spec["belt_thickness"]:
        raise ValueError("tooth_height must be less than belt_thickness")
    width = _number("belt_width", kwargs.get("belt_width", kwargs.get("depth", 6)), strict=True)
    clearance = _number("width_clearance", kwargs.get("width_clearance", 0.6))
    wall = _number("wall", kwargs.get("wall", 3), 2)
    overlap = _number("overlap_teeth", kwargs.get("overlap_teeth", 5), 3)
    if overlap != int(overlap):
        raise ValueError("overlap_teeth must be an integer")
    stack = 2 * spec["belt_thickness"] - spec["tooth_height"]
    gap = _number("compression_gap", kwargs.get("compression_gap", 0.5), 0, strict=True)
    if gap >= stack:
        raise ValueError("compression_gap must be less than the meshed belt stack")
    screw = kwargs.get("screw_size", spec.get("screw_size", "m3"))
    if screw not in ["m3", "m4"]:
        raise ValueError("screw_size must be m3 or m4")
    modes = ["3dpr", "true"]
    head_radius = max(oobb.gv("screw_countersunk_radius_" + screw, mode) for mode in modes)
    nut_radius = max(oobb.gv("nut_radius_" + screw, mode) for mode in modes)
    nut_depth = max(oobb.gv("nut_depth_" + screw, mode) for mode in modes)
    head_depth = max(oobb.gv("screw_countersunk_depth_" + screw, mode) for mode in modes)
    radius = spec["bend_radius"] + spec["belt_thickness"] + gap + 0.2
    central = _number("central_web", kwargs.get("central_web", 2 * (max(head_radius, nut_radius) + 2)), 2 * (max(head_radius, nut_radius) + 1))
    style = kwargs.get("style", "fold_back")
    if style not in ["fold_back", "fold_back_independent"]:
        raise ValueError("Unknown belt coupler style")
    if style == "fold_back_independent":
        central = max(central, 4 * (max(head_radius, nut_radius) + 2))
    base = _number("base_thickness", kwargs.get("base_thickness", 3), 2)
    slide = _number("slide_clearance", kwargs.get("slide_clearance", 0.25), 0.1)
    if slide > 0.8:
        raise ValueError("slide_clearance must not exceed 0.8 mm")
    channel_depth = _number("channel_depth", kwargs.get("channel_depth", 1), 0.3)
    if base - channel_depth < 1.5:
        raise ValueError("channel_depth must leave at least 1.5 mm of solid floor")
    centre = central / 2 + radius + wall
    guide_extension = _number("guide_extension", kwargs.get("guide_extension", spec["pitch"]))
    transition = centre + radius + spec["pitch"] + guide_extension
    clamp = overlap * spec["pitch"]
    end = transition + clamp
    # Straight, full-width middle between the two round loop chambers.
    bridge = 2 * (radius + wall)
    height = max(width + clearance, 2 * (math.sqrt(2)*max(head_radius, nut_radius) + 1))
    clamp_screw_length = next(n for n in range(6, 201) if n in [6,8,10,12,16,20] + list(range(25,201,5)) and n >= bridge-.2)
    layout = kwargs.get("layout", "print")
    if layout not in ["print", "assembled", "exploded", "lower", "upper", "section"]:
        raise ValueError(f"Unknown belt coupler layout: {layout}")
    if gap >= stack - 0.2:
        raise ValueError("compression_gap leaves no belt throat")
    return dict(spec, belt_profile=profile, depth=width, belt_width=width,
                width_clearance=clearance, channel_width=width + clearance, wall=wall,
                overlap_teeth=int(overlap), clamp_length=clamp, loop_radius=radius,
                loop_centre=centre, transition_x=transition, central_web=central,
                body_length=2 * end, body_width=max(bridge, 2 * (radius + wall)),
                bridge_width=bridge, assembled_depth=base + height, cheek_height=height,
                base_thickness=base, slide_clearance=slide, post_radius=spec["bend_radius"],
                channel_depth=channel_depth, channel_floor=base-channel_depth,
                island_tip=transition-max(2*spec["belt_thickness"],spec["pitch"]),
                guide_extension=guide_extension,
                screw_z=base + height / 2, style=style,
                screw_positions=[-central / 4, central / 4] if style == "fold_back_independent" else [0],
                piece_count=3 if style == "fold_back_independent" else 2, stack_height=stack,
                compression_gap=gap, screw_size=screw, clamp_screw_length=clamp_screw_length,
                print_spacing=_number("print_gap", kwargs.get("print_gap", 8), 2),
                layout=layout, split=True, oobb_hole_positions=[])


def _group(objects, pos=None, rot=None, typ="positive"):
    return {"type": "rotation", "typetype": typ, "pos": pos or [0, 0, 0],
            "rot": rot or [0, 0, 0], "objects": copy.deepcopy(objects)}


def _gate(items, mode):
    """Isolate each mode while preserving OOBB's print-only bridge geometry."""
    kept = []
    for item in items:
        if isinstance(item, list):
            kept.append(_gate(item, mode))
            continue
        if item.get("inclusion", "all") not in ["all", mode]:
            continue
        item["inclusion"] = mode
        if "objects" in item:
            item["objects"] = _gate(item["objects"], mode)
        kept.append(item)
    return kept


def _pieces(v):
    import oobb

    def circle(x, radius, z=0, height=None):
        return oobb.oobb_easy(shape="oobb_cylinder", type="positive", radius=radius,
                              depth=v["cheek_height"] if height is None else height,
                              zz="bottom", pos=[x, 0, z])

    def box(x, y, z, sx, sy, sz, typ="positive"):
        return oobb.oobb_easy(shape="cube", type=typ, size=[sx, sy, sz], pos=[x-sx/2,y-sy/2,z])

    body = box(0, 0, 0, 2*v["loop_centre"], v["bridge_width"], v["cheek_height"])
    cuts = []
    for sign in [-1, 1]:
        # Broad round loop well narrows into a straight doubled-belt throat.
        body.append({"type":"hull", "typetype":"positive", "objects":
                     circle(sign*v["loop_centre"], v["loop_radius"]+v["wall"]) +
                     box(sign*(v["body_length"]/2-0.5),0,0,1,v["stack_height"]+2*v["wall"],v["cheek_height"])})
        cuts.append({"type":"hull", "typetype":"negative", "objects":
                     circle(sign*v["loop_centre"], v["loop_radius"],-1,v["cheek_height"]+2) +
                     circle(sign*v["transition_x"], v["stack_height"]/2,-1,v["cheek_height"]+2)})
        cuts.extend(box(sign*(v["transition_x"]+v["clamp_length"]/2+1),0,-1,
                        v["clamp_length"]+2,v["stack_height"],v["cheek_height"]+2,"negative"))
    outline = copy.deepcopy(body)
    pocket_cuts = copy.deepcopy(cuts)
    body.extend(cuts)
    for screw_x in v["screw_positions"]:
        for mode in ["3dpr", "true"]:
            hardware = oobb.oobb_easy(shape="screw_countersunk", type="negative",
                radius_name=v["screw_size"], depth=v["bridge_width"], nut=True,
                overhang=True, mode=mode, pos=[screw_x,v["bridge_width"]/2,v["cheek_height"]/2],rot=[-90,0,0])
            body.extend(_gate(hardware,mode))
    halves=[]
    span=max(v["body_length"],v["body_width"])*2
    for sign in [-1,1]:
        half=copy.deepcopy(body)
        # Remove the opposite cheek, leaving closing travel along Y.
        half.extend(box(0,-sign*(span/2-v["compression_gap"]/2),-1,
                        span,span,v["cheek_height"]+2,"negative"))
        halves.append(half)
    # Match the plate perimeter to the curved wall outline. The centre
    # bridge stays full width and full thickness around the screw bosses.
    floor = outline
    floor.extend(box(0,0,v["base_thickness"],span,span,v["cheek_height"]+2,"negative"))
    # The same pocket geometry makes an actual recessed routing track in
    # the plate. Limit the cutter from below to retain a solid flat floor.
    def positive_cut(items):
        result=copy.deepcopy(items)
        def visit(item):
            if isinstance(item,list):
                for child in item: visit(child)
            elif isinstance(item,dict):
                if item.get("typetype")=="negative": item["typetype"]="positive"
                if item.get("type")=="negative": item["type"]="positive"
        for item in result: visit(item)
        return result
    channel = positive_cut(pocket_cuts)
    channel.extend(box(0,0,-2,span,span,2+v["channel_floor"],"negative"))
    floor.append(_group(channel,typ="negative"))
    base = [_group(floor), _group(halves[0],pos=[0,0,v["base_thickness"]])]
    # An elongated rounded island defines the inside of each teardrop
    # channel, rather than leaving a round peg in an oversized pocket.
    for sign in [-1,1]:
        base.append({"type":"hull","typetype":"positive","objects":
            circle(sign*v["loop_centre"],v["post_radius"],0,v["assembled_depth"]) +
            circle(sign*v["island_tip"],0.25,0,v["assembled_depth"])})
    jaw=halves[1]
    # Clearance underneath the moving jaw permits screw-driven sliding.
    jaw.extend(box(0,0,-1,span,span,1+v["slide_clearance"],"negative"))
    jaws=[]
    for sign in ([-1,1] if v["style"] == "fold_back_independent" else [0]):
        item=copy.deepcopy(jaw)
        if sign:
            item.extend(box(-sign*(span/2-0.4),0,-1,span,span,v["cheek_height"]+2,"negative"))
        jaws.append([_group(item,pos=[0,0,v["base_thickness"]])])
    return [base]+jaws


def _tensioner_dimensions(**kwargs):
    """Two side draw screws, identical end bodies and identical jaws.

    Local end points out along +X. Rotate a second end 180 degrees in XY.
    Each end has one socket-head seat and one nut pocket on opposite sides.
    """
    settings = dict(kwargs, style="fold_back_independent", screw_size="m3")
    requested_layout=kwargs.get("layout","print")
    if requested_layout in ["end_print","end_assembled"]:
        settings["layout"]="print" if requested_layout=="end_print" else "assembled"
    if kwargs.get("screw_size", "m3") != "m3":
        raise ValueError("draw_tensioner uses M3 hardware")
    end = dimensions(**settings)
    gap = _number("adjustment_gap", kwargs.get("adjustment_gap", 6), 2)
    if gap > 10:
        raise ValueError("adjustment_gap must be between 2 and 10 mm")
    # Side lugs align with the inner half of each loop, without rear tool wells.
    draw_x=end['loop_centre']-end['loop_radius']/2
    draw_y=end['body_width']/2+5.5
    # Keep a solid wall beneath the head in the jaw's own print orientation.
    draw_z=end['base_thickness']+end['slide_clearance']+5.5
    screw_length=5*math.ceil((2*draw_x+10+3+1)/5)
    offset=gap/2
    v=dict(end)
    v.update(style='draw_tensioner',layout=requested_layout,end_dimensions=end,end_offset=offset,
             adjustment_gap=gap,adjustment_min=2.0,adjustment_max=10.0,
             adjustment_travel=8.0,adjustment_pitch=.5,
             draw_x=draw_x,draw_y=draw_y,draw_z=draw_z,
             draw_screw_length=screw_length,draw_screw_size='m3',draw_screw_count=2,
             lug_front=draw_x-6,lug_back=draw_x+3,lug_height=end['assembled_depth'],
             lug_inner=end['body_width']/2-2,lug_outer=draw_y+6,
             body_length=end['body_length']+gap,body_width=2*(draw_y+6),
             screw_positions=[-offset-end['central_web']/4,offset+end['central_web']/4],
             clamp_axis=[0,1,0],draw_axis=[1,0,0],piece_count=4)
    return v


def _tensioner_pieces(v):
    import oobb
    end=v['end_dimensions'];original=_pieces(end)
    span=4*v['body_length']
    def box(x0,x1,y0,y1,z0,z1,typ='positive'):
        return oobb.oobb_easy(shape='cube',type=typ,size=[x1-x0,y1-y0,z1-z0],pos=[x0,y0,z0])
    trimmed=[_group(original[0])]
    trimmed+=box(-span,0,-span,span,-1,v['assembled_depth']+1,'negative')
    base=[_group(trimmed)]
    jaw=copy.deepcopy(original[2])
    for sign in [-1,1]:
        x=v['draw_x'];y=sign*v['draw_y'];z=v['draw_z']
        # Full-height rectangular bosses: no skirt, foot or splay. The head
        # boss belongs to the movable jaw; the nut boss belongs to the base.
        inner=v['lug_inner'];outer=v['lug_outer']
        bottom=end['base_thickness']+end['slide_clearance'] if sign==1 else 0
        lug=box(v['lug_front'],v['lug_back'],inner if sign==1 else -outer,
                outer if sign==1 else -inner,bottom,v['lug_height'])
        for mode in ['true','3dpr']:
            if sign==1:
                cut=oobb.oobb_easy(shape='oobb_screw_socket_cap',type='negative',radius_name='m3',
                     depth=8,overhang=True,mode=mode,pos=[x,y,z],rot=[0,90,0])
                lug.extend(_gate(cut,mode))
            else:
                cut=oobb.oobb_easy(shape='oobb_nut',type='negative',radius_name='m3',depth=3.01,
                     overhang=True,mode=mode,pos=[x,y,z],rot=[0,90,0])
                lug.extend(_gate(cut,mode))
                lug.append(_group(_gate(oobb.oobb_easy(shape='oobb_hole',type='positive',radius_name='m3',
                           depth=8,mode=mode),mode),pos=[v['lug_front']-.5,y,z],rot=[0,90,0],typ='negative'))
        (jaw if sign==1 else base).append(_group(lug))
    return [base,jaw]


def _tensioner_action(v, **kwargs):
    import oobb
    base,jaw=_tensioner_pieces(v)
    objects=[]
    layout=v["layout"]
    single=layout in ["end_print","end_assembled"]
    if single:
        layout="print" if layout=="end_print" else "assembled"
    for sign in ([1] if single else [-1,1]):
        rot=[0,0,180 if sign<0 else 0]
        dx=sign*v["end_offset"]
        if layout == "print":
            dx=sign*v["print_spacing"]/2
        if single:
            dx=0
        if layout != "upper":
            objects.append(_group(base,pos=[dx,0,0],rot=rot))
        if layout != "lower":
            local=[0,0,0]
            if layout in ["print","upper"]:
                local=[0,v["body_width"]+v["print_spacing"],-v["base_thickness"]-v["slide_clearance"]]
            elif layout == "exploded":
                local=[0,v["print_spacing"],v["assembled_depth"]+2]
            objects.append(_group([_group(jaw,pos=local)],pos=[dx,0,0],rot=rot))
    if layout == "section":
        objects.extend(oobb.oobb_easy(shape="cube",type="negative",
            size=[v["body_length"]+2,v["body_width"]+2,v["assembled_depth"]],
            pos=[-v["body_length"]/2-1,-v["body_width"]/2-1,v["screw_z"]]))
    return [_group(objects,pos=kwargs.get("pos",[0,0,0]),rot=kwargs.get("rot",[0,0,0]),typ=kwargs.get("type","positive"))]


def action(**kwargs):
    import oobb
    v=dimensions(**kwargs)
    if v["style"] == "draw_tensioner":
        return _tensioner_action(v, **kwargs)
    pieces=_pieces(v)
    layout=v["layout"]
    if layout == "print":
        objects=[_group(pieces[0])]
        for i,piece in enumerate(pieces[1:]):
            # Keep separate independent jaws apart in X as well as the base.
            dx=(i*2-1)*v["print_spacing"]/2 if len(pieces)==3 else 0
            objects.append(_group(piece,pos=[dx,v["body_width"]+v["print_spacing"],-v["base_thickness"]-v["slide_clearance"]]))
    elif layout == "exploded":
        objects=[_group(pieces[0])]+[_group(piece,pos=[0,v["print_spacing"],5]) for piece in pieces[1:]]
    elif layout == "lower":
        objects=[_group(pieces[0])]
    elif layout == "upper":
        objects=[_group(piece,pos=[0,0,-v["base_thickness"]-v["slide_clearance"]]) for piece in pieces[1:]]
    else:
        objects=[_group(piece) for piece in pieces]
        if layout == "section":
            objects.extend(oobb.oobb_easy(shape="cube",type="negative",
                size=[v["body_length"]+2,v["body_width"]+2,v["assembled_depth"]],
                pos=[-v["body_length"]/2-1,-v["body_width"]/2-1,v["screw_z"]]))
    return [_group(objects,pos=kwargs.get("pos",[0,0,0]),rot=kwargs.get("rot",[0,0,0]),typ=kwargs.get("type","positive"))]
