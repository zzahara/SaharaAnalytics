#!/usr/bin/env python

# Copyright 2010 Inyternet Archive
# Written by Zahara Docena
# This program is distributed under the terms of the GNU General Public License v3
# see: http://www.gnu.org/licenses/gpl.txt 

import sys
from sys import argv

total_file = open(argv[1])
flat_file = open(argv[2])

total = float(total_file.readline())
bounces = 0

# count the number of users who only visited one page
for line in flat_file:
    line = line.strip()
    
    if line.startswith('1'):
        bounces = bounces + 1
    else:
        break

bounce_rate = (bounces/total)*100
print "bounce rate = %.2f%%" % (bounce_rate) + '<br><br>'
