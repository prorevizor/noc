# ----------------------------------------------------------------------
# Documentation macroses
# ----------------------------------------------------------------------
# Copyright (C) 2007-2020 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

import os


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

    @env.macro
    def supported_scripts(profile):
        nonlocal scripts
        r = ["Script | Support", "--- | ---"]
        if not scripts:
            # Load list of all scripts
            scripts = list(
                sorted(
                    x[:-3]
                    for x in os.listdir(os.path.join(doc_root, "dev", "scripts"))
                    if x.endswith(".md") and not x.startswith(".")
                )
            )
        # Get profile scripts
        vendor, name = profile.split(".")
        supported = {
            f[:-3]
            for f in os.listdir(os.path.join("sa", "profiles", vendor, name))
            if f.endswith(".py")
        }
        # Render
        for script in scripts:
            if script in supported:
                mark = ":material-check:"
            else:
                mark = ":material-close:"
            r += [f"{script} | {mark}"]
        r += [""]
        return "\n".join(r)

    scripts = []  # Ordered list of scripts
    doc_root = "docs/en/docs"
