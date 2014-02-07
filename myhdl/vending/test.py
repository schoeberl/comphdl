
from __future__ import division
from __future__ import print_function

import os
from argparse import Namespace
from random import randint, choice

from myhdl import *

import vending_models as vm
from vending_models import Sequence, Vend
from vending import m_vending

# small wrappers around clock and reset, simplifies
# testbench and pamaeter passing
from _clock import Clock
from _reset import Reset
        
def button_press(*args):
    button = 0
    for bb in args:
        if bb > 0:
            button |= 1 << (bb-1)
    return button

def push_button(clock, buttons, bb):
    if bb in (0,1,2,3,4,):
        buttons.next = button_press(bb)
    else:
        buttons.next = bb
    delayms = int(round(16e-3/clock.period))
    yield delay(delayms*clock.pticks)
    buttons.next = 0
    yield clock.posedge

def pause(clock, ms=16e-3):
    delayms = int(round(ms/clock.period))
    yield delay(delayms*clock.pticks)

def test(args):
    # test with a slow clock, user-IO delays
    clock = Clock(0, frequency=2e3) #Signal(bool(0))
    reset = Reset(0, active=True, async=False)
    buttons = Signal(intbv(0)[4:])
    leds = Signal(intbv(0)[8:])

    if os.path.isfile('_test.vcd'):
        os.remove('_test.vcd')

    def _test():
        print(type(clock), clock.frequency, type(reset))
        tbdut = m_vending(clock, reset, buttons, leds)
        tbclk = clock.gen()
        
        @instance
        def tbstim():
            yield reset.pulse(clock)
            
            try:
                print("++++ TEST VALID SEQUENCES ++++")
                # test a bunch of valid sequences
                pts,to = 0,now()
                for ii in xrange(args.nloops):
                    vend = Vend(Sequence(randint(1,4), valid=True))
                    for bb,ll,ts in vend:
                        # pause to match the model elapsed time
                        pms,pts = (ts-pts)-32,ts                                                
                        yield pause(clock, pms/1000.)
                        yield push_button(clock, buttons, bb)
                        yield pause(clock) # release button
                        # print and compare
                        print(" %d -> %02X (%8s, %4d) [%02x, %02x, %8s, %4d] ... %8d ms, %8d ms" % \
                              (bb, ll, vend.state, vend.total,
                               buttons, leds, m_vending.state, m_vending.total,
                               ts, (now()-to)/(2*clock.pticks) ))
                        # compare the code (led display) matches
                        assert leds == ll                              
                print("     VALID SEQUENCE SUCCESS")
            
                while leds != vm.WAIT_CODE:
                    yield delay(1000)
                yield clock.posedge
                
                print("++++ TEST INVALID SEQUENCES ++++")
                # test a bunch of invalid sequences
                pts,to = 0,now()
                for ii in xrange(args.nloops):
                    vend = Vend(Sequence(randint(1,4), valid=False))
                    for bb,ll,ts in vend:
                        pms,pts = (ts-pts)-32,ts                                                
                        yield pause(clock, pms/1000.)
                        yield push_button(clock, buttons, bb)
                        yield pause(clock) # release button
                        print(" %d -> %02X (%8s, %4d) [%02x, %02x, %8s, %4d] ... %8d ms, %8d ms" % \
                              (bb, ll, vend.state, vend.total,
                               buttons, leds, m_vending.state, m_vending.total,
                               ts, (now()-to)/(2*clock.pticks) ))
                        assert leds == ll

                    # wait extra long, it should sit
                    yield pause(clock, .5)
                    assert leds == vm.ERROR_CODE
                    print("     INVALID SEQUENCE SUCCESS")
                    
                    # reset, back to wait
                    yield push_button(clock, buttons, 0x0C)
                    yield pause(clock, 32)
                    assert leds == 0
                    
            except AssertionError, err:
                print("**** ERROR (%s) ****" % (err))                
                for _ in range(11):
                    yield clock.posedge
                    print(" %d -> %02X (%8s, %4d) [%02x, %02x, %s, %d] ... %8d ms" % \
                          (bb, ll, vend.state, vend.total,
                           buttons, leds, m_vending.state, m_vending.total,
                           ts))                    
                raise err


            raise StopSimulation

        return tbdut, tbclk, tbstim

    Simulation(traceSignals(_test)).run()
    toVerilog(m_vending, clock, reset, buttons, leds)
    toVHDL(m_vending, clock, reset, buttons, leds)

# run the test
test(args=Namespace(nloops=1))
