#!/usr/bin/env python

# Copyright 2010 Inyternet Archive
# Written by Zahara Docena
# This program is distributed under the terms of the GNU General Public License v3
# see: http://www.gnu.org/licenses/gpl.txt 


import sys
from sys import argv

total_file = open(argv[1])
flat_file = open(argv[2])
field = argv[3]

total = float(total_file.readline())
count = 0

print 'percent' + '\t' + 'count' + '\t' + field
for line in flat_file:
    array = line.split()
    count = int(array[0])
    percentage = (count/total) * 100

    print '  ' + "%6.2f%%" % (percentage) + '\t' + str(count)  + '\t' + array[1]


