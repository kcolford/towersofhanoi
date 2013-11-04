#!/usr/bin/python3

from test import m
from sys import argv, stdin
from os import popen


def plot3d():
    with popen('gnuplot -p', 'w') as p:
        print('splot "-"', file=p)
        for k in range(7, 30):
            for n in range(300):
                print(k, n, m(k, n), file=p)

def main():
    c = 'plot "-" smooth unique title "{}"'
    c = "gnuplot -e 'set term pstex; " + c + "'"
    for a, b in zip(stdin, argv[1:]):
        s = c.format(b)
        with popen(s, 'w') as p:
            for x in range(100):
                print(x, eval(a), file=p)

if __name__ == '__main__':
    if len(argv) > 1:
        main()
    else:
        plot3d()
