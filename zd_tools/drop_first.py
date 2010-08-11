#!/usr/bin/env python

# Copyright 2010 Internet Archive
# Written by Zahara Docena
# This program is distributed under the terms of the GNU General Public License v3
# see: http://www.gnu.org/licenses/gpl.txt 

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

