d = {}


def define():
    global d
    if not d:
        d = {
            "name": "holders",
            "name_short": [],
            "name_long": "OOBB Part Set: Holders",
            "description": "Electronic and mechanical holder variants, including motor mounts and accessory holders.",
            "category": "Part Sets",
            "variables": ["size"],
        }
    return dict(d)


def items(size="oobb", **kwargs):
    import oobb_make_sets

    getter = getattr(oobb_make_sets, "get_holders")
    try:
        return getter(size=size, **kwargs)
    except TypeError:
        return getter(**kwargs)


def test(**kwargs):
    return isinstance(items(**kwargs), list)
