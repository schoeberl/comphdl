
from __future__ import division
from __future__ import print_function

import os
from argparse import Namespace
from random import randint, choice

from myhdl import *
import vending_models as vm
from vending_models import Sequence, Vend
from vending import m_vending
        
def button_press(*args):
    button = 0
    for bb in args:
        if bb > 0:
            button |= 1 << (bb-1)
    return button

def test(args):
    clock = Signal(bool(0))
    reset = ResetSignal(0, active=True, async=False)
    buttons = Signal(intbv(0)[4:])
    leds = Signal(intbv(0)[8:])

    if os.path.isfile('_test.vcd'):
        os.remove('_test.vcd')

    def _test():
        tbdut = m_vending(clock, reset, buttons, leds)

        @always(delay(3))
        def tbclk():
            clock.next = not clock

        @instance
        def tbstim():
            reset.next = reset.active
            yield delay(10)
            reset.next = not reset.active
            yield clock.posedge

            print("++++ VALID SEQUENCES ++++")
            # test a bunch of valid sequences
            for ii in xrange(args.nloops):
                vend = Vend(Sequence(randint(1,4), valid=True))
                for bb,ll,ts in vend:
                    buttons.next = button_press(bb)
                    yield clock.posedge
                    print(" %d -> %02X (%8s, %4d) [%02x, %02x] ... %8d ms" % \
                          (bb,ll, vend.state, vend.total, buttons, leds, ts))
                    #assert led == ll
                # @todo: assert success flash

            while leds != vm.WAIT_CODE:
                yield delay(1000)
            yield clock.posedge

            print("++++ INVALID SEQUENCES ++++")
            # test a bunch of invalid sequences
            for ii in xrange(args.nloops):
                vend = Vend(Sequence(randint(1,4), valid=False))
                for bb,ll,ts in vend:                    
                    buttons.next = button_press(bb)
                    yield clock.posedge
                    print(" %d -> %02X (%8s, %4d) [%02x, %02x] ... %8d ms" % \
                          (bb,ll, vend.state, vend.total, buttons, leds, ts))
                    
                # @todo: might need to wait for the error code, there is
                #        a 4 second timeout 
                #assert leds == vm.ERROR_CODE

                # reset
                buttons.next = 0x03
                yield clock.posedge
                buttons.next = 0x00

            raise StopSimulation

        return tbdut, tbclk, tbstim

    Simulation(traceSignals(_test)).run()

# run the test
test(args=Namespace(nloops=1))
