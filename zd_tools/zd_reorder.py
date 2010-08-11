#!/usr/bin/env python

# Copyright 2010 Internet Archive
# Written by Zahara Docena
# This program is distributed under the terms of the GNU General Public License v3
# see: http://www.gnu.org/licenses/gpl.txt 

# Input: flat file (must have the selected fields to reorder)
# Output: flat file 
#   - with the columns reordered
#   - will only output the specified fields

# Example: ./zd_reorder.py -f count -f page

# Input:
# page          count     locale
# website.com   6791      en-us
# ...

# Output:
# count     page
# 6791      website.com
# ...

import sys
import errno
import zd_lib
from sys import argv
from optparse import OptionParser

argv
parser = OptionParser()

def process_args():
    global argv, parser
    parser.add_option("-f", action="append", dest="fields", help="new order of the field columns")

    (options, args) = parser.parse_args(argv)
    return options

def process_file(options):
    field_list = zd_lib.get_field_list()

    indexes = []
    for field in options.fields:
        indexes.append(field_list.index(field))

    print_field_line(options.fields)
    for log_line in sys.stdin:
        try:
            log_line = log_line.rstrip()
            log_data = log_line.split('\t') 
            print_line(log_data, indexes)
        except IOError, e:
            if e.errno == errno.EPIPE:
                exit(0)

def print_line(log_data, indexes):
    values = []
    for i in indexes:
        values.append(log_data[i])

    print '\t'.join(values)

def print_field_line(fields):
    print '\t'.join(fields)


# Main
options = process_args()
process_file(options)


