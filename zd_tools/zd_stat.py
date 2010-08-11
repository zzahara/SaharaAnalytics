#!/usr/bin/env python

# Copyright 2010 Internet Archive
# Written by Zahara Docena
# This program is distributed under the terms of the GNU General Public License v3
# see: http://www.gnu.org/licenses/gpl.txt 

# Input: flat file (must be sorted by the grouping specified in the options)
# Output: flat file (with new field columns of the desired statistics)

# usage: ./zd_stat.py ...desired options... -g field1 -g field2 -d values
# required: -g field1 -d values

# Example 1: ./zd_stat.py -a ave_load -c num_vals -g ip -d loadtime

#   -option name:
#       - name is the name of the new column with the statistics for that option
#       - e.g. -a ave_loadtime:
#             the name of the field with the average is ave_loadtime

#   -g ip: 
#       - the input flat file is sorted by ip
#       - the program will compute the statistics of this grouping

#   -d loadtime:
#       - the program will compute the statistics of these values

# Input:
# ip                         page           loadtime
# 0.29.113.149          www.abc.com            56 
# 0.29.113.149          www.abc.com            47 
# 0.29.113.149          www.abc.com            38 
# 0.29.113.149          www.boy.com            32
# 0.29.113.149          www.cat.com            32
# 0.14.789.1            www.abc.com            14
# 0.78.234.654          www.fun.com            78
# ...


# Output:
# ip                         page           loadtime      ave_load          num_values
# 0.29.113.149          www.abc.com            56           41                  5
# 0.29.113.149          www.abc.com            47           41                  5
# 0.29.113.149          www.abc.com            38           41                  5
# 0.29.113.149          www.boy.com            32           41                  5
# 0.29.113.149          www.cat.com            32           41                  5
# 0.14.789.1            www.abc.com            14           14                  1
# 0.78.234.654          www.fun.com            78           78                  1
# ...


# Example 2: ./zd_stat.py -a ave_load -c num_vals -t tp99_load -s standard_dev -g ip -g page -g locale -d loadtime

#   -g ip -g page: 
#       - the input flat file is sorted by 1. ip 2. page
#       - the program will compute the statistics of this grouping

# Input:
# ip                         page           loadtime
# 0.29.113.149          www.abc.com            56 
# 0.29.113.149          www.abc.com            47 
# 0.29.113.149          www.abc.com            38 
# 0.29.113.149          www.boy.com            32
# 0.29.113.149          www.cat.com            32
# 0.14.789.1            www.abc.com            14
# 0.78.234.654          www.fun.com            78
# ...


# Output:
# ip                         page           loadtime      tp99_load      ave_load       num_values
# 0.29.113.149          www.abc.com            56             56            47              3
# 0.29.113.149          www.abc.com            47             56            47              3
# 0.29.113.149          www.abc.com            38             56            47              3
# 0.29.113.149          www.boy.com            32             32            32              1
# 0.29.113.149          www.cat.com            32             32            32              1
# 0.14.789.1            www.abc.com            14             14            14              1
# 0.78.234.654          www.fun.com            78             78            78              1
# ...

import re
import sys
import math
import errno
import zd_lib
from sys import argv
from optparse import OptionParser

argv
parser = OptionParser()


def process_args():
    global argv, parser
    parser.add_option("-c", action="store", dest="count", help="counts the size of each group", default="-")
    parser.add_option("-t", action="store", dest="tp99", help="calculates tp99", default="-")
    parser.add_option("-a", action="store", dest="ave", help="calculates average load time", default="-")
    parser.add_option("-s", action="store", dest="standard_dev", help="calculates standard deviation", default="-")
    parser.add_option("-g", action="append", dest="grouping", help="calculates the statistics on the given grouping")
    parser.add_option("-d", action="store", dest="data", help="calculates the statistics of these values", default="loadtime")
 
    (options, args) = parser.parse_args(argv)
    return options


def process_file(options):
    field_list = zd_lib.get_field_list()
    print_field_line(field_list)

    # store the indexes of grouping fields
    grouped_by = []
    for field in options.grouping:
        grouped_by.append(field_list.index(field))
    
    data_field = field_list.index(options.data)

    current = [] # current field values of the current group
    data = [] # data the statistics will be computed over
    saved_lines = [] # log lines in the current group

    for log_line in sys.stdin:
        try:
            log_line = log_line.rstrip()
            log_data = log_line.split('\t')

            # first group
            if len(current) == 0:
                current = get_current(log_data, grouped_by)

            if in_group(log_data, grouped_by, current):
                data.append(log_data[data_field])
                saved_lines.append(log_line)           
            else:
                # end of group so calculate stats
                stats = calculate_stats(options, data)
                print_lines(saved_lines, stats)

                # store new group's values
                current = get_current(log_data, grouped_by)
                data = []
                saved_lines = []

                data.append(log_data[data_field])
                saved_lines.append(log_line)  

        except IOError, e:
            if e.errno == errno.EPIPE:
                exit(0)

    # last group
    try:
        stats = calculate_stats(options, data)
        print_lines(saved_lines, stats)
    except IOError, e:
            if e.errno == errno.EPIPE:
                exit(0)

# gets the field values of the current group
def get_current(log_data, grouped_by):
    current = []

    for field_index in grouped_by:
        value = log_data[field_index]
        current.append(value)

    return current

# verifies if a log line belongs in the current group
def in_group(log_data, grouped_by, current):
    i = 0
    for field_num in grouped_by:
        if log_data[field_num] != current[i]:
            return False
            
        i = i + 1

    return True


# ------------------------------------------------------------
#                Printing Functions
# ------------------------------------------------------------  


def print_field_line(fields):
    stats = []

    if options.tp99 != '-':
        stats.append(options.tp99)

    if options.ave != '-':
        stats.append(options.ave)
    
    if options.standard_dev != '-':
        stats.append(options.standard_dev)

    if options.count != '-':
        stats.append(options.count)

    print '\t'.join(fields) + '\t',
    print '\t'.join(stats)


def print_lines(lines, stats):
    for log in lines:
        print log.rstrip() + '\t',
        print '\t'.join(stats)

# ------------------------------------------------------------
#                Calculating Statistics Functions
# ------------------------------------------------------------  

def calculate_stats(options, values):
    stats = []
    if options.tp99 != '-':
        tp99 = calc_tp99(values, 10)
        stats.append(str(tp99))

    if options.ave != '-':
        ave = calc_ave(values)
        stats.append(str(ave))
    
    if options.standard_dev != '-':
        standard_dev = calc_standard_dev(values)
        stats.append(str(standard_dev))

    if options.count != '-':
        stats.append(str(len(values)))

    return stats

def calc_tp99(values, percentile):
    group = []

    group_len = ((percentile/float(100)) * len(values))

    # round accordingly
    if group_len < 1:
        group_len = 1
    else:
        group_len = int(round(group_len))

    for i in range(0, group_len):
        group.append(values[i])
        
    return calc_ave(group)
    
def calc_ave(values):
    sum = 0
    for x in values:
        if x != '-':
            val = float(x)
            sum = sum + val

    ret_val = sum/len(values)

    if ret_val == 0:
        return '-'
    return ret_val

def calc_standard_dev(values):
    average = calc_ave(values)
    sum = 0.0

    if len(values) <= 1:
        return 0

    else:
        for x in values:
            if x != '-':
                val = float(x)
                sum = sum + math.pow((val-average), 2)

        return math.sqrt(sum/(len(values)-1))

# Main
options = process_args()
process_file(options)


