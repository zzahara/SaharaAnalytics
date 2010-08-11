#!/usr/bin/env python

# Copyright 2010 Inyternet Archive
# Written by Zahara Docena
# This program is distributed under the terms of the GNU General Public License v3
# see: http://www.gnu.org/licenses/gpl.txt 

# Input: flat file (must include the selected fields)
# Output: flat file 
#   - detects the way the input file is grouped
#   - and removes all lines within a group that share the field values specified

# usage: ./zd_uniq.py -f field1 -f field2

import re
import os
import sys
import math
import errno
from sys import argv
from optparse import OptionParser

argv
parser = OptionParser()

def process_args():
    parser.add_option("-f", action="append", dest="fields")
    (options, args) = parser.parse_args(argv)
    
    return options

def process_file(options):
    field_list = get_field_list()
    indexes = get_indexes(field_list, options.fields)
    
    current = []
    equal = False
    prev_line = ''
    
    for log_line in sys.stdin:
        try:
            log_data = log_line.split('\t')

            if len(current) == 0:
                current = get_current(log_data, indexes)
                
            elif equal_values(log_data, indexes, current) == False:
                equal = False
                current = get_current(log_data, indexes)
                print prev_line,

            else:
                equal = True
                
            prev_line = log_line
        except IOError, e:
            if e.errno == errno.EPIPE:
                exit(0)

    # last line
    if equal == False:
        print prev_line,

def get_indexes(field_list, fields):   
    indexes = []

    for field in fields:
        indexes.append(field_list.index(field))   

    return indexes        


def equal_values(log_data, indexes, current):
    i = 0
    
    for x in indexes:
        if log_data[x] != current[i]:
            return False
        i = i + 1

    return True
    
# gets the field values of the current group
def get_current(log_data, grouped_by):
    current = []

    for field_index in grouped_by:
        value = log_data[field_index]
        current.append(value)

    return current


def get_field_list():
    first_line = sys.stdin.readline()
    first_line = first_line.rstrip()
    
    print first_line
    return first_line.split('\t')


options = process_args()
process_file(options)

    
    
