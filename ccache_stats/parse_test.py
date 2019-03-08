import unittest as ut
from datetime import datetime

from .parse import parse_stat, parse_version

class VersionParse(ut.TestCase):
    """Test parsing the version from ccache output.
    """

    def test_version(self):
        output = r"ccache version 3.4.1"
        result = parse_version(output)

        self.assertEqual(result, (3,4,1))

class StatsParse(ut.TestCase):
    """Test the ccache output parser.

    Tests parsing for all known lines in ccache stat output.
    """
    def _compare_out(self, in_field, in_val, expected_name, expected_out):
        """Compare expected parsing output with actual.
        """
        result = parse_stat(f"{in_field}  {in_val}")

        self.assertTrue(expected_name in result)
        self.assertEqual(type(result[expected_name]), type(expected_out))
        self.assertEqual(result[expected_name], expected_out)

    def test_cache_dir(self):
        test_path = "/some/path/"
        self._compare_out("cache directory", test_path,
                          "cache_directory", test_path)

    def test_primary_config(self):
        test_path = "/some/path/ccache.config"
        self._compare_out("primary config", test_path,
                          "primary_config", test_path)

    def test_secondary_config(self):
        test_path = "/some/path/ccache.config"
        self._compare_out("secondary config (readonly)", test_path,
                          "secondary_config", test_path)

    def test_stats_zero_time(self):
        test_date = datetime(2012, 8, 11, 12, 1, 2, 0)
        self._compare_out("stats zero time", test_date.strftime("%a %b %d %H:%M:%S %Y"),
                          "stats_zero_time", test_date)

    def test_cache_hit_direct(self):
        test_hits = 11
        self._compare_out("cache hit (direct)", test_hits,
                          "cache_hit_direct", test_hits)

    def test_cache_hit_preprocessed(self):
        test_hits = 11
        self._compare_out("cache hit (preprocessed)", test_hits,
                          "cache_hit_preprocessed", test_hits)

    def test_cache_hit_rate(self):
        test_rate = 101.01

        self._compare_out("cache hit rate", f"{test_rate} %",
                          "cache_hit_rate", test_rate)

    def test_unknown(self):
        """Check that unknown lines are ignored.
        """
        result = parse_stat(r"invalid field")

        self.assertEqual(result, {})

if __name__ == "__main__":
    ut.main()
