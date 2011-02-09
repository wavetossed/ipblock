# ipv4test - unit test the ipv4 module

# Copyright (c) 2007,2011 Michael Dillon
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

#  -  Redistributions of source code must retain the above copyright notice,
#     this list of conditions and the following disclaimer.
#  -  Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in
#     the documentation and/or other materials provided with the distribution.
#  -  Neither the name of the developing organization nor the names of its
#     contributors may be used to endorse or promote products derived from
#     this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import unittest
from ipv4 import *

class testIPv4Addr(unittest.TestCase):
  def setUp(self):
    self.quad = "234.10.117.3"
    self.addr = IPv4Addr(self.quad)
  def testInOut(self):
    self.assertEqual(self.quad,self.addr.long2quad())
  def testEquals(self):
    a1 = IPv4Addr("0.0.1.2")
    a2 = IPv4Addr(258L)
    self.assertTrue(a1 == a2)
  def testAnd(self):
    a1 = IPv4Addr("234.10.117.3")
    m1 = IPv4NetMask(24)
    r = a1 & m1
    ri = a1 & m1.inversemask()
    self.assertEqual(r.bits,IPv4Addr("234.10.117.0").bits)
    self.assertEqual(ri.bits,IPv4Addr("0.0.0.3").bits)

class testIPv4Mask(unittest.TestCase):
  def setUp(self):
    self.addr = "196.115.109.77"
    self.maskedaddr = "C4736D00".decode("hex_codec")
    self.netmask = "FFFFFF00".decode("hex_codec")
    self.invmask = "000000FF".decode("hex_codec")
    self.str = "255.255.255.0"
  def testHexMask(self):
    self.assertEqual(self.netmask,IPv4Mask(0xffffff00L).bits)
  def testInverseMask(self):
    self.assertEqual(self.invmask,IPv4Mask(0xffffff00L).inversemask().bits)
  def testMaskAddr(self):
    m = IPv4Addr(self.addr) & IPv4Mask(self.netmask)
    self.assertEqual(self.maskedaddr,m.bits)

class testIPv4NetMask(unittest.TestCase):
  def setUp(self):
    self.numbits = 24
    self.addr = "196.115.109.77"
    self.maskedaddr = "C4736D00".decode("hex_codec")
    self.netmask = "FFFFFF00".decode("hex_codec")
    self.invmask = "000000FF".decode("hex_codec")
    self.str = "255.255.255.0"
  def testHexMask(self):
    self.assertEqual(self.netmask,IPv4NetMask(self.numbits).bits)
  def testMask(self):
    self.assertEqual(self.str,IPv4NetMask(self.numbits).netmask())
  def testMaskAddr(self):
    m = IPv4Addr(self.addr) & IPv4NetMask(24)
    self.assertEqual(self.maskedaddr,m.bits)
  def testLen(self):
    m = IPv4NetMask(self.numbits)
    self.assertEqual(256,len(m))
  def testInverseMask(self):
    m = IPv4NetMask(self.numbits)
    self.assertEqual(m.inversemask().bits,self.invmask)


class testIPv4Range(unittest.TestCase):
  def setUp(self):
    self.a1 = "204.17.22.0"
    self.a2 = "204.17.22.31"
    self.a3 = "204.17.22.1"
    self.a4 = "204.17.22.30"
  def testCreate(self):
    r = IPv4Range(self.a1,self.a2)
    self.assertEqual(self.a1,r.start.__str__())
    self.assertEqual(self.a2,r.end.__str__())
  def testContains(self):
    "test containing a range, an addr, and inverted (contained by)"
    r = IPv4Range(self.a1,self.a2)
    rc = IPv4Range(self.a3,self.a4)
    self.assertTrue(r.__contains__(rc))
    self.assertTrue(r.__contains__(self.a4))
    self.assertFalse(r.__contains__(IPv4Range("204.16.22.0","204.17.22.63")))
    self.assertTrue(IPv4Range("204.16.22.0","204.17.22.63").__contains__(r))
  def testOverlaps(self):
    "test left, right, full (like contains) and no overlap"
    r = IPv4Range(self.a1,self.a2)
    self.assertTrue(r.overlaps(IPv4Range("204.16.22.0","204.17.22.7")))
    self.assertTrue(r.overlaps(IPv4Range("204.17.22.8","204.17.22.63")))
    self.assertTrue(r.overlaps(IPv4Range("204.16.22.0","204.17.22.63")))
    self.assertFalse(r.overlaps(IPv4Range("204.16.22.0","204.16.22.63")))
  def testAddrs(self):
    r = IPv4Range(self.a1,self.a2)
    self.assertEqual(32,len(r.addrs()))

class testIPv4CIDR(unittest.TestCase):
  def setUp(self):
    self.a1 = "204.17.22.0"
    self.a2 = "204.17.22.30"
    self.a3 = "204.17.22.31"
    self.m = IPv4Mask("255.255.255.224")
  def testCreate(self):
    r = IPv4CIDR(self.a1,self.m)
    self.assertEqual(self.a1,r.start.__str__())
    self.assertEqual(self.a3,r.end.__str__())

def suite():
  suite = unittest.TestSuite()
  suite.addTest(unittest.makeSuite(testIPv4Addr))
  suite.addTest(unittest.makeSuite(testIPv4Mask))
  suite.addTest(unittest.makeSuite(testIPv4NetMask))
  suite.addTest(unittest.makeSuite(testIPv4Range))
  suite.addTest(unittest.makeSuite(testIPv4CIDR))
  return suite

if __name__ == "__main__":
  unittest.TextTestRunner(verbosity=2).run(suite())
