#!/usr/bin/python3

# Copyright (C) 2013  Kieran Colford

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see
# <http://www.gnu.org/licenses/>.


"""
This module contains a series of methods for computing the Towers of
Hanoi.
"""

import doctest
import unittest
import profile
from functools import lru_cache


__all__ = ['get_time', 'solve', 'm']


class Tester(unittest.TestCase):
   """
   This is the test case for checking the accuracy of the module's
   time solving methods.
   """
   def test_main(self):
      """
      Run a test to make sure that method m behaves the same as
      get_time.  Since we cannot test all possible inputs, we only
      test a small number.
      """
      for k in range(2, 30):
         for n in range(8, 60):
            self.assertEqual(m(k, n), get_time(n, k))


def get_time(n, m):
   pass

@lru_cache(None)
def get_i(n, m):
   """
   Return the ideal factor by which to split a stack of n disks with m
   extra towers.

   Dynamic programming is implemented via @functools.lru_cache(None).

   >>> get_i(31, 5)
   15
   >>> get_i(40, 3)
   15
   >>> get_i(40, 5)
   19
   """
   assert m > 0 or n == 1      
   func = lambda i: 2 * get_time(n - i, m) + get_time(i, m - 1)
   return 1 if m == 1 or n == 1 else min(range(1, n), key=func)

@lru_cache(None)
def get_time(n, m):
   """
   Compute the minimum time needed to solve the Towers of Hanoi
   problem consisting of n disks and m towers (not including the
   starting tower and end tower).

   Dynamic programming is implemented via @functools.lru_cache(None).

   >>> get_time(8, 2)
   33
   """
   assert m > 0 or n == 1
   if n == 1: return 1
   if m == 1: return 2 ** n - 1
   i = get_i(n, m)
   return 2 * get_time(n - i, m) + get_time(i, m - 1)

def towers(n, m):
   """
   Generate a nested list of ints to represent the Towers of Hanoi,
   using the ints as the size of the "disk".
   """
   assert m > 0
   assert n > -1
   return [list(range(n, -1, -1))] + [[n] for i in range(m + 1)]

def move(t, frm, to, n):
   """
   Move n disks from the tower t[frm] to the tower t[to] and print out
   each intermediate step.
   """
   assert t[frm][-1] < t[to][-1]
   if n == 1:
      # do the base case move and print out the new set up
      t[to].append(t[frm].pop())
      print(t)
   else:
      # do some extra calculations to find out what can be used a
      # temporary and what the best way to solve it is
      l = [i for i in range(len(t)) if t[frm][-1] < t[i][-1]]
      l.remove(to)
      assert len(l) > 0
      tmp, i = l[0], get_i(n, len(l))
      # perform the actual move
      move(t, frm, tmp, n - i)
      move(t, frm, to, i)
      move(t, tmp, to, n - i)

def solve(n, m):
   """
   High level function to set up m + 2 towers with n disks on the
   first one, and solve it while printing out each step.
   """
   a = towers(n, m)
   print(a)
   move(a, 0, m + 1, n)

@lru_cache(None)
def factorial(n):
   """
   Compute the factorial of (the product of all positive integers upto
   and including) n.

   This uses a recursive method of solving combined with
   @functools.lru_cache(None) for dynamic programming.

   >>> factorial(5)
   120
   >>> factorial(0)
   1
   """
   
   return 1 if n <= 1 else n * factorial(n - 1)

def f(k, a):
   """
   Compute the binomial coefficient of a + k - 1 choose k.

   >>> f(0, 30)
   1
   >>> f(1, 20)
   20
   >>> f(2, 3)
   6
   >>> f(3, 0)
   0
   """
   return factorial(a + k - 1) // factorial(k) // factorial(a - 1)

def h(k, a):
   """
   This is a helper function for method m.

   >>> h(1, 3)
   1
   >>> h(1, 20)
   1
   >>> h(2, 30)
   29
   >>> h(3, 0)
   0
   """
   p = sum(f(b, a) for b in range(k - 1, -1, -2))
   m = sum(f(b, a) for b in range(k - 2, -1, -2))
   return p - m

def break_input(k, n):
   """
   This is helper function for method m, it computes the largest
   integer a that satisfies f(k, a) <= n

   >>> break_input(1, 15)
   15
   >>> break_input(2, 8)
   3
   >>> break_input(4, 0)
   0
   """
   a = 0
   while f(k, a + 1) <= n:
      a += 1
   return a

def m(k, n):
   """
   This function computes the time it takes to solve the Towers of
   Hanoi problem with k extra towers and n disks.

   It does this by computing a closed form solution.

   An extraordinary fact about this method is that the Wikipedia
   article on the Towers of Hanoi claims that it is unknown how long
   it takes to solve a puzzle with 10 pegs (k = 8) and 1,000 disks (n
   = 1000).
   
   >>> m(8, 1000)
   22561

   ...I guess this is why you should take everything said by Wikipedia
   with a grain of salt.
   
   >>> m(3, 0)
   0
   >>> m(2, 8)
   33
   >>> m(2, 9)
   41
   >>> m(3, 10)
   31
   >>> m(4, 100)
   1729
   >>> m(15, 100)
   367
   """
   if n == 0: return 0
   if k == 1: return 2**n - 1
   a = break_input(k, n)
   w = n - f(k, a)
   u = break_input(k - 1, w)
   ret = (h(k, a) + h(k, u)) * 2**a + (-1)**k
   if w:
      ret += 2**(a - u) * (m(k - 1, w) + (-1)**k)
   return ret

def main():
   """
   Run the profiler and test cases for this module.  You can choose
   what to run by (un)commenting the options you want.
   """
   # simple test
   doctest.testmod()
   # profiling
   #profile.run('[m(i, 100) for i in range(2, 20)]')
   # full test, toggle 
   #unittest.main()

if __name__ == '__main__':
   main()
