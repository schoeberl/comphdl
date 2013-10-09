comphdl
=======

Current hardware design is dominated by two languages, VHDL and Verilog,
which are about 30 years old. They have originally not been designed for
hardware synthesis. Therefore, a lot of constructs in the languages cannot
be implemented in hardware and basic synthesizable constructs (combinational
logic, registers, and memory) are are only 'inferred' from code in a typical
style.

However, several projects build on the active development of new languages for
classic software development and adapt it for hardware description languages
(HDL). This GitHub project is about getting an overview what is out on new
tools and trying to assess the pro and cons for individual languages.

The repository currently contains currently only tiny examples in VHDL,
myHDL, and Chisel.

It also contains a minimum setup example for Chisel, as the original
getting started example from Chisel was a too complex setup. This
has changed now with a complete example in the Chisel README.md.


