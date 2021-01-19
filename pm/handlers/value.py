# ----------------------------------------------------------------------
# Value handlers
# ----------------------------------------------------------------------
# Copyright (C) 2007-2020 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------


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
        return v * 100 / bandwidth
    if in_speed:
        return v * 100 / in_speed
    if out_speed:
        return v * 100 / out_speed
    return v
