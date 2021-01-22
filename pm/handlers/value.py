# ----------------------------------------------------------------------
# Value handlers
# ----------------------------------------------------------------------
# Copyright (C) 2007-2020 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------


def humanize_load(speed, type_speed):

    d_speed = {
        "bit/s": 1000000,
        "kbit/s": 1000,
    }

    if speed < 1000 and speed > 0:
        return "%s " % speed
    res = d_speed.get(type_speed)
    if speed >= res:
        print(speed // res)
        return speed // res


def bw_percent(v, in_speed=None, out_speed=None, bandwidth=None, **kwargs):
    """
    Convert speed to speed to bandwidth percent ratio
    :param v:
    :param in_speed:
    :param out_speed:
    :param bandwidth:
    :param kwargs:
    :return:
    """
    if bandwidth:
        return round(humanize_load(int(v), "bit/s") * 100 / humanize_load(bandwidth, "kbit/s"), 0)
    if in_speed:
        return round(humanize_load(int(v), "bit/s") * 100 / humanize_load(in_speed, "kbit/s"), 0)
    if out_speed:
        return round(humanize_load(int(v), "bit/s") * 100 / humanize_load(out_speed, "kbit/s"), 0)
    return v
