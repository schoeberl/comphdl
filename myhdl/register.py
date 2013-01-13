
#
# How to model a register wirh a reset
#
from myhdl import *

def clk_driver(clk):
    interval = delay(1)
    @always(interval)
    def driveClk():
        clk.next = not clk
    return driveClk

def foo(clk, reset, sig):

    # it is very strange to have reset as edge sensiteve,
    # but MyHDL generatess the 'correct' ansynchronous reset
    # in VHDL
    @always(clk.posedge, reset.posedge)
    def hdl():
        if reset == 1:
            sig.next = 0
        else:
            sig.next = not sig

    return hdl

clk = Signal(bool())
reset = Signal(bool())
sig = Signal(bool())
clkdr = clk_driver(clk)
inst = foo(clk, reset, sig)
sim = Simulation(clkdr, inst)
sim.run(10)
toVHDL(foo, clk, reset, sig)

