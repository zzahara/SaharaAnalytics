#!/usr/bin/env python
import sys
import errno

# read first line from stdin and discard it
first_line = sys.stdin.readline()

# print all other lines
for line in sys.stdin:
    try:
        print line,
    except IOError, e:
        if e.errno == errno.EPIPE:
            exit(0)

