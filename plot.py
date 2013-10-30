#!/usr/bin/python3

from test import m
from sys import argv, stdin
from os import popen

c = 'plot "-" smooth unique title "{}"'
c = "gnuplot -e 'set term pstex; " + c + "'"

for a in stdin:
    with popen(c.format(argv[1]), 'w') as p:
        for x in range(100):
            print(x, eval(a), file=p)
