# ---------------------------------------------------------------------
# HP.Comware.get_config
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------


# NOC modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetconfig import IGetConfig


class Script(BaseScript):
    name = "HP.Comware.get_config"
    interface = IGetConfig

    def to_reuse_cli_session(self):
        if self.is_bad_release:
            return False
        return self.reuse_cli_session

    def execute_cli(self, policy="r"):
        assert policy in ("r", "s")
        self.cli("undo terminal monitor")
        config = self.cli("display current-configuration")
        config = self.profile.clean_spaces(config)
        return self.cleaned_config(config)
