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
Hanoi running time.
"""

import doctest
import unittest
from functools import lru_cache


__all__ = ['time', 'm']


class Tester(unittest.TestCase):
   """
   This is the test case for checking the accuracy of the module's
   time solving methods.
   """
   def test_main(self: 'Tester') -> None:
      """
      Run a test to make sure that method m behaves the same as time.
      Since we cannot test all possible inputs, we only test a small
      number.
      """
      for k in range(2, 30):
         for n in range(8, 60):
            self.assertEqual(m(k, n), time(n, k))


@lru_cache(None)
def time(n: int, m: int) -> int:
   """
   Compute the minimum time needed to solve the Towers of Hanoi
   problem consisting of n disks and m towers (not including the
   starting tower and end tower).

   Dynamic programming is implemented via @functools.lru_cache(None).

   >>> time(8, 2)
   33
   """
   if m == 1 or n == 1:
      return 2**n - 1

   return min(time(i, m - 1) + 2 * time(n - i, m) for i in range(1, n))

@lru_cache(None)
def fac(n: int) -> int:
   """
   Compute the factorial of (the product of all positive integers upto
   and including) n.

   This uses a recursive method of solving combined with
   @functools.lru_cache(None) for dynamic programming.

   >>> fac(5)
   120
   >>> fac(0)
   1
   """
   return 1 if n <= 1 else n * fac(n - 1)

def m(k: int, n: int) -> int:
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
   # set up helper function to compute nested sums
   f = lambda x, y: fac(x + y - 1) // fac(x) // fac(y - 1)

   # compute the largest integer a that's smaller than n (via linear
   # search)
   a = 0
   while f(k, a + 1) <= n:
      a += 1
   # compute the overflow
   w = n - f(k, a)

   # compute the value of h_k(a)
   h_ka = sum((-1)**(k + 1 - b) * f(b, a) for b in range(k))

   # return the answer
   return (h_ka + w) * 2**a + (-1)**k if n else 0

if __name__ == '__main__':
   doctest.testmod()
   #unittest.main()
