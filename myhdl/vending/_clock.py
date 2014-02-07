from math import floor
import myhdl
from myhdl import instance, delay

class Clock(myhdl.SignalType):
    
    def __init__(self, val, frequency=1.):
        self.frequency = frequency
        self.period = 1./frequency
        self.pticks = 6
        myhdl.SignalType.__init__(self, bool(val))
        
    def gen(self):
        """ generate a clock """
        @instance
        def gclock():
            self.next = False
            while True:
                yield delay(3)               
                self.next = not self.val
                
        return gclock
                                
    def timescale(self):
        """ get the timescale given the clock freq
        six simulation steps is equal to one clock cycle, each
        simulation step is clock_period/6.
        """
        tstep = int(round(((self.period)/6.) * 1e12))
        ts = "%d ps"%(tstep)
        print(ts)
        return ts
