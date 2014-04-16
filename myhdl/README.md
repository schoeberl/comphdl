Introduction
============
This directory contains the MyHDL implementation for 
the examples in the comphdl effort.  Currently, this
includes a:

1.  *vending machine* 
2.  *leros* processor
3.  *???*

The directory is organized as:
   
    <example>/
              myhdl/           # python source lives here
              test_verilogs/   # test the generated verilogs
              
It is very important that the examles are working examples,
some focus on verification.  The *test_verilogs* will be able
to verify each of the generated Verilog from each language. 
This is similar to the examples in [alt.hdl](https://github.com/cfelton/alt.hdl).

MyHDL Cheetsheet
=================
The following are some notes/hints for basic MyHDL 
topics.

types
-----
The base type in MyHDL is an *intbv*.  This is a range
limited integer that can be bit accessed.

```python
# signed 32-bit value
>>> sint32 = intbv(0, min=-2**31, max=2**31)
>>> uint32 = intbv(0, min=0, max=2**32)
# or
>>> uint32 = intbv(0)[32:]

>>> print(len(sint32), sint32.min, sint32.max)
(32, -2147483648, 2147483648)
>>> print(len(uint32), uint32.min, uint32.max)
(32, 0, 4294967296)
```

The MyHDL preferred way is not to think about a bit
width but rather the range of number required for a 
task.  Example, if a counter is needed that counts 
from 0 to 312 (because you have upto 312 things to
count) then an *intbv* can be defined

```python
>>> counter = intbv(0, min=0, max=313)
>>> print(len(counter), counter.min, counter.max)
(9, 0, 313)
```

Notice that Python uses exlcusive on the max range
and inclusive on the min range, this is the format
adopted by the Python community.

