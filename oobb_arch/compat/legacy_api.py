"""Thin compatibility wrappers.

Phase 1 behavior: simply delegates to existing `oobb_base` API.
"""


def get_thing_from_dict(*args, **kwargs):
    import oobb_base

    return oobb_base.get_thing_from_dict(*args, **kwargs)


def build_thing(*args, **kwargs):
    import oobb_base

    return oobb_base.build_thing(*args, **kwargs)


def build_things(*args, **kwargs):
    import oobb_base

    return oobb_base.build_things(*args, **kwargs)
