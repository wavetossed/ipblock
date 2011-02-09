# ipv4 - module to support IPv4 addresses, ranges, and lists.

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

import socket, struct, bisect

_structunpack = struct.unpack
_structpack = struct.pack
_sockinetaton = socket.inet_aton
_sockinetntoa = socket.inet_ntoa
_hdigs = ('0', '1', '2', '3', # hex digits for storing
          '4', '5', '6', '7', # numbers as hex strings
          '8', '9', 'A', 'B',
          'C', 'D', 'E', 'F')
_hbits = ('0000', '0001', '0010', '0011', # hex bits for printing
          '0100', '0101', '0110', '0111', # numbers in binary format
          '1000', '1001', '1010', '1011',
          '1100', '1101', '1110', '1111')
class IPv4Addr(object):
  "32-bit IPv4 addresses"
  __slots__ = ["bits"] # reduce storage required for an instance

  def __init__(self,a):
    "initialize from either a long int or a dotted quad string"
    if isinstance(a,str):
      if len(a) == 4:
        self.bits = a
      else:
        self.bits = _sockinetaton(a)
    elif isinstance(a,(long,int)):
      self.bits = _structpack('!L',a)

  def __str__(self):
    "show it as dotted quad"
    return _sockinetntoa(self.bits)

  @staticmethod
  def bstr(n): # n in range 0-255
    return ''.join([str(n >> x & 1) for x in (7,6,5,4,3,2,1,0)])

  def __cmp__(self,other):
    "make comparisons work"
    return cmp(self.bits,other.bits)
  def __add__(self,n):
     a1 = _structunpack("!L",self.bits)[0]
     a1 = (a1 + 1) & 0xffffffffL
     return IPv4Addr(a1)
  def __lshift__(self,n):
     a1 = "".join([chr((ord(x)<<n)&0xff) for x in self.bits])
     return IPv4Addr(a1)
  def __rshift__(self,n):
     a1 = "".join([chr((ord(x)>>n)&0xff) for x in self.bits])
     return IPv4Addr(a1)
  def __or__(self,m):
     return IPv4Addr("".join([chr(ord(x)|ord(y)) 
                              for x,y in zip(self.bits,m.bits)]))
  def __xor__(self,m):
     return IPv4Addr("".join([chr(ord(x)^ord(y)) 
                              for x,y in zip(self.bits,m.bits)]))
  def __and__(self,m):
     return IPv4Addr("".join([chr(ord(x)&ord(y)) 
                              for x,y in zip(self.bits,m.bits)]))
  def rrot(self,n):
     a1 = _structunpack("!L",self.bits)[0]
     a1 = (a1>>(n%32))|(a1<<(32-(n%32))&0xffffffffL)
     return IPv4Addr(a1)
  def lrot(self,n):
     a1 = _structunpack("!L",self.bits)[0]<<(n%32)
     a1 = (a1&0xffffffffL)|(a1&0xffffffff00000000L)>>32
     return IPv4Addr(a1)

  def tobin(self):
    return ''.join([ ''.join((_hbits[ord(i)>>4],
                              _hbits[ord(i)&0xf])) for i in self.bits])
  def tohex(self):
    return ''.join([ ''.join((_hdigs[ord(i)>>4],
                              _hdigs[ord(i)&0xf])) for i in self.bits])
  def tolong(self):
    return long(_structunpack("!L",self.bits)[0])

  @staticmethod
  def quad2long(ip):
    "convert decimal dotted quad string to long integer"
    return _sockinetaton(ip)

  def long2quad(self):
    "convert long int to dotted quad string"
    return _sockinetntoa(self.bits)
  def octets(self):
    "return an array of integer octets"
    return [ord(o) for o in self.bits]

class IPv4Range(object):
  __slots__ = ["start","end"] # reduce storage required for an instance
  def __init__(self,s,e):
    if isinstance(s,IPv4Addr): 
      self.start = s
    else:
      self.start = IPv4Addr(s)
    if isinstance(e,IPv4Addr): 
      self.end = e
    else:
      self.end = IPv4Addr(e)
  def __str__(self):
    return self.start.long2quad() + " - " + self.end.long2quad()
  def __len__(self):
    return self.end.tolong() - self.start.tolong() + 1
  def __cmp__(self,other):
    if self.start == other.start and self.end == other.end:
      result = 0
    elif self.lessthan(other):
      result = -1
    else:
      result = 1
    return result
  def lessthan(self,other):
    if self.start == other.start and self.end == other.end:
      result = False
    elif self.start < other.start:
      result = True
    elif self.start > other.start:
      result = False
    elif self.end < other.end: # having eliminated < and > we have starts ==
      result = True
    elif self.end > other.end:
      result = False
    else:
      result = False # at this point starts and ends are equal
    return result
  def difference(self,other): 
    "subtract another range returning a list of ranges"
    if isinstance(self,IPv4Addr):
      other = IPv4Range(other.bits,other.bits) # create range of 1 addr
    if self.overlaps(other):
      if self.start == other.start:
        if self.end == other.end:
          return IPv4RangeList() # return empty list
        else:
          return IPv4RangeList([IPv4Range(other.end + 1,other.end)])
      elif self.end == other.end:
        return IPv4RangeList([IPv4Range(self.start,other.start-1)])
      elif other.start < self.start and self.end < other.end:
        return IPv4RangeList() # return empty list
      else:
        return IPv4RangeList([IPv4Range(self.start,other.start-1),
                              IPv4Range(other.end + 1,other.end)])
    else:
      return(IPv4RangeList([self])) # return list containing self

  def join(self,other):
    "combine two continuous ranges"
    if self.overlaps(other) or self.adjacent(other):
      if self.start < other.start:
        s = self.start
      elif self.start == other.start:
        s = self.start
      else:
        s = other.start

      if self.end > other.end:
        e = self.end
      elif self.end == other.end:
        e = self.end
      else:
        e = other.end
      return IPv4Range(s,e)
    else:
      raise ArithmeticError("Cannot join Ranges that are not continuous.")    

  def __contains__(self,r):
    "does self contain the argument range or address"
    if not isinstance(r,IPv4Range):
      if not isinstance(r, IPv4Addr):
        r = IPv4Addr(r)
      if r >= self.start and r <= self.end:
        return True
      else:
        return False
    if self.start <= r.start and self.end >= r.end:
      return True
    else:
      return False

  def __iter__(self): #generate a list of all addrs in range
    for a in xrange(self.start.tolong(),self.end.tolong()+1):
      yield IPv4Addr(a)
    
  def overlaps(self,r):
    "does self overlap the argument range"
    if isinstance(r,IPv4Addr):
      other = IPv4Range(r.bits,r.bits) # create range of 1 addr
    if (self.start <= r.start and self.end >= r.start) or\
       (r.start <= self.start and r.end >= self.start) or\
       (r.start <= self.start and r.end >= self.end):
      return True
    else:
      return False

  def adjacent(self,r):
    "are the two ranges adjacent"
    if self.end + 1 == r.start or r.end +1 == self.start:
      return True
    else:
      return False
  def addrs(self):
    "returns a list of all addrs in the range"
    a = []
    for x in range(_structunpack("!L",self.start.bits)[0],
                   _structunpack("!L",self.end.bits)[0]):
      a.append(IPv4Addr(x))
    a.append(self.end)
    return a
  def subtract(self,r): # may be faster to do set ops
    "returns a list of all ranges in self not overlapping r"
    if not isinstance(r,IPv4Range):
      r = IPv4Range(r,r)
    if self == r:
      return self
  # return intersections, unions, spans (smallest supernet containing both)

class IPv4Mask(object):
  __slots__ = ["bits"] # reduce storage required for an instance
  def __init__(self,m):
    if isinstance(m,str):
      if len(m) == 4:
        self.bits = m
      else:
        self.bits = _sockinetaton(m)
    elif isinstance(m,long):
      self.bits = _structpack('!L',m)
  def __str__(self):
    return self.bits.encode("hex_codec")
  def inversemask(self):
      "inverse mask as used for matching in ACLs and firewall rules"
      # this has to mask off 8 bits due to python's arbitrary length ints
      return IPv4Mask("".join([chr(~ord(m)&0xff) for m in self.bits]))

class IPv4NetMask(IPv4Mask):
  __slots__ = ["numbits","bits"] # reduce storage required for an instance
  def __init__(self,b):
    "a mask of n bits as a long integer"
    if b>=0 and b<=32:
      self.numbits = b
      self.bits = _structpack('!L',0xFFFFFFFFL - ((1L<<(32 - self.numbits))-1))
    else:
      raise ValueError,"IPv4Mask init"
  def __str__(self):
    return _sockinetntoa(self.bits)
  def nbits(self):
    return self.numbits 
  def hexmask(self):
    return self.bits.encode("hex_codec")
  def netmask(self):
    return _sockinetntoa(self.bits)
  def __len__(self):
    return 2**(32-self.numbits)

class IPv4CIDR(IPv4Range):
  __slots__ = ["start","end","mask"] # reduce storage required for an instance
  def __init__(self,s,m):
    if isinstance(m,IPv4Mask): 
      self.mask = m
    else:
      self.mask = IPv4Mask(m)
    if isinstance(s,IPv4Addr): 
      self.start = s & self.mask
    else:
      self.start = IPv4Addr(s) & self.mask
    self.end = self.start | self.mask.inversemask()
  def usable(self): 
    "return the number of usable IPs in CIDR, i.e. not incl. all 0s, all 1s"
    return self.end.tolong() - self.start.tolong() - 1
  # is_cidr? is_the_same_range?

class IPv4RangeList(list):
  def __init__(self,items=[]):
    for i in items:
      self.append(i)
    self.sort()
  def span(self): #return smallest block spanning all ranges
    e = self[-1].end
    for i in self:
      if i.end > e:
        e = i.end
    return IPv4Range(self[0].start,e) #assume list is sorted   
  def __str__(self):
    return ",".join([i.start.long2quad() + "-" +
                     i.end.long2quad() for i in self])
  def __contains__(self,other):
    r = False
    for i in self:
      if other in i:
        r = True
        break
    return r
  def append(self,r):
    if isinstance(r,IPv4Range): #don't add to end, put it where it belongs
      super(IPv4RangeList, self).insert(bisect.bisect(self,r),r)
    else:
      raise ValueError("Can only append ranges to a rangelist")
  def extend(self,x):
    if isinstance(x,IPv4RangeList): # then merge lists
      for i in x:
        super(IPv4RangeList, self).insert(bisect.bisect(self,i),i)
    elif isinstance(x,IPv4Range): #then do an append operation
      self.append(self,x)
    else:
      raise ValueError("Can only extend rangelists with range or rangelist")
  def sort(self,cmpfunc=None):
    pass # It's already sorted so this is a no-op
  def normalize(self):
    "we need to join any adjacent or overlapping ranges"
    pass # this needs to be written yet

if __name__ == "__main__":
  print "This is an import module"
