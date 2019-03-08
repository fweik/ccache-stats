import unittest as ut
from unittest.mock import patch
from datetime import datetime
from subprocess import CompletedProcess

from ccache_stats import CCacheStats, _BlockingExecutor

CCACHE_EXECUTABLE = r"ccache"
CCACHE_VERSION = (1,3,3)
CCACHE_VERSION_STRING = '.'.join((str(i) for i in CCACHE_VERSION))
CCACHE_CACHE_HITS_DIRECT = 1123
CCACHE_CACHE_DIR = r"/some/path/to/cache"

class _DummyExecutor:
    def __call__(self, executable, args):
        if executable != CCACHE_EXECUTABLE:
            return None
        if args[0] in ["--version", "-V"]:
            return f"ccache version {CCACHE_VERSION_STRING}"
        if args[0] in ["--show-stats", "-s"]:
            return f"cache hit (direct) {CCACHE_CACHE_HITS_DIRECT} \ncache directory  {CCACHE_CACHE_DIR}"

class CCacheStatsTest(ut.TestCase):
    def test(self):
        stats = CCacheStats(CCACHE_EXECUTABLE, executor=_DummyExecutor())

        self.assertEqual(stats.version(), CCACHE_VERSION)
        res = stats.stats()

        self.assertTrue("cache_directory" in res)
        self.assertEqual(res["cache_directory"], CCACHE_CACHE_DIR)

        self.assertTrue("cache_hit_direct" in res)
        self.assertEqual(res["cache_hit_direct"], CCACHE_CACHE_HITS_DIRECT)

EXECUTOR_COMMAND = "some_exec"
EXECUTOR_ARGS = ["some", "arguments"]
EXECUTOR_OUTPUT = r"foo/bar"

class BlockingExecutorTest(ut.TestCase):
    @patch('subprocess.run', return_value=CompletedProcess(args=EXECUTOR_ARGS,
                                                           stdout=EXECUTOR_OUTPUT,
                                                           returncode=0))
    def test(self, run_mock):
        blocking_exec = _BlockingExecutor()

        ret = blocking_exec(EXECUTOR_COMMAND, EXECUTOR_ARGS)
        self.assertEqual(ret, EXECUTOR_OUTPUT)

        print(run_mock.getvalue())

if __name__ == "__main__":
    ut.main()
