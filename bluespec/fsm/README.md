Vending Machine Bluespec Example
================================

This is an example of a vending machine as outlined in /myhdl/vending/problem_statement.md. It implements
said vending machine in Bluespec System Verilog. Rather than hardcoding all prices and coin values, they
are passed as parameters to the module. Equally, the number of coin/vending inputs is parameterisable using
the interface parameter. If any are not used, they should be tied off to zero.

Because of restrictions with the FSM used and the reset logic, starting the machine should be done by sending
the normal reset sequence to the machine first before any other transactions.

In addition, a FIFO is used to buffer inputs. This used to be a simple register instead (hence the large amount of
commented code), but this requires explicit delays, or predicating putButtons on "no outstanding buttons". Since a
FIFO used to be in use, this is why `awaitCoinOrTimeout` is an external function, which could now be rolled into the 
main logic for receiving a coin now to eliminate the extra cycle of delay.

Finally, since a FIFO is now used, `putButtons` will now be predicated on the FIFO having available space (due to
Bluespec's implicit conditions) and thus export a RDY_ signal in the generated Verilog. If this is undesirable, 
the FIFO can be changed to a GFIFO with the enqueue guard disabled. If a plain Verilog file is required, CompFSM
will have to be instantiated from another module with the interface arguments tied off to known values. This is because
the Bluespec compiler cannot generate Verilog from a source file with interface arguments.