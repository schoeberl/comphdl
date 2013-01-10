#
# Cheatsheet fo MyHDL
#

from myhdl import *

# a signed 32-bit variable/signal
sign32 = intbv(min=-2**31, max=2**31)
# unsigned 32-bit
unsig32 = intbv()[32:]

print(len(sign32), sign32.min, sign32.max)
print(len(unsig32), unsig32.min, unsig32.max)

# a HW component with 2 ports
def foo(clk, res):

    val = Signal(intbv(min=0, max=2))

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

# bool gets a std_logic (with additional conversions when used in expressions)
clk = Signal(bool())
# this becomes a single bit unsigned
led = Signal(intbv(min=0, max=2))
sim = Simulation(clk_driver(clk), foo(clk, led), debug(clk, led))
sim.run(10)
toVHDL(foo, clk, led)

#########
# combinational testing
def logic(inv, out1, out2, width):
    @always_comb
    def orandf():
        res = 0 # this gives an integer...
        res2 = bool(1) # this gives an integer as well...
        # res2 = intbv()[1:] # this does not work
        for i in range(width):
            res = res | inv[i]
            res2 = res2 & inv[i]
        out1.next = res 
        out2.next = res2
    return orandf

def test_comb(width):

    inv = Signal(intbv(0))
    out1 = Signal(intbv(0))
    out2 = Signal(intbv(0))

    dut = logic(inv, out1, out2, width)

    @instance
    def stimulus():
        for i in range(2**width):
            inv.next = intbv(i)
            yield(delay(10))
            print("in: "+bin(inv, width)+" out1: "+bin(out1, 1)+" out2: "+bin(out2, 1))

    return dut, stimulus

Simulation(test_comb(width=3)).run()
# now do the VHDL
inv = Signal(intbv()[3:])
out1 = Signal(bool())
out2 = Signal(bool())
toVHDL(logic, inv, out1, out2, 3)

#######
# bit slicing is a little bit unnatural
val = intbv(-7, min=-8, max=7)
x = val
print(x, len(x), x.min, x.max)
slice = val[3:0] # it goes from 2 to 0, not including 3
x = slice
print(x, len(x), x.min, x.max)
sinslice = slice.signed()
# this is not a intbv anymore...
print(sinslice)
