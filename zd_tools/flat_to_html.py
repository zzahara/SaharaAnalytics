#!/usr/bin/env python

# Copyright 2010 Internet Archive
# Written by Zahara Docena
# This program is distributed under the terms of the GNU General Public License v3
# see: http://www.gnu.org/licenses/gpl.txt 

# Input: flat file
# Output: html file

import os
import sys
from sys import argv
from optparse import OptionParser

argv
parser = OptionParser()

def process_args():
    global argv, parser
    parser.add_option("--header", action="store_true", dest="header", help="includes a table header based on the first line of the flat file", default=False)
 
    (options, args) = parser.parse_args(argv)
    return options

def process_file(options):
    field_list = get_field_list()
    print '<table border=\"1\" cellpadding=\"5\" cellspacing=\"1\" width=\"50%\">'
    if options.header:
        print_table_header(field_list)

    for log_line in sys.stdin:
        log_line = log_line.rstrip()
        log_data = log_line.split('\t')
        print_table_row(log_data)

    print '</table>'

def get_field_list():
    first_line = sys.stdin.readline()
    first_line = first_line.rstrip()

    field_list = first_line.split('\t')
    return field_list

def print_table_header(fields):
    print '<tr>',
    
    for x in fields:
        print '<th>' + str(x) + '</th>',

    print '</tr>'

def print_table_row(log_data):
    print '<tr>',

    for x in log_data:
        x = x.strip()
        if (x.startswith('http://')):
            print '<td width=\"20%\"><a href=\"' + str(x) + '\">' + str(x) + '</a></td>',

        elif(is_float(x)):
            print '<td width=\"20%\">' + "%.2f" % (float(x)) + '</td>',
        
        else:
            print '<td width=\"20%\">' + str(x) + '</td>',

    print '</tr>'

def is_float(x):
    try:
        float(x)
        return True
    except ValueError:
        return False

# Main
options = process_args()
process_file(options)




