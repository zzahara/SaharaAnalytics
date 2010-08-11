#!/usr/bin/env python

# Copyright 2010 Internet Archive
# Written by Zahara Docena
# This program is distributed under the terms of the GNU General Public License v3
# see: http://www.gnu.org/licenses/gpl.txt 

# Input: flat file (must include the selected fields to add)
# Output: flat file (same as input with a new sum field)

# Example: ./zd_add.py -n sum_field -a loadtime -a server_ms

# Input:
# loadtime    server_ms     locale
# 500           200         en-US
# ...

# Output:
# loadtime    server_ms     locale      sum_field
# 500           200         en-US          700
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
    parser.add_option("-n", action="store", dest="name", help="name of new field")
    parser.add_option("-a", action="append", dest="add_fields", help="fields to add")
    
    (options, args) = parser.parse_args(argv)
    return options

def process_file(options):
    field_list = zd_lib.get_field_list()

    # store the indexes of the fields that will be added
    indexes = []
    for field in options.add_fields:
        indexes.append(field_list.index(field))

    print_field_line(options.name, field_list)
    for log_line in sys.stdin:
        try:
            log_line = log_line.rstrip()
            log_data = log_line.split('\t')

            print log_line + '\t',
            print_sum(log_data, options.add_fields, field_list)     

        except IOError, e:
            if e.errno == errno.EPIPE:
                exit(0)      
    
def print_sum(log_data, sum_fields, field_list):
    new_sum = 0

    for field in sum_fields:
        index = field_list.index(field)
        if log_data[index] != '-':
            new_sum = new_sum + int(log_data[index])

    print str(new_sum)

def print_field_line(new_field, field_list):
    field_list.append(new_field)
    print '\t'.join(field_list)

# Main
options = process_args()
process_file(options)


