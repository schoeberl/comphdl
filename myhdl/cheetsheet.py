from myhdl import *

# a signed 32-bit variable/signal
sign32 = intbv(min=-2**31, max=2**31)
# unsigned 32-bit
unsig32 = intbv()[32:]

print(len(sign32), sign32.min, sign32.max)
print(len(unsig32), unsig32.min, unsig32.max)

# a HW component with 2 ports
def foo(clk, res):

    val = Signal()

    # a registered component
    @always(clk.posedge)
    def reg():
        val.next = not val;

    # a combinational component
    @always_comb
    def comb():
        res.next = val

    # return the 'local' functions for the components
    return reg, comb

# a clock for the simulation
def clk_driver(clk):

    @always(delay(1))
    def driver():
        clk.next = not clk

    return driver

# some debugging output
def debug(clk, res):
    @always(clk.posedge)
    def reg():
        print(res);
    return reg

clk = Signal()
led = Signal()
sim = Simulation(clk_driver(clk), foo(clk, led), debug(clk, led))
sim.run(10)
