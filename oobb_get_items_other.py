from oobb_get_items_base import *
import oobb_base as ob


def get_bolt(**kwargs):
    from part_calls.objects.oobb_object_bolt.working import action

    return action(**kwargs)


def get_nut_m3():
    nut = get_nut(radius_name="m3", type="nut")
    return nut


def get_nut(**kwargs):
    from part_calls.objects.oobb_object_nut.working import action

    return action(**kwargs)


def get_screw_countersunk(**kwargs):
    from part_calls.objects.oobb_object_screw_countersunk.working import action

    return action(**kwargs)

def get_screw_self_tapping(**kwargs):
    from part_calls.objects.oobb_object_screw_self_tapping.working import action

    return action(**kwargs)

def get_screw_socket_cap(**kwargs):
    from part_calls.objects.oobb_object_screw_socket_cap.working import action

    return action(**kwargs)


def get_standoff(**kwargs):
    from part_calls.objects.oobb_object_standoff.working import action

    return action(**kwargs)


def get_threaded_insert(**kwargs):
    from part_calls.objects.oobb_object_threaded_insert.working import action

    return action(**kwargs)


def get_bearing(**kwargs):
    from part_calls.objects.oobb_object_bearing.working import action

    return action(**kwargs)
