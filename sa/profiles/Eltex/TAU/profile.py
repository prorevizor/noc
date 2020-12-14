# ---------------------------------------------------------------------
# Vendor: Eltex
# OS:     TAU
# ---------------------------------------------------------------------
# Copyright (C) 2007-2020 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
import re

# NOC modules
from noc.core.profile.base import BaseProfile


class Profile(BaseProfile):
    name = "Eltex.TAU"
    pattern_username = r"^\S+ [Ll]ogin:"
    pattern_password = r"^[Pp]assword:"
    pattern_unprivileged_prompt = r"^(?P<hostname>\S+)>\s*"
    pattern_prompt = r"^(\S+# |> |config> |\[\S+\]\s*)"
    pattern_more = (
        r'Press any key to continue|\| Press any key to continue \| Press "q" to exit \| '
    )
    pattern_syntax_error = r"Syntax error: Unknown command|-sh: .+: not found"
    command_exit = "exit"
    command_more = "\n"
    command_enter_config = "config"
    command_leave_config = "exit"
    command_super = "enable"
    rogue_chars = [re.compile(rb"\^J"), b"\r"]

    def setup_session(self, script):
        try:
            script.cli("show hwaddr", cached=True)
            script.cli("shell", ignore_errors=True)
            self.already_in_shell = False
        except script.CLISyntaxError:
            self.already_in_shell = True

    def shutdown_session(self, script):
        if not self.already_in_shell:
            script.cli("exit\r", ignore_errors=True)

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
