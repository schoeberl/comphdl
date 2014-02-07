

from __future__ import division
from __future__ import print_function

from random import randint, choice

WAIT_CODE = 0x00
ERROR_CODE = 0xFF
DISP_CODE  = 0xC3

coins = [0, 1, 5, 10, 25]
cost = [0, 20, 100, 40, 55]

class Sequence:
    """ build a sequence to extract an item from the vending machine
    """    
    def __init__(self, item, valid=True):
        assert item > 0 and item < 5
        self.item = item
        self.cost = cost[item]
        self.valid = valid
        if valid:
            total = []
            while True:
                valid_coins = [cc for cc in coins[1:]
                               if cc <= self.cost-sum(total)]
                #print(self.cost, total, valid_coins)
                total += [choice(valid_coins)]
                if sum(total) == self.cost:
                    break
        else:
            while True:
                total = [choice(coins[1:])
                         for rr in range(randint(0,103))]                
                if sum(total) != self.cost:
                    break

        self.sequence = ([0] + [item] +
                         [coins.index(cc) for cc in total])

        # generate a bunch of timestamps for the buttons
        self.seqts = []
        for seq in self.sequence:
            if self.valid:
                self.seqts += [(seq,randint(300,2700),)]
            else:
                self.seqts += [(seq,randint(300,6300),)]
                               
    def __len__(self):
        return len(self.sequence)
    
    def __iter__(self):
        return iter(self.seqts)

class Vend:
    """ model for the vending machine

    This object emulates a Vending machine transaction, that
    is it is initialized with an input sequence and will
    iterate through the states of the machine.  This models
    will always finish in "end state" or "error state", if
    the interation is restarted the machine will be back at
    the "wait" state.

    The machine only accepts an input 0-4, this machine does
    not emulate the multi-button press reset, rather to reset
    the Vend.reset() function is called.
    """
    def __init__(self, seq):
        self.item = seq.item  # item selection
        self.seq = iter(seq)  # input sequence
        self.cost = cost      # item cost definition
        self.coins = coins    # coin definition

        self.ts = 0     # timestamp in ms
        self.total = 0  # input coin total
        
        self.ValidStates = ['wait',      # wait for item selection
                            'coinage',   # recieve coins
                            'dispense',  # dispense item
                            'error']     # error

        self.state = 'wait'    # init state  
        self.code = WAIT_CODE  # init code

        # state handler table
        self.sm = {'wait' : self._sm_wait,
                   'dispense' : self._sm_dispense,
                   'coinage' : self._sm_coinage,
                   'error' : self._sm_error,
                   'end': self._sm_end
                   }


    def __iter__(self):
        return self

    def next(self):
        """ The state-machine
        """
        try:
            button,elapse = self.seq.next()
            assert button < 5
        except StopIteration:
            button,elapse = 0,0

        # execute the state
        next_state = self.sm[self.state](button, elapse)
        self.ts += elapse
        
        # determine when to stop
        if self.state == 'end' or self.state == 'error':
            raise StopIteration 

        self.state = next_state
        return button, self.code, self.ts

    def reset(self):
        self.state = 'wait'
        self.code = WAIT_CODE
        
    def _sm_wait(self, button, elapse):
        next_state = self.state
        if button > 0 and button < 5:
            self.code = 0x02 << button
            self.item = button 
            next_state = 'coinage'
            self.total = 0

        return next_state
    
    def _sm_coinage(self, button, elapse):
        next_state = self.state        
        self.total += coins[button]
        icost = cost[self.item]
        
        if elapse > 4000 or button == 0 or self.total > icost:
            self.code = ERROR_CODE
            next_state = 'error'
            
        elif self.total == cost[self.item]:
            next_state = 'dispense'
            self.code = DISP_CODE
            self.nblnk = 0
            
        return next_state
    
    def _sm_dispense(self, button, elapse):
        next_state = self.state
        assert elapse == 0
        self.ts += 500
        self.nblnk += 1

        if self.nblnk % 2 == 1:
            self.code = 0x02 << self.item
        else:
            self.code = DISP_CODE
            
        if self.nblnk == 6:
            self.code = 0
            next_state = 'end'

        return next_state
    
    def _sm_error(self, button, elapse):
        self.code = ERROR_CODE
        return 'error'

    def _sm_end(self, button, elapse):
        self.code = 0
        return 'wait'
