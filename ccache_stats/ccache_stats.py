"""Evaluate ccache stats.
"""

import subprocess
from parse import parse_stat, parse_version

class _BlockingExecutor:
    def __call__(self, executable, args):
        res = subprocess.run([executable] + args,
                             stdout=subprocess.PIPE,
                             universal_newlines=True,
                             check=True)

        return str(res.stdout)

class CCacheStats:
    def __init__(self, ccache_exec, executor = _BlockingExecutor()):
        self._ccache = ccache_exec
        self._exec = executor

    def version(self):
        """The version of the ccache executable.
        """

        version_string = self._exec(self._ccache, ["-V"])
        return parse_version(version_string)

    def stats(self):
        """Run ccache and retrieve stats.
        """

        return parse_stat(self._exec(self._ccache, ["-s"]))

