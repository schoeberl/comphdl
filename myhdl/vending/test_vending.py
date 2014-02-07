
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
    """button number to button bit"""
    button = 0
    for bb in args:
        if bb > 0:
            button |= 1 << (bb-1)
    return button


def push_button(clock, buttons, bb, sec=16e-3):
    """emulate a button press"""
    if bb in (0,1,2,3,4,):
        buttons.next = button_press(bb)
    else:
        buttons.next = bb
    delayticks = int(round(sec/clock.period) * clock.pticks)
    yield delay(delayticks)
    buttons.next = 0
    yield clock.posedge


def pause(clock, sec=16e-3):
    """pause for a simulated period of seconds (sec)"""
    if sec > 0:
        delaytick = int(round(sec/clock.period) * clock.pticks)
        yield delay(delaytick)


def verify_sequence(clock, buttons, leds, valid=True):
    """generate button sequences and verify against a model
    This function (generator) will use a model to generate a
    sequence of button presses and expected codes (LEDs).    
    """
    seqtype = 'VALID' if valid else 'INVALID'
    print("++++ TEST %s SEQUENCES ++++" % (seqtype))
    # test a valid sequences
    pts,to = 0,now()
    vend = Vend(Sequence(randint(1,4), valid=valid))
    for bb,ll,ts in vend:
        # pause to match the model elapsed time
        dt,pms,pts = (ts-pts), (ts-pts)-32, ts
        # pms is in millesconds, convert to seconds
        yield pause(clock, pms/1000.)
        yield push_button(clock, buttons, bb)  # 16 wait
        yield pause(clock)                     # release button, 16 wait
        
        # if the model returns a button of zero and zero elapsed time,
        # it is the end of the the sequence.  To the dut this should look
        # like a hang (walk away).  Wait a large period of time for the
        # dut to match the model
        if bb == 0 and dt <= 0:
            yield pause(clock, 10)
            
        # print and compare
        print(" %d -> %02X (%8s, %4d) [%02x, %02x, %8s, %4d] ... %8d ms, %8d ms" % \
              (bb, ll, vend.state, vend.total,
               buttons, leds, m_vending.state, m_vending.total,
               ts, (now()-to)/(2*clock.pticks) ))
        # compare the code (led display) matches
        assert leds == ll

    if not valid:
        # wait extra long, it should sit
        yield pause(clock, .5)
        assert leds == vm.ERROR_CODE

    print("---- %s SEQUENCE SUCCESS ----" % (seqtype))


def test(args):
    """main test harness for the vending digital system"""
    # test with a slow clock, user-IO delays
    clock = Clock(0, frequency=2e3) 
    reset = Reset(0, active=True, async=False)
    buttons = Signal(intbv(0)[4:])
    leds = Signal(intbv(0)[8:])

    def _test():
        print(type(clock), clock.frequency, type(reset))
        tbdut = m_vending(clock, reset, buttons, leds)
        tbclk = clock.gen()
        
        @instance
        def tbstim():
            yield reset.pulse(clock)
            
            try:
                for _ in xrange(args.nloops):
                    # always test four sequences with random order
                    for ii in range(4):
                        valid = randint(0, 1)
                        # verify a valid sequence
                        yield verify_sequence(clock, buttons, leds,
                                              valid=bool(valid))

                        # invalid sequency ends up in error state, need
                        # to do a user reset (two buttons at once)
                        if not valid:
                            yield push_button(clock, buttons, 0x0C)
                            yield pause(clock, 32)
                            assert leds == 0

                    maxwait = 5
                    while leds != vm.WAIT_CODE and maxwait > 0:
                        yield pause(clock, 10)
                        maxwait -= 1
                    yield clock.posedge
                    assert maxwait > 0

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


    # remove previous VCD file, this prevents numerous backups
    if os.path.isfile('_test.vcd'):
        os.remove('_test.vcd')

    # the above test will test semi-random sequences,
    # valid and invalid seqeuences
    g = traceSignals(_test) if args.trace else _test()
    Simulation(g).run()

    # need the actual clock frequency for conversion, use a
    # clock of 50MHz, example board Altera DE2
    clock = Clock(0, frequency=50e6)
    toVerilog(m_vending, clock, reset, buttons, leds)
    toVHDL(m_vending, clock, reset, buttons, leds)

# run the test
test(args=Namespace(nloops=10, trace=True))
