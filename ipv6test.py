# ipv6test - unit test the ipv6 module

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
from ipv6 import *

class testIPv6Addr(unittest.TestCase):
  def setUp(self):
    self.text = "2002:4b20:0000:0000:0000:0000:00a2:0007"
    self.addr = IPv6Addr(self.text)
#some samples for testing correctness and for timing tests
    self.v6addrs = ["ABCD:EF01:2345:6789:ABCD:EF01:2345:6789",
       "2001:DB8:0:0:8:800:200C:417A",
       "FF01:0:0:0:0:0:0:101",
       "FF01::101",
       "0:0:0:0:0:0:0:1",
       "::1",
       "0:0:0:0:0:0:0:0",
       "::",
       "::0.0.0.0",
       "2001:DB8::8:800:200C:417A",
       "0:0:0:0:0:0:13.1.68.3",
       "::13.1.68.3",
       "0:0:0:0:0:FFFF:129.144.52.38",
       "::FFFF:129.144.52.38",
       "2001:0DB8:0000:CD30:0000:0000:0000:0000",
       "2001:0DB8::CD30:0000:0000:0000:0000",
       "2001:0DB8:0000:CD30::",
       "2001:0DB8:0:CD30:123:4567:89AB:CDEF",
       "FF00::",
       "FF01:0:0:0:0:0:0:101",
       "FF0F:0:0:0:0:0:0:0",
       "FF02:0:0:0:0:1:FF00:0000",
       "FF02:0:0:0:0:1:FFFF:FFFF",
       "3ffe:501:8:0:260:97ff:fe40:efab",
       "3ffe:501:8::260:97ff:fe40:efab",
       "fe80::260:97ff:fe40:efab",
       "3ffe:501:4819:2000:5254:ff:fedc:50d2",
       "2001:0db8:0000:0000:0000:0000:1428:57ab",
       "2001:0db8:0000:0000:0000::1428:57ab",
       "2001:0db8:0:0:0:0:1428:57ab",
       "2001:0db8:0:0::1428:57ab",
       "2001:0db8::1428:57ab",
       "2001:db8::1428:57ab",
       "::ffff:1.2.3.4",
       "::ffff:102:304",
       "0000:0000:0000:0000:0000:0000:111.222.111.222",
       "1080::8:800:200C:417A",
       "1080:0:0:0:8:800:200C:417A",
       "1080:0000:0000:0000:0008:0800:200C:417A",
       "1762:0:0:0:0:B03:1:AF18",
       "1762::B03:1:AF18",
       "FF01:0:0:0:CA:0:0:2",
       "FF01::CA:0:0:2",
       "FF01:0:0:0:CA::2",
       "0:0:0:0:0:0:127.32.67.15",
       "::127.32.67.15",
       "0:0:0:0:0:FFFF:127.32.67.15",
       "::FFFF:127.32.67.15",
       "FEC0:0000:0000:0000:02AA:00FF:FE3F:2A1C",
       "FEC0:0:0:0:2AA:FF:FE3F:2A1C",
       "FEC0::2AA:FF:FE3F:2A1C",
       "455F:E104:22CA:29C4:933F:9505:2B79:2AB2",
       "09F9:1102:9D74:E35B:D841:56C5:6356:88C0"]
    self.v6bits = [ 'abcdef0123456789abcdef0123456789',
           '20010db80000000000080800200c417a',
           'ff010000000000000000000000000101',
           'ff010000000000000000000000000101',
           '00000000000000000000000000000001',
           '00000000000000000000000000000001',
           '00000000000000000000000000000000',
           '00000000000000000000000000000000',
           '00000000000000000000000000000000',
           '20010db80000000000080800200c417a',
           '0000000000000000000000000d014403',
           '0000000000000000000000000d014403',
           '00000000000000000000ffff81903426',
           '00000000000000000000ffff81903426',
           '20010db80000cd300000000000000000',
           '20010db80000cd300000000000000000',
           '20010db80000cd300000000000000000',
           '20010db80000cd300123456789abcdef',
           'ff000000000000000000000000000000',
           'ff010000000000000000000000000101',
           'ff0f0000000000000000000000000000',
           'ff0200000000000000000001ff000000',
           'ff0200000000000000000001ffffffff',
           '3ffe050100080000026097fffe40efab',
           '3ffe050100080000026097fffe40efab',
           'fe80000000000000026097fffe40efab',
           '3ffe050148192000525400fffedc50d2',
           '20010db80000000000000000142857ab',
           '20010db80000000000000000142857ab',
           '20010db80000000000000000142857ab',
           '20010db80000000000000000142857ab',
           '20010db80000000000000000142857ab',
           '20010db80000000000000000142857ab',
           '00000000000000000000ffff01020304',
           '00000000000000000000ffff01020304',
           '0000000000000000000000006fde6fde',
           '108000000000000000080800200c417a',
           '108000000000000000080800200c417a',
           '108000000000000000080800200c417a',
           '176200000000000000000b030001af18',
           '176200000000000000000b030001af18',
           'ff0100000000000000ca000000000002',
           'ff0100000000000000ca000000000002',
           'ff0100000000000000ca000000000002',
           '0000000000000000000000007f20430f',
           '0000000000000000000000007f20430f',
           '00000000000000000000ffff7f20430f',
           '00000000000000000000ffff7f20430f',
           'fec000000000000002aa00fffe3f2a1c',
           'fec000000000000002aa00fffe3f2a1c',
           'fec000000000000002aa00fffe3f2a1c',
           '455FE10422CA29C4933F95052B792AB2',
           '09F911029D74E35BD84156C5635688C0']
  def testaton(self):
    for i,j in zip(self.v6addrs,self.v6bits):
      a = IPv6Addr(i)
      self.assertEqual(a.tohex().upper(),j.upper())
  def testInOut(self):
    self.assertEqual(self.text.upper(),self.addr.tonorm().upper())

def suite():
  suite = unittest.TestSuite()
  suite.addTest(unittest.makeSuite(testIPv6Addr))
  return suite

if __name__ == "__main__":
  unittest.TextTestRunner(verbosity=2).run(suite())

