
from math import log, ceil
from myhdl import *

# the maximum time to wait between key presses
MAX_MS_WAIT = 4000
# the button debounce time
DEBOUNCE_MS = 4

# static defines
C_WAIT_CODE = 0x00
C_ERROR_CODE = 0xFF
C_DISP_CODE = 0xC3

def m_vending(
    # ~~~[PORTS]~~~
    clock, reset, button, led,
    
    # ~~~[PARAMETERS]~~~
    coins=[0, 1, 5, 10, 25], 
    costs=[0, 20, 100, 40, 55]    
    ):
    """
    """
    # Compute some constants/parameers
    TicksPerMs = int(clock.frequency / 1000)
    MaxTick = MAX_MS_WAIT * TicksPerMs
    DebounceMs = DEBOUNCE_MS
    
    # define the states for this machine
    States = enum('WAIT', 'RELEASE', 'COINAGE', 'DISPENSE', 'ERROR', 'END')

    state = Signal(States.WAIT)
    user_reset = Signal(bool(0))
    
    # the modbv needs to be a power of two, could simply
    # define the number of bits but then it loses some
    # some real-world defintion/information
    tmax = int(ceil(log(MaxTick*2, 2)))
    ticks = Signal(modbv(0, min=0, max=2**tmax))
    
    # the following two are used to debounce the button
    _button = Signal(button.val)  # copy of the button type
    bbounce = Signal(button.val)  # copy of the button type
    
    # state-machine variables
    # store the button to update the LEDs with the
    # item selected (bit version) store the int (1,2,3,4)
    # of item to select the correct coin
    imax = 8 if len(costs) < 8 else len(costs)
    itemi = Signal(intbv(0, min=0, max=imax)) # int version
    itemb = intbv(0, min=0, max=button.max)   # bit version
    total = intbv(0, min=0, max=max(costs)+10)
    
    # use non-mutable container (ROM)
    coins = tuple(coins)
    costs = tuple(costs)
    
    # use the following to convert a bit to (0,1,2,4) to
    # the int (1,2,3,4).  The -1 is used mainly for verification
    # these values should not be used.
    bits2int = [-1 for _ in range(2**len(button))]
    bits2int[1:9] = 1, 2, -1, 3, -1, -1, -1, 4
    bits2int = tuple(bits2int)

    # convert button to item (easy to look-up)
    bitem = Signal(intbv(0, min=0, max=9))
    @always_comb
    def rtl_bits2int():
        if bbounce > 0 and bbounce < 9:
            bitem.next = bits2int[bbounce]
        else:
            bitem.next = 0

    # using look-up tables for the coins and costs
    # need to pull them out here ????
    ccoin = Signal(intbv(0, min=0, max=max(coins)+1))
    ccost = Signal(intbv(0, min=0, max=max(costs)+1))
    @always_comb
    def rtl_coin():
        ccoin.next = coins[bitem]
        if state == States.COINAGE:
            ccost.next = costs[itemi]

    # ~~~[STATE MACHINE]~~~
    @always_seq(clock.posedge, reset=reset)
    def rtl_sm():
        # running counter for timeouts etc
        ticks.next = ticks + 1

        # ~~~~[State Machine Core]~~~~
        # detect reset then the states
        if user_reset:
            state.next = States.END            
        
        elif state == States.WAIT:
            total[:] = 0
            if bbounce > 0 and bbounce < 9:
                itemb[:] = button
                itemi.next = bitem
                ticks.next = 0
                state.next = States.RELEASE
                led.next = itemb << 2
                
        elif state == States.RELEASE:
            if bbounce == 0:
                state.next = States.COINAGE
                
        elif state == States.COINAGE:
            if ticks >= MaxTick or total > ccost:
                state.next = States.ERROR
                led.next = C_ERROR_CODE
            elif bbounce > 0 and bbounce < 9:
                total[:] = total + ccoin #coins[bitem]
                if total == ccost: #costs[itemi]:
                    state.next = States.DISPENSE
                    ticks.next = 0
                    # reuse itemi to the number of blinks
                    itemi.next = 1
                    led.next = C_DISP_CODE
                else:
                    state.next = States.RELEASE
                    ticks.next = 0
                    
        elif state == States.DISPENSE:
            if ticks > 500*TicksPerMs:
                ticks.next = 0
                itemi.next = itemi+1
                if (itemi % 2) == 1:
                    led.next = itemb << 2
                else:
                    led.next = C_DISP_CODE
                if itemi == 6:
                    state.next = States.END
                
        elif state == States.END:
            state.next = States.WAIT
            led.next = 0

        elif state == States.ERROR:
            led.next = C_ERROR_CODE

        else:
            assert False, "Invalid state %s" % (state)


    # simple debounce, button(s) constant for 4ms
    # then will pass the button    
    @always_seq(clock.posedge, reset=reset)
    def rtl_debounce():
        if (ticks % (TicksPerMs*DebounceMs)) == 0:
            _button.next = button
            if button == _button:
                bbounce.next = button
                
        
    @always_comb
    def rtl_user_reset():
        bcnt = 0
        for ii in range(len(bbounce)):
            if bbounce[ii]:
                bcnt += 1
                
        if bcnt > 1:
            user_reset.next = True
        else:
            user_reset.next = False


    # DEBUG STUFF
    m_vending.state = state
    m_vending.total = total
    # END DEBUG STUFF
        
    return rtl_bits2int, rtl_coin, rtl_sm, rtl_debounce, rtl_user_reset
