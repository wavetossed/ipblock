# ipv6 - module to support IPv6 addresses, ranges, and lists.

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

import socket

_hdigs = ('0', '1', '2', '3', # hex digits for storing
          '4', '5', '6', '7', # numbers as hex strings
          '8', '9', 'A', 'B',
          'C', 'D', 'E', 'F')
_hbits = ('0000', '0001', '0010', '0011', # hex bits for printing
          '0100', '0101', '0110', '0111', # numbers in binary format
          '1000', '1001', '1010', '1011',
          '1100', '1101', '1110', '1111')

class IPv6Addr(object):
  "128 bit IPv6 addresses"
  def __init__(self,a):
    "initialize from either a bit array or colon hex notation"
    if isinstance(a,(list,tuple)):
      self.addr = ""
    elif isinstance(a,str):
      self.addr = v6_inet_aton(a)

#  def tobin(self):
#    return ''.join([ ''.join((_hbits[ord(i)>>4],
#                              _hbits[ord(i)&0xf])) for i in self.bits])
  def tohex(self):
    return ''.join([ ''.join((_hdigs[ord(i)>>4],
                              _hdigs[ord(i)&0xf])) for i in self.addr])
  def tonorm(self):
    abytes = self.tohex()
    return ':'.join([abytes[i:i+4] for i in range(0,32,4)])

# IPv6 helper functions

_zeroaddr = ["0000", "0000", "0000", "0000", "0000", "0000", "0000", "0000"]
_sockinetaton = socket.inet_aton
def v6_inet_aton(a):
  "converts RFC 4291 string format to internal binary octets"
  c = a.split("::")
  if len(c) > 2: raise ValueError("Only one :: allowed by RFC 4291")
  if len(c) == 1: c.insert(0,"")
  if c[1].rfind(".") >= 0: # if dots in second part, parse out IPv4 quad
    rightparts = c[1].rsplit(":") 
    if len(rightparts) == 1:
      rbits = _sockinetaton(rightparts[0]).encode("hex_codec")
      c[1] = [rbits[:4],rbits[4:]]
    else:
      rbits = _sockinetaton(rightparts[-1]).encode("hex_codec")
      c[1] = [ b.zfill(4) for b in rightparts[0:-1]] +\
             [rbits[:4],rbits[4:]]
  else:
    c[1] = [ b.zfill(4) for b in c[1].split(":")]
  if c[0] != "": c[0] = [ b.zfill(4) for b in c[0].split(":")]
  #print " @ ",c[0]," @ ",c[1]
  return "".join(["".join(c[0]),
                  "".join(_zeroaddr[0:8-(len(c[0])+len(c[1]))]),
                  "".join(c[1])]).decode("hex_codec")

if __name__ == "__main__":
  print "This is an import module"
