"""Standard stacking lip variant of the independently named 0.4 mm nozzle tub."""
from components.gridfinity_tub_nozzle_04_no_lip import working as tub

def describe():
    return tub.metadata(True)

def define():
    return describe()

def action(**kwargs):
    return tub.make(True, **kwargs)
