
VENDING MACHINE EXAMPLE
=======================
This directory contains the MyHDL implementation of simple 
vending machine described in 
(problem_descriptions.md)[https://github.com/schoeberl/comphdl/blob/master/myhdl/vending/problem_statement.md].
The simple vending machine is an academic problem but is 
defined such that it can be run on an FPGA development 
board and the functionality verified.  The state-machine
needs to deal with user interaction time.

Testing the Design
------------------
The implementation has an extensive test - to run the 
tests and convert to Verilog and VHDL:

    >> python test_vending.py

The test uses a **model** to generate correct sequences
(item selection and coin insertion).  The test will output
sequences:

    ++++ TEST VALID SEQUENCES ++++
     0 -> 00 (    wait,    0) [00, 00,     WAIT,    0] ...      866 ms,      866 ms
     1 -> 04 ( coinage,    0) [00, 04,  COINAGE,    0] ...     1224 ms,     1224 ms
     3 -> 04 ( coinage,   10) [00, 04,  COINAGE,   10] ...     3922 ms,     3922 ms
     2 -> 04 ( coinage,   15) [00, 04,  COINAGE,   15] ...     4483 ms,     4483 ms
     2 -> C3 (dispense,   20) [00, c3, DISPENSE,   20] ...     5531 ms,     5531 ms
     0 -> 04 (dispense,   20) [00, 04, DISPENSE,   20] ...     6031 ms,     6031 ms
     0 -> C3 (dispense,   20) [00, c3, DISPENSE,   20] ...     6531 ms,     6531 ms
     0 -> 04 (dispense,   20) [00, 04, DISPENSE,   20] ...     7031 ms,     7031 ms
     0 -> C3 (dispense,   20) [00, c3, DISPENSE,   20] ...     7531 ms,     7531 ms
     0 -> 04 (dispense,   20) [00, 04, DISPENSE,   20] ...     8031 ms,     8031 ms
     0 -> 00 (     end,   20) [00, 00,     WAIT,    0] ...     8531 ms,     8531 ms
     |    |       |       |     |    |     |       |             |            |
     |    |       |       |     |    |     |       |             |            +----- simulation time
     |    |       | 	  |     |    |	   |	   |     	 +------------------ model elapsed time
     |	  |	  |	  |     |    |	   |	   +-------------------------------- DUT total coin recieved
     |	  |	  |	  |     |    |	   +---------------------------------------- DUT state
     |	  |	  |	  |     |    +---------------------------------------------- DUT code (LED value)
     |    |       |       |     +--------------------------------------------------- DUT button input
     |    |       |       +--------------------------------------------------------- model total coin received
     |    |       +----------------------------------------------------------------- model state
     |    +------------------------------------------------------------------------- model code (LED value)
     +------------------------------------------------------------------------------ model button input 


The test will walk through valid and invalid sequences
and verify the correct LED output given a particular 
button sequence input.

Currently, the default is to run 10 test loops, each 
test loop consists of four sequences.  This takes a 
little time to run, the tests can be sped up by running
(pypy)[https://www.pypy.org].

    >> python test_vending.py
    average time 3 minutes and 47 seconds

    >> pypy test_vending.py
    average time 52 seconds

[//] Verilog(s) Testing
[//] FPGA Results