#!/usr/bin/env python

# Copyright 2010 Internet Archive
# Written by Zahara Docena
# This program is distributed under the terms of the GNU General Public License v3
# see: http://www.gnu.org/licenses/gpl.txt 

# Input: flat file (must include the selected fields in the condition)
# Output: flat file (with lines that satisfy the given condition)

# Example 1: ./zd_select.py "d['loadtime'] > 100"

# Input:
# ip                         page               loadtime
# 0.29.113.149          www.yoursite.com         6789
# 0.29.113.149          www.yoursite.com         56
# ...

# Output:
# ip                         page               loadtime
# 0.29.113.149          www.yoursite.com         6789

# Example 2: ./zd_select.py "d['loadtime'] > 100 and d['referrer'].startswith('http://www.google.com')"

# Input:
# ip                         page               loadtime        referrer
# 0.29.113.149          www.yoursite.com         6789           http://www.google.com/search?sourceid=chrome&ie=UTF-8&q=archive
# 0.29.113.149          www.yoursite.com         56             http://www.yahoo.com
# ...

# Output:
# ip                         page               loadtime        referrer
# 0.29.113.149          www.yoursite.com         6789           http://www.google.com/search?sourceid=chrome&ie=UTF-8&q=archive

import re
import sys
import math
import errno
import zd_lib
from sys import argv
from optparse import OptionParser

argv

def process_args():
    global argv

    if len(argv) != 2:
        print 'usage: ./zd_select "condition"'
        return False
        
    return True

def process_file():
    global argv
    field_list = zd_lib.get_field_list()
    exec("include = lambda d: " + argv[1])

    print '\t'.join(field_list)
    for log_line in sys.stdin:
        try:
            log_line = log_line.rstrip()
            log_data = log_line.split('\t')
            line = list_to_dict(log_data, field_list)
        
            if include(line):
                print log_line

        except IOError, e:
            if e.errno == errno.EPIPE:
                exit(0)       


def list_to_dict(log_data, field_list):
    return_dict = dict()

    for i in range(0, len(field_list)):
        return_dict[field_list[i]] = log_data[i]

    return return_dict

# Main
if process_args():
    process_file()

    
    
