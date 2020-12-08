# ---------------------------------------------------------------------
# Vendor: Eltex
# OS:     TAU
# ---------------------------------------------------------------------
# Copyright (C) 2007-2020 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# NOC modules
from noc.core.profile.base import BaseProfile


class Profile(BaseProfile):
    name = "Eltex.TAU"
    pattern_username = r"^\S+ [Ll]ogin:"
    pattern_password = r"^[Pp]assword:"
    pattern_unprivileged_prompt = r"^(?P<hostname>\S+)>\s*"
    pattern_prompt = r"^(\S+# |> |config> |\S+]\s*)"
    pattern_more = "Press any key to continue"
    pattern_syntax_error = "Syntax error: Unknown command"
    command_exit = "exit"
    command_more = "\n"
    command_enter_config = "config"
    command_leave_config = "exit"
    command_super = "enable"

    class shell(object):
        """Switch context manager to use with "with" statement"""

        def __init__(self, script):
            self.script = script

        def __enter__(self):
            """Enter switch context"""
            self.script.cli("shell")

        def __exit__(self, exc_type, exc_val, exc_tb):
            """Leave switch context"""
            if exc_type is None:
                self.script.cli("exit\r")

    INTERFACE_TYPES = {
        "e": "physical",  # Ethernet
        "p": "physical",  # Virtual Ethernet
        "l": "loopback",  # Local Loopback
    }

    @classmethod
    def get_interface_type(cls, name):
        c = cls.INTERFACE_TYPES.get(name[:1])
        return c
