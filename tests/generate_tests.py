import os
import opsc
import oobb
import oobb_get_items_base as base
import oobb_get_items_other as other
import oobb_get_items_oobb as oobb_items
import oobb_get_items_oobb_other as oobb_other

def ensure(path):
    os.makedirs(path, exist_ok=True)

def run_case(name, idx, objs):
    if isinstance(objs, dict) and 'components' in objs:
        objs = objs['components']
    path = os.path.join('test', f'{name}_index_{idx}')
    ensure(path)
    opsc.opsc_make_object(os.path.join(path, 'working.scad'), objs, mode='3dpr', save_type='none')

    # Dump the generated object as yaml and json for comparison
    import json
    import yaml

    yaml_path = os.path.join(path, 'item.yaml')
    json_path = os.path.join(path, 'item.json')

    with open(yaml_path, 'w') as f:
        yaml.dump(objs, f, indent=2)

    with open(json_path, 'w') as f:
        json.dump(objs, f, indent=2)

    # Verify that reloaded yaml and json are identical
    with open(yaml_path) as f_yaml, open(json_path) as f_json:
        yaml_data = yaml.safe_load(f_yaml)
        json_data = json.load(f_json)

    assert yaml_data == json_data, f"YAML and JSON mismatch for {name} case {idx}"

def main():
    cases = {
        'oobb_cube_center': (
            base.get_oobb_cube_center,
            [
                {'type':'p','size':[15,15,15],'pos':[0,0,0]},
                {'type':'p','size':[20,10,5],'pos':[5,0,0]},
                {'type':'p','size':[10,5,10],'pos':[-5,-5,0]},
            ]
        ),
        'oobb_cylinder': (
            base.get_oobb_cylinder,
            [
                {'type':'p','radius':5,'depth':10,'pos':[0,0,0]},
                {'type':'p','radius_name':'hole_radius_m6','depth':8,'pos':[5,0,0]},
                {'type':'p','r1':6,'r2':3,'depth':15,'pos':[0,5,0]},
            ]
        ),
        'oobb_rounded_rectangle_hollow': (
            base.get_oobb_rounded_rectangle_hollow,
            [
                {'type':'p','size':[20,10,5],'pos':[0,0,0],'wall_thickness':2},
                {'type':'p','size':[15,15,5],'radius':3,'wall_thickness':2},
                {'type':'p','size':[20,10,5],'r1':5,'r2':3,'wall_thickness':1},
            ]
        ),
        'bolt': (
            other.get_bolt,
            [
                {'type':'bolt','radius_name':'m6','depth':12},
                {'type':'bolt','radius_name':'m6','depth':20},
                {'type':'bolt','radius_name':'m8','depth':16},
            ]
        ),
        'nut': (
            other.get_nut,
            [
                {'type':'nut','radius_name':'m6'},
                {'type':'nut','radius_name':'m8'},
                {'type':'nut','radius_name':'m5'},
            ]
        ),
        'screw_countersunk': (
            other.get_screw_countersunk,
            [
                {'type':'screw_countersunk','radius_name':'m6','depth':16},
                {'type':'screw_countersunk','radius_name':'m6','depth':12},
                {'type':'screw_countersunk','radius_name':'m3','depth':10},
            ]
        ),
       'standoff': (
           other.get_standoff,
           [
                {'type':'standoff','radius_name':'m3','depth':10},
                {'type':'standoff','radius_name':'m3','depth':15},
                {'type':'standoff','radius_name':'m3','depth':20},
            ]
        ),
       'threaded_insert': (
           other.get_threaded_insert,
           [
                {'type':'threaded_insert','radius_name':'m3','style':'01'},
                {'type':'threaded_insert','radius_name':'m3','style':'01'},
                {'type':'threaded_insert','radius_name':'m3','style':'01'},
            ]
        ),
        'bearing': (
            other.get_bearing,
            [
                {'type':'bearing','bearing_name':'6705'},
                {'type':'bearing','bearing_name':'6704'},
                {'type':'bearing','bearing_name':'6800'},
            ]
        ),
        'plate': (
            oobb_items.get_plate,
            [
                {'type':'plate','width':3,'height':3,'thickness':3},
                {'type':'plate','width':5,'height':2,'thickness':3},
                {'type':'plate','width':6,'height':4,'thickness':3},
            ]
        ),
        'plate_l': (
            oobb_items.get_plate_l,
            [
                {'type':'plate_l','width':3,'height':3,'thickness':3},
                {'type':'plate_l','width':4,'height':4,'thickness':3},
                {'type':'plate_l','width':5,'height':5,'thickness':3},
            ]
        ),
        'other_bolt_stacker': (
            oobb_other.get_other_bolt_stacker,
            [
                {'type':'other_bolt_stacker','width':3,'height':3,'thickness':3},
                {'type':'other_bolt_stacker','width':4,'height':4,'thickness':3},
                {'type':'other_bolt_stacker','width':5,'height':5,'thickness':3},
            ]
        ),
        'other_corner_cube': (
            oobb_other.get_other_corner_cube,
            [
                {'type':'other_corner_cube','width':3,'height':3,'thickness':3},
                {'type':'other_corner_cube','width':4,'height':4,'thickness':3},
                {'type':'other_corner_cube','width':5,'height':5,'thickness':3},
            ]
        ),
        'other_ptfe_tube_holder': (
            oobb_other.get_other_ptfe_tube_holder,
            [
                {'type':'other_ptfe_tube_holder','width':3,'height':3,'thickness':3},
                {'type':'other_ptfe_tube_holder','width':4,'height':4,'thickness':3},
                {'type':'other_ptfe_tube_holder','width':5,'height':5,'thickness':3},
            ]
        ),
        'other_timing_belt_clamp_gt2': (
            oobb_other.get_other_timing_belt_clamp_gt2,
            [
                {'type':'other_timing_belt_clamp_gt2','width':3,'height':3,'thickness':3},
                {'type':'other_timing_belt_clamp_gt2','width':4,'height':4,'thickness':3},
                {'type':'other_timing_belt_clamp_gt2','width':5,'height':5,'thickness':3},
            ]
        ),
    }
    for name,(func, params_list) in cases.items():
        for idx, params in enumerate(params_list,1):
            objs = func(**params)
            print(f"    running {name} case {idx}")
            run_case(name, idx, objs)

if __name__ == '__main__':
    main()
