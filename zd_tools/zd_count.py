#!/usr/bin/env python

# Copyright 2010 Internet Archive
# Written by Zahara Docena
# This program is distributed under the terms of the GNU General Public License v3
# see: http://www.gnu.org/licenses/gpl.txt 


import os
import sys
import errno
import zd_lib
from sys import argv
from optparse import OptionParser


argv
parser = OptionParser()

def process_args():
    parser.add_option("-f", action="append", dest="fields")
    (options, args) = parser.parse_args(argv)
    
    return options

def process_file(options):
    field_list = zd_lib.get_field_list()
    indexes = get_indexes(field_list, options.fields)
    
    current = []
    equal = False
    prev_line = ''

    print '\t'.join(field_list)
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

    #print current
    return current


options = process_args()
process_file(options)

    
    
