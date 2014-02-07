
import myhdl

class Reset(myhdl.ResetSignal):

    def __init__(self, val, active, async):

        myhdl.ResetSignal.__init__(self, val, active, async)

    def pulse(self, clock=None):
        self.next = self.active
        yield myhdl.delay(100)
        self.next = not self.active
        if clock is not None:
            yield clock.posedge

