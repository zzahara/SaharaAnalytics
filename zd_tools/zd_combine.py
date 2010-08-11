#!/usr/bin/env python

# Copyright 2010 Internet Archive
# Written by Zahara Docena
# This program is distributed under the terms of the GNU General Public License v3
# see: http://www.gnu.org/licenses/gpl.txt 

# Input: flat file (must include the selected fields to combine)
# Output: flat file 
#   - deletes the combined fields' columns
#   - concatenates the selected fields and adds a new column with the combined value

# Example: ./zd_combine.py -n combined_field -c ip -c locale

# Input:
# ip                         page               locale
# 0.29.113.149          www.yoursite.com        en-US
# ...

# Output:
# combined_field             page     
# 0.29.113.149en-US     www.yoursite.com
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
    parser.add_option("-c", action="append", dest="combine", help="fields to combine in the order entered")
    
    (options, args) = parser.parse_args(argv)
    return options

def process_file(options):
    field_list = zd_lib.get_field_list()

    # store the indexes of combining fields
    indexes = []
    for field in options.combine:
        indexes.append(field_list.index(field))

    print_field_line(options.name, options.combine, field_list)
    for log_line in sys.stdin:
        try:
            log_line = log_line.rstrip()
            log_data = log_line.split('\t')

            print_combined(log_data, options.combine, field_list)
            print_other_fields(log_data, options.combine, field_list)

        except IOError, e:
            if e.errno == errno.EPIPE:
                exit(0)

# print the fields that aren't being combined
def print_other_fields(log_data, combined, field_list):
    values = []
    for i in range(0, len(field_list)):
        if other_field(combined, i, field_list):
            values.append(log_data[i])

    print '\t'.join(values)

# check if the field is not one of the combined fields
def other_field(combined, field, field_list):
    for x in combined:
        if field == field_list.index(x):
            return False

    return True
   
def print_combined(log_data, combine_fields, field_list):
    new_string = ''

    for field in combine_fields:
        index = field_list.index(field)
        new_string = new_string + log_data[index]

    print new_string + '\t',

def print_field_line(new_field, combine, field_list):
    fields = []
    fields.append(new_field)
    
    for i in range(0, len(field_list)):
        if other_field(combine, i, field_list):
            fields.append(field_list[i])

    print '\t'.join(fields)
    
# Main
options = process_args()
process_file(options)


