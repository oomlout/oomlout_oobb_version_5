"""Standard stacking lip variant of the independently named 0.8 mm nozzle tub."""
from components.gridfinity_tub_nozzle_08_no_lip import working as tub

def describe():
    return tub.metadata(True)

def define():
    return describe()

def action(**kwargs):
    return tub.make(True, **kwargs)
