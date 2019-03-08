# ccache statistics

[![Build Status](https://travis-ci.org/fweik/ccache-stats.svg?branch=master)](https://travis-ci.org/fweik/ccache-stats)

This is a simple python package that runs ccache and extracts
information about the cache statistics as returned by `ccache -s`
and can report the version of a ccache executable.

## Basic usage

```python

from ccache_stats import CCacheStats

stats = CCacheStats()

print(stats.version())
print(stats.stats())

```
