This directory contains the [LEROS](https://github.com/schoeberl/leros) MyHDL implementation.

The LEROS is a small processor optimized for FPGAs and ...

LEROS Instruction Format
------------------------
@todo add the instruction format

LEROS Instructions
-------------------
*    (0_0000_xx) nop 
*    (0_0001_xx) addsub
*    (0_0010_xx) shr
*    (0_0100_xx) alu
*    (0_0101_xx) loadh
*    (0_0110_xx) store
*    (0_0111_xx) io
*    (0_1000_xx) jal
*    (0_1001_xx) branch
*    (0_1010_xx) loadaddr
*    (0_1100_xx) load indirect
*    (0_1110_xx) store indirect
