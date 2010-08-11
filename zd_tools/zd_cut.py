#!/usr/bin/env python

# Copyright 2010 Internet Archive
# Written by Zahara Docena
# This program is distributed under the terms of the GNU General Public License v3
# see: http://www.gnu.org/licenses/gpl.txt 

# Input: flat file (must include the selected fields to cut)
# Output: flat file (with only the cut fields)

# Example: ./zd_cut.py -f ip -f page

# Input:
# ip                         page               loadtime
# 0.29.113.149          www.yoursite.com         678
# ...

# Output:
# ip                         page     
# 0.29.113.149          www.yoursite.com

import os
import sys
import errno
import zd_lib
import optparse
from sys import argv
from optparse import OptionParser

argv
parser = OptionParser()
cut_fields = []

def process_args():
    global argv, cut_fields, filename
    parser.add_option("-f", action="append", dest="fields") # fields to cut

    (options, args) = parser.parse_args(argv)
    cut_fields = options.fields

def get_script_args():
    field_list = zd_lib.get_field_list_wrapper()
    field_nums = ''

    script_args = ['']
    indexes = []
    field_nums = []
    
    for i in range(0, len(cut_fields)):
        try:
            index = field_list.index(cut_fields[i])
            indexes.append(index)
            field_nums.append(str(index+1))
        except IOError, e:
            if e.errno == errno.EPIPE:
                exit(0)
    try:
        write_first_line(indexes, field_list)
        script_args.append(','.join(field_nums))
    except IOError, e:
        if e.errno == errno.EPIPE:
            exit(0)      
    return script_args

def write_first_line(indexes, field_list):
    fields = []
    indexes.sort()

    for i in range(0, len(indexes)):
        x = indexes[i]
        fields.append(field_list[x])

    first_line = '\t'.join(fields)
    os.write(1, first_line)
    os.write(1,'\n')

def cut(script_args):
    os.execv("cut-wrapper", script_args)

# MAIN

process_args()
script_args = get_script_args()
cut(script_args)




