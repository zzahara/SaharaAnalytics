#!/usr/bin/env python

# Copyright 2010 Internet Archive
# Written by Zahara Docena
# This program is distributed under the terms of the GNU General Public License v3
# see: http://www.gnu.org/licenses/gpl.txt 

# usage: ./zd_sort.py -f field 
# usage: ./zd_sort.py -f field1 -f field2 ... [-n] [field] [-r]
# e.g. ./zd_sort.py -f page -f loadtime -n loadtime ... (will 1st sort by page, 2nd sort by loadtime numerically for same pages)

# Example: ./zd_sort.py -f ip -f page
# sorts by 1. ip 2. page


# Input:
# ip                         page           loadtime
# 0.29.113.149          www.boy.com            32
# 0.14.789.1            www.abc.com            14
# 0.29.113.149          www.cat.com            32
# 0.29.113.149          www.abc.com            56 
# 0.78.234.654          www.fun.com            78
# ...

# Output:
# ip                         page           loadtime
# 0.14.789.1            www.abc.com            14
# 0.29.113.149          www.abc.com            56 
# 0.29.113.149          www.boy.com            32
# 0.29.113.149          www.cat.com            32
# 0.78.234.654          www.fun.com            78
# ...

# Example: ./zd_sort.py -f page -f loadtime -n loadtime -r

# -r: reversed sort
# -n loadtime: sort loadtime numerically

# Input:
# ip                    	page	            loadtime
# 0.29.113.149      www.abc.com	          6	
# 0.29.113.149      www.boy.com	          7	
# 0.29.113.149      www.cat.com	          8
# 0.14.789.1	        www.abc.com	          3
# 0.78.234.654      www.fun.com	          9
# 0.29.113.149      www.abc.com	          5
# 0.29.113.149      www.abc.com	          4	


# Output:
# ip                    	page	            loadtime
# 0.78.234.654	    www.fun.com	          9
# 0.29.113.149	    www.cat.com	          8	
# 0.29.113.149	    www.boy.com	          7	
# 0.29.113.149	    www.abc.com	          6	
# 0.29.113.149	    www.abc.com	          5
# 0.29.113.149	    www.abc.com	          4	
# 0.14.789.1        	www.abc.com	          3	


import os
import sys
import errno
import zd_lib
from sys import argv
from optparse import OptionParser

argv
field_list = []
sort_fields = []
parser = OptionParser()

def process_args():
    global argv, parser, sort_fields
    parser.add_option("-f", action="append", help="fields to sort by", dest="fields")
    parser.add_option("-n", action="store", help="the field to sort numerically", dest="numeric")
    parser.add_option("-r", action="store_true", help="reverse sort", dest="reverse", default=False)
    parser.add_option("-g", action="store_true", help="general numeric sort (sorts numbers with + correctly)", dest="gen_num", default=False)
    
    (options, args) = parser.parse_args(argv)
    sort_fields = options.fields

    return options

def get_script_args(options):
    global sort_fields, field_list
    field_list = zd_lib.get_field_list_wrapper()

    script_args = []
    script_args.append('')
    length = len(sort_fields)

    numeric = -1
    if options.numeric:
        numeric = field_list.index(options.numeric)
    
    for i in range(0, length):
        try:
            index = field_list.index(sort_fields[i])
            
            other_option = ''
            
            if numeric == field_list[i]:
                other_option = 'n'

            if length > 1 and i != length-1:
                script_args.append('-k')
                script_args.append(str(index+1) + ',' + str(index+1) + other_option)

            else:
                script_args.append('-k')
                script_args.append(str(index+1) + other_option)

        except IOError, e:
            if e.errno == errno.EPIPE:
                exit(0)

    if options.reverse:
        script_args.append('-r')

    if options.gen_num:
        script_args.append('-g')

    return script_args

def sort(script_args):
    global field_list
    first_line = '\t'.join(field_list)
    os.write(1,first_line + '\n')
    os.execv("sort-wrapper", script_args)


# Main
options = process_args()
script_args = get_script_args(options)
sort(script_args)
