import copy
import oobb_base
import math

# gear
def get_test_gear(**kwargs):
    # default sets
    style = kwargs.get("style", "socket_cap")
    kwargs.pop("style","")
    pos = kwargs.get("pos", [0, 0, 0])    
    full_object = kwargs.get("full_object", True)
        
    # extra sets
    kwargs["pos"] = pos
    
    # get the default thing
    thing = oobb_base.get_default_thing(**kwargs)
    kwargs.pop("size","")    
    kwargs.pop("extra","")
    kwargs.pop("type","")
    
    pos_current = [0,0,0]
    pos_shift = 100
    comment_extra = ""
    thickness = 3

    versions = []
    base = {}    
    base["shape"] = f"gear"  
    base["type"] = "p"   
    base["shape"] = f"gear"
    base["diametral_pitch"] = 0.53333333
    base["number_of_teeth"] = 3 * 8  
    base["depth"] = thickness
    base["pos"] = pos_current
    base["comment_extra"] = ""
    base["comment_display"] = True
    base["comment_shift_line"] = 30
    #base["m"] = ""
    base["extra"] = {}

    versions.append(copy.deepcopy(base))

    """ variables to play with
    number_of_teeth = params.get("number_of_teeth", 24)
    circular_pitch = params.get("circular_pitch", False) # couldn't figure this one out
    diametral_pitch = params.get("diametral_pitch", 0.533333) #(teeth / diameter mm) gear 15 mm wide has 8 teeth
    pressure_angle = params.get("pressure_angle", 28)
    clearance = params.get("clearance", 1)
    gear_thickness = params.get("gear_thickness", 6)
    rim_thickness = params.get("rim_thickness", gear_thickness)
    rim_width = params.get("rim_width", 0)
    hub_thickness = params.get("hub_thickness", 0)
    hub_diameter = params.get("hub_diameter", 0)
    bore_diameter = params.get("bore_diameter", 0)
    circles = params.get("circles", 0)
    backlash = params.get("backlash", 1)
    twist = params.get("twist", 0)
    involute_facets = params.get("involute_facets", 0)
    flat = params.get("flat", False)
    """

    b = copy.deepcopy(base)

    #versions.append(b)
    
    
    tests = {}
    tests["pressure_angle"] = [0,14.5, 20, 25, 28, 30, 35,60]
    tests["clearance"] = [0, 0.5, 1, 5]
    tests["backlash"] = [0, 0.5, 1, 2, -1]

    a_extra = "clearance"    
    b_extra = "backlash"                     
    
    for b in tests[a_extra]:        
        for a in tests[b_extra]:            
            for v in versions:                       
                    p3 = copy.deepcopy(v)
                    comment_extra = v["comment_extra"]                     
                    comment_extra += f" {a_extra} : {a}\n"
                    comment_extra += f" {b_extra} : {b}"

                    depth = v["depth"]            
                    p3["comment"] = f"{v['shape']}_{depth}\n{comment_extra}"
                    p3["pos"] = copy.deepcopy(pos_current)
                    p3[b_extra] = b
                    p3[a_extra] = a
                    p3["m"] = ""
                    extra = v.get("extra", {})
                    p3.update(extra)
                    oobb_base.append_full(thing, **p3)
                    pos_current[1] += pos_shift
        pos_current[0] += pos_shift
        pos_current[1] = 0    
    pos_current[0] += pos_shift

    if full_object:   
        return thing
    else: # only return the elements
        return thing["components"]

#hole
def get_test_hole(**kwargs):
    # default sets
    style = kwargs.get("style", "socket_cap")
    kwargs.pop("style","")
    pos = kwargs.get("pos", [0, 0, 0])    
    full_object = kwargs.get("full_object", True)
    hole_size = kwargs.get("shaft", 3)    
    increment = kwargs.get("bearing", 0.5)



    # extra sets
    kwargs["pos"] = pos
    
    # get the default thing
    thing = oobb_base.get_default_thing(**kwargs)
    kwargs.pop("size","")    
    kwargs.pop("extra","")
    kwargs.pop("type","")
    width = kwargs.get("width", 3)
    height = kwargs.get("height", 3)


    pos_current = [0,0,0]
    pos_shift = 15
    comment_extra = ""
    thickness = kwargs.get("thickness", 3)

    #main_plate
    p3 = copy.deepcopy(kwargs)
    p3["shape"] = f"oobb_plate"
    p3["type"] = "positive"
    p3["width"] = width
    p3["height"] = height
    p3["depth"] = thickness
    oobb_base.append_full(thing, **p3)

    #hole test
    wid = width
    hei = height
    extra = -increment * 4
    for w in range(0,wid):
        for h in range(0,hei):
            p3 = copy.deepcopy(kwargs)
            p3["shape"] = f"oobb_hole"
            p3["type"] = "negative"
            p3["width"] = wid
            p3["height"] = hei
            p3["depth"] = 3
            x = (w*15) - math.floor(wid/2) * 15
            y = (h*15) - math.floor(hei/2) * 15
            pos1 = copy.deepcopy(p3["pos"])
            pos1[0] += x
            pos1[1] += y
            p3["pos"] = pos1
            p3["radius"] = (hole_size + extra) / 2
            oobb_base.append_full(thing, **p3)
            extra += increment
        






    

    if full_object:   
        return thing
    else: # only return the elements
        return thing["components"]
    

# rotation
def get_test_rotation(**kwargs):
    # default sets
    width = 5
    height = 5
    thickness = kwargs.get("thickness", 3)
    size = kwargs.get("size", "oobb")
    pos = kwargs.get("pos", [0, 0, 0])
    extra = kwargs.get("extra", "")
    
    full_object = kwargs.get("full_object", True)
        
    # extra sets
    holes = kwargs.get("holes", True)
    both_holes = kwargs.get("both_holes", False)
    kwargs["pos"] = pos
    
    

    # get the default thing
    thing = oobb_base.get_default_thing(**kwargs)
    kwargs.pop("size","")    
    kwargs.pop("extra","")
    
    pos_current = [0,0,0]
    pos_shift = 30    
    comment_extra = ""
    #basic     
    
    item = "oobb_screw_socket_cap_shape_m3_radius_name_12_mm_depth"
    p3 = copy.deepcopy(kwargs)
    p3["comment"] = f"{item}{comment_extra}\n"
    p3["pos"] = copy.deepcopy(pos_current)
    p3["item"] = item
    p3["m"] = ""
    oobb_base.append_full(thing, **p3)
    
    ########################### rot_y

    pos_current = [300,0,0]
    pos_shift = 30    
    comment_extra = " rot_y : 180"
    #basic     
    
    item = "oobb_screw_socket_cap_shape_m3_radius_name_12_mm_depth"
    p3 = copy.deepcopy(kwargs)
    p3["comment"] = f"{item}{comment_extra}\n"
    p3["pos"] = copy.deepcopy(pos_current)
    p3["item"] = item
    p3["rot_y"] = 180
    p3["m"] = ""
    oobb_base.append_full(thing, **p3)
    
    
    if full_object:   
        return thing
    else: # only return the elements
        return thing["components"]

# motor

#      motor_tt_01
def get_test_motor_tt_01(**kwargs):
    # default sets    
    kwargs.pop("style","")
    pos = kwargs.get("pos", [0, 0, 0])    
    full_object = kwargs.get("full_object", True)
        
    # extra sets
    kwargs["pos"] = pos
    
    # get the default thing
    thing = oobb_base.get_default_thing(**kwargs)
    kwargs.pop("size","")    
    kwargs.pop("extra","")
    kwargs.pop("type","")
    
    pos_current = [0,0,0]
    pos_shift = 15
    comment_extra = ""
    thickness = 3

    #oobb plate
    p3 = copy.deepcopy(kwargs)
    p3["shape"] = f"oobb_plate"
    p3["type"] = "p"
    p3["width"] = 1.5
    p3["height"] = 5
    p3["depth"] = 7
    pos1 = copy.deepcopy(p3["pos"])
    pos1[2] += -6
    p3["pos"] = pos1
    #oobb_base.append_full(thing, **p3)

    versions = []
    base = {}    
    base["type"] = "p"   
    base["shape"] = f"oobb_motor_tt_01" 
    base.pop("clearance","") 
    #base["part"] = f"shaft"    
    #base["depth"] = 50
    base["pos"] = pos_current
    base["comment_extra"] = ""
    #base["comment_display"] = True
    base["comment_shift_line"] = 30
    #base["m"] = "#"
    base["extra"] = {}

    versions.append(copy.deepcopy(base))

    b = copy.deepcopy(base)

    #versions.append(b)
    
    
    tests = {}
    tests["radius_extra"] = [0]
    
    a_extra = "radius_extra"    
    #b_extra = "backlash"                     
    
    #for b in tests[a_extra]:        
    for a in tests[a_extra]:            
        for v in versions:                       
                p3 = copy.deepcopy(v)
                comment_extra = v["comment_extra"]                     
                comment_extra += f" {a_extra} : {a}\n"
                #comment_extra += f" {b_extra} : {b}"

                extra_detail_a = a
                p3["comment"] = f"{v['shape']}_{a}_{extra_detail_a}\n{comment_extra}"
                p3["pos"] = copy.deepcopy(pos_current)
                #p3[b_extra] = b
                p3[a_extra] = a
                #p3["m"] = ""
                extra = v.get("extra", {})
                p3.update(extra)
                oobb_base.append_full(thing, **p3)
                pos_current[1] += pos_shift
    pos_current[0] += pos_shift
    pos_current[1] = 0    


    if full_object:   
        return thing
    else: # only return the elements
        return thing["components"]


#      motor_tt_01_shaft
def get_test_motor_tt_01_shaft(**kwargs):
    # default sets    
    kwargs.pop("style","")
    pos = kwargs.get("pos", [0, 0, 0])    
    full_object = kwargs.get("full_object", True)
        
    # extra sets
    kwargs["pos"] = pos
    
    # get the default thing
    thing = oobb_base.get_default_thing(**kwargs)
    kwargs.pop("size","")    
    kwargs.pop("extra","")
    kwargs.pop("type","")
    
    pos_current = [0,-30,0]
    pos_shift = 15
    comment_extra = ""
    thickness = 3

    #oobb plate
    p3 = copy.deepcopy(kwargs)
    p3["shape"] = f"oobb_plate"
    p3["type"] = "p"
    p3["width"] = 1.5
    p3["height"] = 5
    p3["depth"] = 7
    pos1 = copy.deepcopy(p3["pos"])
    pos1[2] += -6
    p3["pos"] = pos1
    oobb_base.append_full(thing, **p3)

    versions = []
    base = {}    
    base["type"] = "n"   
    base["shape"] = f"oobb_motor_tt_01"  
    base["part"] = f"shaft"    
    base["depth"] = 50
    base["pos"] = pos_current
    base["comment_extra"] = ""
    #base["comment_display"] = True
    base["comment_shift_line"] = 30
    #base["m"] = "#"
    base["extra"] = {}

    versions.append(copy.deepcopy(base))

    b = copy.deepcopy(base)

    #versions.append(b)
    
    
    tests = {}
    tests["radius_extra"] = [0,0.1,0.2,0.3,0.4]
    
    a_extra = "radius_extra"    
    #b_extra = "backlash"                     
    
    #for b in tests[a_extra]:        
    for a in tests[a_extra]:            
        for v in versions:                       
                p3 = copy.deepcopy(v)
                comment_extra = v["comment_extra"]                     
                comment_extra += f" {a_extra} : {a}\n"
                #comment_extra += f" {b_extra} : {b}"

                extra_detail_a = a
                p3["comment"] = f"{v['shape']}_{a}_{extra_detail_a}\n{comment_extra}"
                p3["pos"] = copy.deepcopy(pos_current)
                #p3[b_extra] = b
                p3[a_extra] = a
                #p3["m"] = ""
                extra = v.get("extra", {})
                p3.update(extra)
                oobb_base.append_full(thing, **p3)
                pos_current[1] += pos_shift
    pos_current[0] += pos_shift
    pos_current[1] = 0    


    if full_object:   
        return thing
    else: # only return the elements
        return thing["components"]


#      motor_n20_shaft
def get_test_motor_n20_shaft(**kwargs):
    # default sets
    style = kwargs.get("style", "socket_cap")
    kwargs.pop("style","")
    pos = kwargs.get("pos", [0, 0, 0])    
    full_object = kwargs.get("full_object", True)
        
    # extra sets
    kwargs["pos"] = pos
    
    # get the default thing
    thing = oobb_base.get_default_thing(**kwargs)
    kwargs.pop("size","")    
    kwargs.pop("extra","")
    kwargs.pop("type","")
    
    pos_current = [0,-30,0]
    pos_shift = 15
    comment_extra = ""
    thickness = 3

    #oobb plate
    p3 = copy.deepcopy(kwargs)
    p3["shape"] = f"oobb_plate"
    p3["type"] = "p"
    p3["width"] = 1.5
    p3["height"] = 5
    p3["depth"] = 3
    oobb_base.append_full(thing, **p3)

    versions = []
    base = {}    
    base["type"] = "n"   
    base["shape"] = f"oobb_motor_n20"  
    base["part"] = f"shaft"    
    base["pos"] = pos_current
    base["comment_extra"] = ""
    #base["comment_display"] = True
    base["comment_shift_line"] = 30
    #base["m"] = ""
    base["extra"] = {}

    versions.append(copy.deepcopy(base))

    b = copy.deepcopy(base)

    #versions.append(b)
    
    
    tests = {}
    tests["radius_extra"] = [0,0.1,0.2,0.3,0.4]
    
    a_extra = "radius_extra"    
    #b_extra = "backlash"                     
    
    #for b in tests[a_extra]:        
    for a in tests[a_extra]:            
        for v in versions:                       
                p3 = copy.deepcopy(v)
                comment_extra = v["comment_extra"]                     
                comment_extra += f" {a_extra} : {a}\n"
                #comment_extra += f" {b_extra} : {b}"

                extra_detail_a = a
                p3["comment"] = f"{v['shape']}_{a}_{extra_detail_a}\n{comment_extra}"
                p3["pos"] = copy.deepcopy(pos_current)
                #p3[b_extra] = b
                p3[a_extra] = a
                p3["m"] = ""
                extra = v.get("extra", {})
                p3.update(extra)
                oobb_base.append_full(thing, **p3)
                pos_current[1] += pos_shift
    pos_current[0] += pos_shift
    pos_current[1] = 0    


    if full_object:   
        return thing
    else: # only return the elements
        return thing["components"]

#      motor_servo_standard_01
def get_test_oobb_motor_servo_standard_01(**kwargs):
    # default sets
    pos = kwargs.get("pos", [0, 0, 0])
    
    full_object = kwargs.get("full_object", True)
        
    # extra sets
    kwargs["pos"] = pos
    
    

    # get the default thing
    thing = oobb_base.get_default_thing(**kwargs)
    kwargs.pop("size","")    
    kwargs.pop("extra","")
    kwargs.pop("type","")
    
    pos_current = [0,0,0]
    pos_shift = 150    
    comment_extra = ""
    
    versions = []
    base = {}    
    base["shape"] = "oobb_motor_servo_standard_01"
    base["comment_extra"] = ""
    base["m"] = ""
    base["extra"] = {}

    versions.append(copy.deepcopy(base))

    b = copy.deepcopy(base)
    b["extra"]["rot_y"] = 180
    b["comment_extra"] = " rot_y : 180"
    versions.append(b)
    
    b = copy.deepcopy(base)
    b["extra"]["rot_y"] = 90
    b["comment_extra"] = " rot_y : 90"
    versions.append(b)


    b = copy.deepcopy(base)
    b["extra"]["rot_x"] = 90
    b["comment_extra"] = " rot_x : 90"
    versions.append(b)

    
    b = copy.deepcopy(base)
    b["extra"]["screw_rot_y"] = True
    b["comment_extra"] = " screw_rot_y : True"
    versions.append(b)

    for v in versions:                        
        p3 = copy.deepcopy(kwargs)
        comment_extra = v["comment_extra"]
        p3["shape"] = v["shape"] 
        p3["type"] = "positive"
        p3["comment"] = f"{v['shape']}{comment_extra}\n"
        p3["pos"] = copy.deepcopy(pos_current)
        p3["m"] = ""
        p3.update(v["extra"])
        oobb_base.append_full(thing, **p3)
        pos_current[1] += pos_shift
    
    
    

    if full_object:   
        return thing
    else: # only return the elements
        return thing["components"]

#nut
def get_test_oobb_nut(**kwargs):
    # default sets
    kwargs.pop("style","")
    pos = kwargs.get("pos", [0, 0, 0])    
    full_object = kwargs.get("full_object", True)
        
    # extra sets
    kwargs["pos"] = pos
    
    # get the default thing
    thing = oobb_base.get_default_thing(**kwargs)
    kwargs.pop("size","")    
    kwargs.pop("extra","")
    kwargs.pop("type","")
    
    pos_current = [0,0,0]
    pos_shift = 50
    comment_extra = ""
    
    versions = []
    base = {}    
    base["shape"] = f"oobb_nut"
    base["radius_name"] = "m3"
    base["comment_extra"] = ""
    base["comment_display"] = True
    #base["m"] = ""
    base["extra"] = {}

    versions.append(copy.deepcopy(base))

    

    
    b = copy.deepcopy(base)    
    b["extra"]["overhang"] = True
    b["comment_extra"] = "overhang : True\n"
    versions.append(b)

    b = copy.deepcopy(base)    
    b["extra"]["overhang"] = True
    b["extra"]["hole"] = True
    b["comment_extra"] = "overhang : True hole: True\n"
    versions.append(b)


    b = copy.deepcopy(base)    
    b["extra"]["zz"] = "top"
    b["comment_extra"] = "zz : top\n"
    versions.append(b)

    #zz bottom
    b = copy.deepcopy(base)
    b["extra"]["zz"] = "bottom"
    b["comment_extra"] = "zz : bottom\n"
    versions.append(b)

    #zz middle
    b = copy.deepcopy(base)
    b["extra"]["zz"] = "middle"
    b["comment_extra"] = "zz : middle\n"
    versions.append(b)

    #longer
    b = copy.deepcopy(base)    
    b["extra"]["depth"] = 25
    b["comment_extra"] = "depth : 25\n"
    versions.append(b)

    b = copy.deepcopy(base)    
    b["extra"]["zz"] = "top"
    b["extra"]["depth"] = 25
    b["comment_extra"] = "zz : top depth : 25\n"
    versions.append(b)

    #zz middle
    b = copy.deepcopy(base)
    b["extra"]["zz"] = "middle"
    b["extra"]["depth"] = 25
    b["comment_extra"] = "zz : middle depth : 25\n"
    versions.append(b)

    #clearance top
    b = copy.deepcopy(base)
    b["extra"]["clearance"] = "top"
    b["comment_extra"] = "clearance : top\n"
    versions.append(b)

    #clearance bottom
    b = copy.deepcopy(base)
    b["extra"]["clearance"] = "bottom"
    b["comment_extra"] = "clearance : bottom\n"
    versions.append(b)

    #loose
    b = copy.deepcopy(base)    
    b["extra"]["extra"] = "loose"
    b["comment_extra"] = "extra : loose\n"
    #versions.append(b)

    #tight
    b = copy.deepcopy(base)
    b["extra"]["extra"] = "tight"
    b["comment_extra"] = "extra : tight\n"
    #versions.append(b)


    rots = []
    rots.append([[0,0,0], {}, ""])
    rots.append([[150,0,0], {"rot":[0,360/12,0]}, "rot_y : 360/12"])
    rots.append([[300,0,0], {"rot":[0,90,0]}, "rot_y : 90"])
    rots.append([[450,0,0], {"rot":[90,45,0]}, "rot_x : 90 rot_y : 45"])

    for r in rots:
        pos_current = r[0]
        extra_extra = r[1]
        comment_extra_extra = r[2]

        for v in versions:                        
            p3 = copy.deepcopy(kwargs)
            comment_extra = v["comment_extra"]
            p3["shape"] = v["shape"] 
            p3["type"] = "positive"
            radius_name = v["radius_name"]
            p3["radius_name"] = radius_name            
            p3["comment"] = f"{v['shape']}_{radius_name}\n{comment_extra}{comment_extra_extra}"
            comment_display = v.get("comment_display", False)
            p3["comment_display"]   = comment_display
            p3["pos"] = copy.deepcopy(pos_current)
            rot = v.get("rot", [0,0,0])
            p3["rot"] = rot
            p3["m"] = ""
            p3.update(v["extra"])
            p3.update(extra_extra)
            oobb_base.append_full(thing, **p3)
            pos_current[1] += pos_shift
        
        
    

    if full_object:   
        return thing
    else: # only return the elements
        return thing["components"]


# screw
def get_test_oobb_screw_socket_cap(**kwargs):
    kwargs["style"] =  "socket_cap"
    return get_test_oobb_screw(**kwargs)

def get_test_oobb_screw_countersunk(**kwargs):
    kwargs["style"] =  "countersunk"
    return get_test_oobb_screw(**kwargs)

def get_test_oobb_screw_self_tapping(**kwargs):
    kwargs["style"] =  "self_tapping"
    return get_test_oobb_screw(**kwargs)

def get_test_oobb_screw(**kwargs):
    # default sets
    style = kwargs.get("style", "socket_cap")
    kwargs.pop("style","")
    pos = kwargs.get("pos", [0, 0, 0])    
    full_object = kwargs.get("full_object", True)
        
    # extra sets
    kwargs["pos"] = pos
    
    # get the default thing
    thing = oobb_base.get_default_thing(**kwargs)
    kwargs.pop("size","")    
    kwargs.pop("extra","")
    kwargs.pop("type","")
    
    pos_current = [0,0,0]
    pos_shift = 30
    comment_extra = ""
    
    versions = []
    base = {}    
    base["shape"] = f"oobb_screw_{style}"
    base["radius_name"] = "m3"
    base["depth"] = 12
    base["comment_extra"] = ""
    base["comment_display"] = True
    #base["m"] = ""
    base["extra"] = {}

    versions.append(copy.deepcopy(base))

    b = copy.deepcopy(base)
    b["extra"]["nut"] = True
    b["comment_extra"] = "nut : True"
    versions.append(b)
    
    b = copy.deepcopy(base)
    b["extra"]["nut"] = True
    b["extra"]["overhang"] = True
    b["comment_extra"] = "nut : True overhang : True"
    versions.append(b)
    
    b = copy.deepcopy(base)
    b["extra"]["zz"] = "top"
    b["comment_extra"] = "zz : top"
    versions.append(b)
    
    b = copy.deepcopy(base)
    b["extra"]["zz"] = "bottom"
    b["comment_extra"] = "zz : bottom"
    versions.append(b)

    
    b = copy.deepcopy(base)
    b["extra"]["zz"] = "top"
    b["extra"]["nut"] = True
    b["comment_extra"] = "zz : top nut : True"
    versions.append(b)
    
    b = copy.deepcopy(base)
    b["extra"]["zz"] = "bottom"
    b["extra"]["nut"] = True
    b["comment_extra"] = "zz : bottom nut : True"
    versions.append(b)
    
    b = copy.deepcopy(base)
    b["extra"]["zz"] = "bottom"
    b["extra"]["nut"] = True
    b["extra"]["rot_y"] = 180
    b["comment_extra"] = "zz : top nut : True rot_y : 180"
    versions.append(b)
    
    b = copy.deepcopy(base)
    b["extra"]["clearance"] = "top"
    b["comment_extra"] = "clearance : top"
    versions.append(b)
    
    b = copy.deepcopy(base)
    b["extra"]["clearance"] = "bottom"
    b["comment_extra"] = "clearance : bottom"
    versions.append(b)

    
    b = copy.deepcopy(base)
    b["extra"]["clearance"] = "bottom"
    b["extra"]["nut"] = True
    b["comment_extra"] = "clearance : bottom nut : True"
    versions.append(b)
    
    
    b = copy.deepcopy(base)
    b["extra"]["clearance"] = ["top","bottom"]
    b["extra"]["nut"] = True
    b["comment_extra"] = "clearance : [top , bottom] nut : True"
    versions.append(b)
    
    
    b = copy.deepcopy(base)
    b["extra"]["clearance"] = ["top","bottom"]
    b["extra"]["nut"] = True
    b["extra"]["zz"] = "top"
    b["comment_extra"] = "clearance : [top , bottom] nut : True zz : top"
    versions.append(b)

    b = copy.deepcopy(base)
    b["extra"]["clearance"] = ["top","bottom"]
    b["extra"]["nut"] = True
    b["extra"]["zz"] = "bottom"
    b["comment_extra"] = "clearance : [top , bottom] nut : True zz : bottom"
    versions.append(b)
    

    ########################### rot_y

    pos_current = [300,0,0]
    pos_shift = 30    
    comment_extra = " rot_y : 180"
    #basic     


    ########################### rot_y 90

    pos_current = [600,0,0]
    pos_shift = 30    
    comment_extra = " rot_y : 90"

    ########################### rot_x 180

    pos_current = [900,0,0]
    pos_shift = 60    
    comment_extra = " rot_x : 180"

    ########################### rot_x 90 rot_y 90

    pos_current = [1500,0,0]
    pos_shift = 60    
    comment_extra = " rot_x : 90 rot_y : 90 rot_z : 90"

    rots = []
    rots.append([[0,0,0], {}, ""])
    rots.append([[150,0,0], {"rot_y":180}, "rot_y : 180"])
    rots.append([[300,0,0], {"rot_y":90}, "rot_y : 90"])
    rots.append([[450,0,0], {"rot_x":45, "rot_y": 45}, "rot_x : 90 rot_y : 45"])

    for r in rots:
        pos_current = r[0]
        extra_extra = r[1]
        comment_extra_extra = r[2]

        for v in versions:                        
            p3 = copy.deepcopy(kwargs)
            comment_extra = v["comment_extra"]
            p3["shape"] = v["shape"] 
            p3["type"] = "positive"
            radius_name = v["radius_name"]
            p3["radius_name"] = radius_name
            depth = v["depth"]
            p3["depth"] = depth
            p3["comment"] = f"{v['shape']}_{radius_name}_{depth}\n{comment_extra}{comment_extra_extra}"
            comment_display = v.get("comment_display", False)
            p3["comment_display"]   = comment_display
            p3["pos"] = copy.deepcopy(pos_current)
            p3["m"] = ""
            p3.update(v["extra"])
            p3.update(extra_extra)
            oobb_base.append_full(thing, **p3)
            pos_current[1] += pos_shift
        
        
    

    if full_object:   
        return thing
    else: # only return the elements
        return thing["components"]

def get_test_oobb_screw_socket_cap_old_1(**kwargs):
    # default sets
    width = 5
    height = 5
    thickness = kwargs.get("thickness", 3)
    size = kwargs.get("size", "oobb")
    pos = kwargs.get("pos", [0, 0, 0])
    extra = kwargs.get("extra", "")
    
    full_object = kwargs.get("full_object", True)
        
    # extra sets
    holes = kwargs.get("holes", True)
    both_holes = kwargs.get("both_holes", False)
    kwargs["pos"] = pos
    
    

    # get the default thing
    thing = oobb_base.get_default_thing(**kwargs)
    kwargs.pop("size","")    
    kwargs.pop("extra","")
    
    pos_current = [0,0,0]
    pos_shift = 30    
    comment_extra = ""
    #basic     
    
    item = "oobb_screw_socket_cap_shape_m3_radius_name_12_mm_depth"
    p3 = copy.deepcopy(kwargs)
    p3["comment"] = f"{item}{comment_extra}\n"
    p3["pos"] = copy.deepcopy(pos_current)
    p3["item"] = item
    p3["m"] = ""
    oobb_base.append_full(thing, **p3)
    
    
    pos_current[1] += pos_shift
    # nut
    p4 = copy.deepcopy(p3)    
    p4["nut"] = True
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}{comment_extra}\nnut : True"
    oobb_base.append_full(thing, **p4)
        
    pos_current[1] += pos_shift
    # nut and overhang
    p4 = copy.deepcopy(p3)    
    p4["nut"] = True
    p4["overhang"] = True
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}{comment_extra}\nnut : True, overhang : True"
    oobb_base.append_full(thing, **p4)    
     
    pos_current[1] += pos_shift
    # zz top
    p4 = copy.deepcopy(p3)    
    p4["zz"] = "top"    
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}{comment_extra}\nzz : top"
    oobb_base.append_full(thing, **p4) 


    pos_current[1] += pos_shift
    # zz bottom
    p4 = copy.deepcopy(p3)    
    p4["zz"] = "bottom"    
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}{comment_extra}\nzz : bottom"
    oobb_base.append_full(thing, **p4) 

    pos_current[1] += pos_shift
    # zz bottom
    p4 = copy.deepcopy(p3)    
    p4["zz"] = "bottom"  
    p4["nut"] = True  
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}{comment_extra}\nzz : bottom nut : True"
    oobb_base.append_full(thing, **p4) 
    
    pos_current[1] += pos_shift
    # zz bottom
    p4 = copy.deepcopy(p3)    
    p4["zz"] = "bottom"  
    p4["nut"] = True  
    p4["pos"] = copy.deepcopy(pos_current)
    p4["clearance"] = "bottom"
    p4["comment"] = f"{item}{comment_extra}\nzz : bottom nut : True clearance : bottom"
    oobb_base.append_full(thing, **p4) 
    
    pos_current[1] += pos_shift
    # zz bottom
    p4 = copy.deepcopy(p3)    
    p4["zz"] = "bottom"  
    p4["nut"] = True  
    p4["rot_y"] = 180
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}{comment_extra}\nzz : bottom nut : True rot_y : 180"
    oobb_base.append_full(thing, **p4) 

    
    pos_current[1] += pos_shift
    # clearance_top
    p4 = copy.deepcopy(p3)    
    p4["clearance"] = "top"
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}{comment_extra}\nclearance : top"
    oobb_base.append_full(thing, **p4) 


    pos_current[1] += pos_shift
    # clearance_top
    p4 = copy.deepcopy(p3)    
    p4["clearance"] = "bottom"
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}{comment_extra}\nclearance : bottom"
    oobb_base.append_full(thing, **p4) 
    
    pos_current[1] += pos_shift
    # clearance_bottom
    p4 = copy.deepcopy(p3)    
    p4["clearance"] = "bottom"
    p4["nut"] = True
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}{comment_extra}\nclearance : bottom nut : True"
    oobb_base.append_full(thing, **p4) 
    
    pos_current[1] += pos_shift
    # clearance_bottom
    p4 = copy.deepcopy(p3)    
    p4["clearance"] = ["top","bottom"]
    p4["nut"] = True
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}{comment_extra}\nclearance : [bottom , top] nut : True"
    oobb_base.append_full(thing, **p4) 
    
    pos_current[1] += pos_shift
    # clearance_bottom
    p4 = copy.deepcopy(p3)    
    p4["clearance"] = ["top","bottom"]
    p4["zz"] = "top"
    p4["nut"] = True
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}{comment_extra}\nclearance : [bottom , top] nut : True zz : top"
    oobb_base.append_full(thing, **p4) 

    pos_current[1] += pos_shift
    # clearance_bottom zz bottom
    p4 = copy.deepcopy(p3)    
    p4["clearance"] = "bottom"
    p4["zz"] = "bottom"
    p4["nut"] = True
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}{comment_extra}\nclearance : bottom nut : True zz : bottom"
    oobb_base.append_full(thing, **p4) 

    ########################### rot_y

    pos_current = [300,0,0]
    pos_shift = 30    
    comment_extra = " rot_y : 180"
    #basic     
    
    item = "oobb_screw_socket_cap_shape_m3_radius_name_12_mm_depth"
    p3 = copy.deepcopy(kwargs)
    p3["comment"] = f"{item}\n{comment_extra}\n"
    p3["pos"] = copy.deepcopy(pos_current)
    p3["item"] = item
    p3["rot_y"] = 180
    p3["m"] = ""
    oobb_base.append_full(thing, **p3)
    
    
    pos_current[1] += pos_shift
    # nut
    p4 = copy.deepcopy(p3)    
    p4["nut"] = True
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nnut : True"
    oobb_base.append_full(thing, **p4)
        
    pos_current[1] += pos_shift
    # nut and overhang
    p4 = copy.deepcopy(p3)    
    p4["nut"] = True
    p4["overhang"] = True
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nnut : True, overhang : True"
    oobb_base.append_full(thing, **p4)    
     
    pos_current[1] += pos_shift
    # zz top
    p4 = copy.deepcopy(p3)    
    p4["zz"] = "top"    
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nzz : top"
    oobb_base.append_full(thing, **p4) 


    pos_current[1] += pos_shift
    # zz bottom
    p4 = copy.deepcopy(p3)    
    p4["zz"] = "bottom"    
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nzz : bottom"
    oobb_base.append_full(thing, **p4) 

    
    pos_current[1] += pos_shift
    # clearance_top
    p4 = copy.deepcopy(p3)    
    p4["clearance"] = "top"
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nclearance : top"
    oobb_base.append_full(thing, **p4) 


    pos_current[1] += pos_shift
    # clearance_top
    p4 = copy.deepcopy(p3)    
    p4["clearance"] = "bottom"
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nclearance : bottom"
    oobb_base.append_full(thing, **p4) 
    
    pos_current[1] += pos_shift
    # clearance_top
    p4 = copy.deepcopy(p3)    
    p4["clearance"] = "bottom"
    p4["nut"] = True
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nclearance : bottom nut : True"
    oobb_base.append_full(thing, **p4) 

    
    pos_current[1] += pos_shift
    # clearance_bottom zz bottom
    p4 = copy.deepcopy(p3)    
    p4["clearance"] = "bottom"
    p4["zz"] = "bottom"
    p4["nut"] = True
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nclearance : bottom nut : True zz : bottom"
    oobb_base.append_full(thing, **p4) 

    ########################### rot_y 90

    pos_current = [600,0,0]
    pos_shift = 30    
    comment_extra = " rot_y : 90"
    #basic     
    
    item = "oobb_screw_socket_cap_shape_m3_radius_name_12_mm_depth"
    p3 = copy.deepcopy(kwargs)
    p3["comment"] = f"{item}\n{comment_extra}\n"
    p3["pos"] = copy.deepcopy(pos_current)
    p3["item"] = item
    p3["rot_y"] = 90
    p3["m"] = ""
    oobb_base.append_full(thing, **p3)
    
    
    pos_current[1] += pos_shift
    # nut
    p4 = copy.deepcopy(p3)    
    p4["nut"] = True
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nnut : True"
    oobb_base.append_full(thing, **p4)
        
    pos_current[1] += pos_shift
    # nut and overhang
    p4 = copy.deepcopy(p3)    
    p4["nut"] = True
    p4["overhang"] = True
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nnut : True, overhang : True"
    oobb_base.append_full(thing, **p4)    
     
    pos_current[1] += pos_shift
    # zz top
    p4 = copy.deepcopy(p3)    
    p4["zz"] = "top"    
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nzz : top"
    oobb_base.append_full(thing, **p4) 


    pos_current[1] += pos_shift
    # zz bottom
    p4 = copy.deepcopy(p3)    
    p4["zz"] = "bottom"    
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nzz : bottom"
    oobb_base.append_full(thing, **p4) 

    
    pos_current[1] += pos_shift
    # clearance_top
    p4 = copy.deepcopy(p3)    
    p4["clearance"] = "top"
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nclearance : top"
    oobb_base.append_full(thing, **p4) 


    pos_current[1] += pos_shift
    # clearance_top
    p4 = copy.deepcopy(p3)    
    p4["clearance"] = "bottom"
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nclearance : bottom"
    oobb_base.append_full(thing, **p4) 
    
    pos_current[1] += pos_shift
    # clearance_top
    p4 = copy.deepcopy(p3)    
    p4["clearance"] = "bottom"
    p4["nut"] = True
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nclearance : bottom nut : True"
    oobb_base.append_full(thing, **p4) 

    
    pos_current[1] += pos_shift
    # clearance_bottom zz bottom
    p4 = copy.deepcopy(p3)    
    p4["clearance"] = "bottom"
    p4["zz"] = "bottom"
    p4["nut"] = True
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nclearance : bottom nut : True zz : bottom"
    oobb_base.append_full(thing, **p4) 

    ########################### rot_x 180

    pos_current = [900,0,0]
    pos_shift = 60    
    comment_extra = " rot_x : 180"
    #basic     
    
    item = "oobb_screw_socket_cap_shape_m3_radius_name_12_mm_depth"
    p3 = copy.deepcopy(kwargs)
    p3["comment"] = f"{item}\n{comment_extra}\n"
    p3["pos"] = copy.deepcopy(pos_current)
    p3["item"] = item
    p3["rot_x"] = 180
    p3["m"] = ""
    oobb_base.append_full(thing, **p3)
    
    
    pos_current[1] += pos_shift
    # nut
    p4 = copy.deepcopy(p3)    
    p4["nut"] = True
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nnut : True"
    oobb_base.append_full(thing, **p4)
        
    pos_current[1] += pos_shift
    # nut and overhang
    p4 = copy.deepcopy(p3)    
    p4["nut"] = True
    p4["overhang"] = True
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nnut : True, overhang : True"
    oobb_base.append_full(thing, **p4)    
     
    pos_current[1] += pos_shift
    # zz top
    p4 = copy.deepcopy(p3)    
    p4["zz"] = "top"    
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nzz : top"
    oobb_base.append_full(thing, **p4) 


    pos_current[1] += pos_shift
    # zz bottom
    p4 = copy.deepcopy(p3)    
    p4["zz"] = "bottom"    
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nzz : bottom"
    oobb_base.append_full(thing, **p4) 

    ########################### rot_x -90

    pos_current = [1200,0,0]
    pos_shift = 60    
    comment_extra = " rot_x : -90"
    #basic     
    
    item = "oobb_screw_socket_cap_shape_m3_radius_name_12_mm_depth"
    p3 = copy.deepcopy(kwargs)
    p3["comment"] = f"{item}\n{comment_extra}\n"
    p3["pos"] = copy.deepcopy(pos_current)
    p3["item"] = item
    p3["rot_x"] = -90
    p3["m"] = ""
    oobb_base.append_full(thing, **p3)
    
    
    pos_current[1] += pos_shift
    # nut
    p4 = copy.deepcopy(p3)    
    p4["nut"] = True
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nnut : True"
    oobb_base.append_full(thing, **p4)
        
    pos_current[1] += pos_shift
    # nut and overhang
    p4 = copy.deepcopy(p3)    
    p4["nut"] = True
    p4["overhang"] = True
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nnut : True, overhang : True"
    oobb_base.append_full(thing, **p4)    
     
    pos_current[1] += pos_shift
    # zz top
    p4 = copy.deepcopy(p3)    
    p4["zz"] = "top"    
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nzz : top"
    oobb_base.append_full(thing, **p4) 


    pos_current[1] += pos_shift
    # zz bottom
    p4 = copy.deepcopy(p3)    
    p4["zz"] = "bottom"    
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nzz : bottom"
    oobb_base.append_full(thing, **p4) 

    ########################### rot_x 90 rot_y 90

    pos_current = [1500,0,0]
    pos_shift = 60    
    comment_extra = " rot_x : 90 rot_y : 90 rot_z : 90"
    #basic     
    
    item = "oobb_screw_socket_cap_shape_m3_radius_name_12_mm_depth"
    p3 = copy.deepcopy(kwargs)
    p3["comment"] = f"{item}\n{comment_extra}\n"
    p3["pos"] = copy.deepcopy(pos_current)
    p3["item"] = item
    p3["rot_x"] = 90
    p3["rot_y"] = 90
    p3["rot_z"] = 90
    p3["m"] = ""
    oobb_base.append_full(thing, **p3)
    
    
    pos_current[1] += pos_shift
    # nut
    p4 = copy.deepcopy(p3)    
    p4["nut"] = True
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nnut : True"
    oobb_base.append_full(thing, **p4)
        
    pos_current[1] += pos_shift
    # nut and overhang
    p4 = copy.deepcopy(p3)    
    p4["nut"] = True
    p4["overhang"] = True
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nnut : True, overhang : True"
    oobb_base.append_full(thing, **p4)    
     
    pos_current[1] += pos_shift
    # zz top
    p4 = copy.deepcopy(p3)    
    p4["zz"] = "top"    
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nzz : top"
    oobb_base.append_full(thing, **p4) 


    pos_current[1] += pos_shift
    # zz bottom
    p4 = copy.deepcopy(p3)    
    p4["zz"] = "bottom"    
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nzz : bottom"
    oobb_base.append_full(thing, **p4) 
    

    if full_object:   
        return thing
    else: # only return the elements
        return thing["components"]

# shape
def get_test_oobb_shape_slot(**kwargs):
    # default sets
    kwargs.pop("style","")
    pos = kwargs.get("pos", [0, 0, 0])    
    full_object = kwargs.get("full_object", True)
        
    # extra sets
    kwargs["pos"] = pos
    
    # get the default thing
    thing = oobb_base.get_default_thing(**kwargs)
    kwargs.pop("size","")    
    kwargs.pop("extra","")
    kwargs.pop("type","")
    
    pos_current = [0,0,0]
    pos_shift = 50
    comment_extra = ""
    
    versions = []
    base = {}    
    base["shape"] = f"oobb_slot"
    base["r1"] = 5
    base["r2"] = 10
    base["width"] = 20
    base["depth"]   = 10
    base["comment_shift_line"] = 15
    base["comment_extra"] = ""
    base["comment_display"] = True
    #base["m"] = ""
    base["extra"] = {}

    versions.append(copy.deepcopy(base))
    
    b = copy.deepcopy(base)
    b["zz"] = "top"
    b["comment_extra"] = "zz : top"
    versions.append(b)

    b = copy.deepcopy(base)
    b["zz"] = "bottom"
    b["comment_extra"] = "zz : bottom"
    versions.append(b)

    b = copy.deepcopy(base)
    b["zz"] = "middle"
    b["comment_extra"] = "zz : middle"
    versions.append(b)




    rots = []
    rots.append([[0,0,0], {}, ""])
    rots.append([[150,0,0], {"rot":[0,360/12,0]}, "rot_y : 360/12"])
    rots.append([[300,0,0], {"rot":[0,90,0]}, "rot_y : 90"])
    rots.append([[450,0,0], {"rot":[90,45,0]}, "rot_x : 90 rot_y : 45"])

    for r in rots:
        pos_current = r[0]
        extra_extra = r[1]
        comment_extra_extra = r[2]

        for v in versions:                        
            p3 = copy.deepcopy(kwargs)
            p3.update(v)
            comment_extra = v["comment_extra"]
            p3["comment"] = f"{v['shape']}\n{comment_extra}{comment_extra_extra}"
            comment_display = v.get("comment_display", False)
            p3["pos"] = copy.deepcopy(pos_current)
            p3.update(v["extra"])
            p3.update(extra_extra)
            oobb_base.append_full(thing, **p3)
            pos_current[1] += pos_shift
        
        
    

    if full_object:   
        return thing
    else: # only return the elements
        return thing["components"]


# wire
def get_test_oobb_wire(**kwargs):
    # default sets
    style = kwargs.get("style", "wire")
    kwargs.pop("style","")
    pos = kwargs.get("pos", [0, 0, 0])    
    full_object = kwargs.get("full_object", True)
        
    # extra sets
    kwargs["pos"] = pos
    
    # get the default thing
    thing = oobb_base.get_default_thing(**kwargs)
    kwargs.pop("size","")    
    kwargs.pop("extra","")
    kwargs.pop("type","")
    
    pos_current = [0,0,0]
    pos_shift = 60
    comment_extra = ""
    
    versions = []
    

    styles = ["motor","motor_stepper","basic","higher_voltage","i2c","spacer"]

    for style in styles:
        base = {}    
        base["shape"] = f"oobb_wire_{style}"
        base["comment_extra"] = ""
        base["comment_display"] = True
        #base["m"] = ""
        base["extra"] = {}
        versions.append(copy.deepcopy(base))
    
    rots = []
    rots.append([[0,0,0], {}, ""])
    rots.append([[150,0,0], {"rot_y":180}, "rot_y : 180"])
    rots.append([[300,0,0], {"rot_y":90}, "rot_y : 90"])
    rots.append([[450,0,0], {"rot_x":45, "rot_y": 45}, "rot_x : 90 rot_y : 45"])


    for r in rots:
        pos_current = r[0]
        extra_extra = r[1]
        comment_extra_extra = r[2]

        for v in versions:                        
            p3 = copy.deepcopy(kwargs)
            comment_extra = v["comment_extra"]
            p3["shape"] = v["shape"] 
            p3["type"] = "positive"
            
            p3["comment"] = f"{v['shape']}_\n{comment_extra}{comment_extra_extra}"
            comment_display = v.get("comment_display", False)
            p3["comment_display"]   = comment_display
            p3["pos"] = copy.deepcopy(pos_current)
            p3["m"] = ""
            p3.update(v["extra"])
            p3.update(extra_extra)
            oobb_base.append_full(thing, **p3)
            pos_current[1] += pos_shift
        
        
    

    if full_object:   
        return thing
    else: # only return the elements
        return thing["components"]