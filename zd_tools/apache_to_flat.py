#!/usr/bin/env python

# Copyright 2010 Inyternet Archive
# Written by Zahara Docena
# This program is distributed under the terms of the GNU General Public License v3
# see: http://www.gnu.org/licenses/gpl.txt 

# Input: log file
# Output: flat file (first line = field names, each line after lists the field values for that log line)

# Example:
# ip    page    referrer    loadtime    server_ms   timestamp   locale  useragent
# 0.29.113.149	http://www.yoursite.org http://www.google.com 579.0 en-us 03/Aug/2010:00:01:02    en-us   (compatible; MSIE 8.0; Windows NT 6.0; WOW64; Trident/4.0; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.5.21022; .NET CLR 3.5.30729; MDDC; .NET CLR 3.0.30729; InfoPath.1; .NET4.0C)
# 0.17.457.261  http://www.yoursite.org http://www.google.com 579.0 en-us 03/Aug/2010:00:01:02    en-us   -
# (log line values)
# (log line values)
# ...

# Note: A '-' in the place of a field value like above represents no value found (in example above: no useragent found)

import re
import sys
import cgi
import urlparse
import urllib
from sys import argv
from optparse import OptionParser

argv
parser = OptionParser()

def process_args():
    global argv, parser
    parser.add_option("-f", action="append", dest="fields", help="the fields to add in the flat file")

    (options, args) = parser.parse_args(argv)
    parserOptions = options

    return options

# img_src = bug request made on analytics.js
def process_file(file, img_src, options):
    pattern = '(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) [^ ]+ [^ ]+ \[(?P<timestamp>../.../....:..:..:..) .....\] ' + '"GET (?P<bug>' + img_src + '\?[^ ]+)( HTTP/1\.\d)?" (?P<status>\d{3}) (?P<size>[^ ]+) "(?P<page>[^"]+)" "(?P<useragent>[^"]+)"'
    c = re.compile(pattern)

    total_lines = 0
    count_no_match = 0
    regex_no_match = 0
    
    print_field_line(options.fields)
    for log_line in file:
        m = c.match(log_line)
        
        if m:
            page_data = m.groupdict()

            if page_data['page'] == '-':
                continue
            bug_values = get_bug_values(page_data['bug'], img_src)
            page_data.update(bug_values)

            # count = the number of bug values that should be in the bug
            # bug values are separated by '&'
            # ampersands in the referrer bug value will result in a miscount
            if 'count' in bug_values and int(bug_values['count']) == len(bug_values):
                print_page_values(page_data, bug_values, options.fields)
            else:
                #sys.stderr.write('COUNT DOES NOT MATCH: ' + log_line + '\n')
                count_no_match = count_no_match + 1
            
        else:
            #sys.stderr.write('REGEX DOES NOT MATCH: ' + log_line + '\n')
            regex_no_match = regex_no_match + 1
            
        total_lines = total_lines + 1

    sys.stderr.write("count didn't match: " + str(count_no_match) + '\n')
    sys.stderr.write("regex didn't match: " + str(regex_no_match) + '\n')
    sys.stderr.write("total lines = " + str(total_lines) + '\n')

# parse the values the analytics.js bug generated
# return values in a dictionary (associated array)
def get_bug_values(bug, img_src):
    bug_values = cgi.parse_qs(urlparse.urlparse(bug)[4])

    for key in bug_values:
        bug_values[key] = bug_values[key][0]

    return bug_values

# prints the first line of the flat file
def print_field_line(fields):
    print '\t'.join(fields)

# prints page values separated by tabs           
def print_page_values(page_data, bug_values, fields):
    values = []
    
    for field in fields:
        if field in page_data and page_data[field].strip() != '':
            if field in bug_values:
                page_data[field] = urllib.unquote(page_data[field])

            # checks for & removes any interfering chars
            if '\n' in page_data[field]:
                page_data[field] = page_data[field].replace('\n', '')

            if '\t' in page_data[field]:
                page_data[field] = page_data[field].replace('\t', '')

            if '\r' in page_data[field]:
                page_data[field] = page_data[field].replace('\r', '')

            values.append(page_data[field])
            
        else:
            values.append('-')
            
    print '\t'.join(values) 

options = process_args()
# 0.gif holds the 1 pixel image that is loaded with the bug values as parameters (during the GET request)
process_file(sys.stdin, '/0.gif', options)

