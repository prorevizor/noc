# ----------------------------------------------------------------------
# Documentation macroses
# ----------------------------------------------------------------------
# Copyright (C) 2007-2020 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------


def define_env(env):
    @env.macro
    def mr(iid):
        """
        Link to Merge Request. Usage:

        {{ mr(123) }}
        :param iid:
        :return:
        """
        return f"[MR{iid}](https://code.getnoc.com/noc/noc/merge_requests/{iid})"
