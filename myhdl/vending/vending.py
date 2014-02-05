
from myhdl import *

def m_vending(clock, reset, buttons, leds):

    @always_seq(clock.posedge, reset=reset)
    def rtl():
        leds.next = 0x00
        
    return rtl
