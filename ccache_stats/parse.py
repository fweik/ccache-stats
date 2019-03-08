"""Parse output from ccache executable.

This file contains regex definitions and field
names for the different stats that can be found
in the output of the ccache executable, as well
as function for parsing this output into a dict.
"""

import re
from datetime import datetime

def _parse_int(token: str) -> int:
    return int(token)

def _parse_float(token: str) -> float:
    return float(token)

def _parse_str(token: str) -> str:
    return str(token)

_STATS_DATE_FORMAT = r"%a %b %d %H:%M:%S %Y"
"""Date format used by ccache.
"""

def _parse_date(token: str) -> datetime:
    """Parse ccache datetime into datetime.

    ccache date format is like 'Thu Nov 29 15:15:44 2018',
    see _STATS_DATE_FORMAT.
    """
    return datetime.strptime(token, _STATS_DATE_FORMAT)

_STATS_FIELDS = [
    (r"cache directory[ ]+(.*)", "cache_directory", _parse_str),
    (r"primary config[ ]+(.*)", "primary_config", _parse_str),
    (r"secondary config[ ]+\(readonly\)[ ]+(.*)", "secondary_config", _parse_str),
    (r"stats zero time[ ]+([A-Z].*)", "stats_zero_time", _parse_date),
    (r"cache hit \(direct\)[ ]+([0-9]+)", "cache_hit_direct", _parse_int),
    (r"cache hit \(preprocessed\)[ ]+([0-9]+)", "cache_hit_preprocessed", _parse_int),
    (r"cache miss[ ]+([0-9]+)", "cache_hit_miss", _parse_int),
    (r"cache hit rate[ ]+([0-9]{1,3}\.[0-9]{2}) %", "cache_hit_rate", _parse_float),
    (r"cleanups performed[ ]+([0-9]+)", "cleanups_performed", _parse_int),
    (r"files in cache[ ]+([0-9]+)", "files_in_cache", _parse_int),
    (r"cache size[ ]+([0-9]+\.[0-9]) GB", "cache_size", _parse_float),
    (r"max cache size[ ]+([0-9]+\.[0-9]) GB", "max_cache_size", _parse_float)
]
"""Map strings to fields.

For each stat line, this contains a tuple of a regex to match
the line, the name used by this module for the field and the
parser function to convert the matched token into a python variable.
"""

_STATS_FIELDS_RE = [(re.compile(r), f, con) for r, f, con in _STATS_FIELDS]
"""_STATS_FIELDS with compiled regular expressions.
"""

def _parse_stat_line(line: str):
    """Parse single line of input

    Returns the first field that matches any of the fields
    described in _STATS_FIELDS, or None if there is no match.
    """
    for matcher, field_name, value_parser in _STATS_FIELDS_RE:
        match = matcher.match(line)
        if match:
            return (field_name, value_parser(match.group(1)))

    return None

def parse_stat(output: str):
    """Parse multiple lines of input into dict.

    Returns a dict with all found field names as keys, or
    an empty dict if none where found.
    """
    vals = {}
    for line in output.splitlines():
        rval = _parse_stat_line(line)
        if rval:
            key, value = rval
            vals[key] = value

    return vals

_VERSION_RE = re.compile(r"ccache version ([0-9]+)\.([0-9]+)\.([0-9]+)")

def parse_version(output: str):
    """Parse ccache version from output of ccache --version

    Returns tuple (MAJOR, MINOR, PATCH).
    """
    matcher = _VERSION_RE

    for line in output.splitlines():
        match = matcher.match(line)
        if match:
            group = match.group
            tokens = (group(1), group(2), group(3))
            return tuple(_parse_int(token) for token in tokens)
