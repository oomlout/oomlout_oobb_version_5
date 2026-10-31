"""Palletizable Gridfinity pot with an inset lower wall and printable flare."""
import copy
import math
from pathlib import Path

NAME = "gridfinity_palet_pot"
WRAPPER = str(Path(__file__).with_name("gridfinity_palet_pot.scad"))

def define():
    return dict(name=NAME, name_long="Gridfinity: Palletizable Pot",
        shape_aliases=[NAME], category="Gridfinity",
        description="Solid Gridfinity base with an inset lower wall, support-free flare and four optional corner label pads.",
        notes=["Dimensions use millimetres except width and height, which use 42 mm Gridfinity units.",
               "The standard feet join through a solid base bridge. The flare and label supports are support-free.",
               "label_size sets four square corner label pads below the rim; set it to 0 to omit them."],
        variables=[dict(name=n, description=d, type="number", default=v) for n,d,v in [
            ("gridfinity_width","Footprint width in Gridfinity units.",1),
            ("gridfinity_height","Footprint height in Gridfinity units.",1),
            ("height_mm","Total height above the feet in millimetres.",17),
            ("inset_mm","Inset from each outside edge where the lower wall starts.",5),
            ("flare_from_top_mm","Distance below the top where the flare begins.",12),
            ("wall_thickness","Wall thickness in millimetres.",1.2),
            ("label_size","Square label pad side length at each of the four corners.",10),
            ("label_drop_mm","How far the label pads sit below the upper rim.",5.75),
            ("base_bridge_mm","Solid bridge thickness above the standard Gridfinity feet.",1),
        ]]+[dict(name="pos",description="XYZ position in millimetres.",type="list",default=[0,0,0]),
             dict(name="rot",description="XYZ rotation in degrees.",type="list",default=[0,0,0])])

def describe(): return define()

def action(**kwargs):
    # Related tooling modules live in the tray SCAD source and component action.
    # This keeps one project-specific OOBB component registration.
    mode = kwargs.get("component_mode", "tray")
    if mode in ("top_pickup", "fork_pallet_twist"):
        if mode == "fork_pallet_twist":
            width = float(kwargs.get("gridfinity_width", kwargs.get("width", 1)))
            height = float(kwargs.get("gridfinity_height", kwargs.get("height", 2)))
            bearing_clearance = float(kwargs.get("bearing_fit_clearance_mm", 0.2))
            fit_clearance = float(kwargs.get("twist_fit_clearance_mm", 1.0))
            return dict(type=kwargs.get("type", kwargs.get("t", "positive")),
                shape="raw_scad", file=WRAPPER, module="gridfinity_fork_pallet_twist",
                module_kwargs=dict(gridfinity_width=width, gridfinity_height=height,
                    bearing_od=27.4, bearing_width=3.6,
                    bearing_fit_clearance=bearing_clearance,
                    fit_clearance_mm=fit_clearance, fork_angle=180,
                    print_layout=True),
                pos=copy.deepcopy(kwargs.get("pos", [0, 0, 0])),
                rot=copy.deepcopy(kwargs.get("rot", [0, 0, 0])),
                inclusion=kwargs.get("inclusion", "all"), m=kwargs.get("m", ""))
        def pickup_number(key, default):
            value = float(kwargs.get(key, default))
            if not math.isfinite(value):
                raise ValueError(key + " must be finite")
            return value
        width = pickup_number("gridfinity_width", 1)
        height = pickup_number("gridfinity_height", 1)
        height_mm = pickup_number("height_mm", 17)
        label_size = pickup_number("label_size", 10)
        label_drop = pickup_number("label_drop_mm", 5.75)
        clearance = pickup_number("clearance_mm", 0.5)
        overlap = pickup_number("contact_overlap", 0.05)
        if min(width, height) < 1 or min(height_mm, label_size) <= 0 or clearance < 0 or overlap < 0:
            raise ValueError("Pickup dimensions must be positive and clearances cannot be negative")
        if label_size < 8:
            raise ValueError("label_size must be at least 8 mm for the pickup hooks")
        return dict(type=kwargs.get("type", kwargs.get("t", "positive")),
            shape="raw_scad", file=WRAPPER, module="gridfinity_top_pickup",
            module_kwargs=dict(gridfinity_width=width, gridfinity_height=height,
                height_mm=height_mm, label_size=label_size,
                label_drop_mm=label_drop, clearance_mm=clearance,
                engaged=kwargs.get("engaged", False),
                draw_handle=kwargs.get("draw_handle", True),
                print_layout=kwargs.get("print_layout", True),
                contact_overlap=overlap),
            pos=copy.deepcopy(kwargs.get("pos", [0, 0, 0])),
            rot=copy.deepcopy(kwargs.get("rot", [0, 0, 0])),
            inclusion=kwargs.get("inclusion", "all"), m=kwargs.get("m", ""))
    def number(key, default):
        aliases={"gridfinity_width":"width","gridfinity_height":"height","height_mm":"depth"}
        value=float(kwargs.get(key, kwargs.get(aliases.get(key,""), default)))
        if not math.isfinite(value): raise ValueError(key+" must be finite")
        return value
    w=number("gridfinity_width",1); h=number("gridfinity_height",1)
    height=number("height_mm",17); inset=number("inset_mm",5)
    flare=number("flare_from_top_mm",12); wall=number("wall_thickness",1.2); label=number("label_size",10)
    label_drop=number("label_drop_mm",5.75); bridge=number("base_bridge_mm",1)
    if min(w,h)<=0 or height<4.75+bridge+inset or inset<0 or flare<0 or wall<=0 or wall>=1.9 or label<0 or label_drop<0 or bridge<=0:
        raise ValueError("Pot dimensions must be positive; height must allow the base bridge and inset wall")
    if height-label_drop<=4.75+bridge:
        raise ValueError("label_drop_mm places the label pads below the wall origin")
    return dict(type=kwargs.get("type",kwargs.get("t","positive")),shape="raw_scad",file=WRAPPER,
        module="gridfinity_palet_pot",module_kwargs=dict(gridfinity_width=w,gridfinity_height=h,
        height_mm=height,inset_mm=inset,flare_from_top_mm=flare,wall_thickness=wall,label_size=label,
        label_drop_mm=label_drop,base_bridge_mm=bridge),
        pos=copy.deepcopy(kwargs.get("pos",[0,0,0])),rot=copy.deepcopy(kwargs.get("rot",[0,0,0])),
        inclusion=kwargs.get("inclusion","all"),m=kwargs.get("m",""))
