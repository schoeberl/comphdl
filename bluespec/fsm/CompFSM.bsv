// Simple vending machine example (I'll rename the packages later...).
// See /myhdl/vending/problem_statement.md for full spec.
// We currently make the assumption that the number of selections is equal
// to the number of coin types.

package CompFSM;

export IfcCompFSM(..);
export mkCompFSM;
export Price;

import StmtFSM::*;
import Vector::*;
import PrioritySetReset::*;
import FIFOF::*;

// Tie costs to 8 bits for now. That should be enough...
typedef UInt#(8) Price;

// NOTE: Change the below to reflect your actual environment
`define TIMEOUT_CYCLES 200  // 4 seconds?
`define FLASH_CYCLES 25     // 0.5 seconds?

// Because it'd be boring without making the interface generic ;)
// I'd make it fully generic, but there's actually no point making it for anything
// non-Bits...
interface IfcCompFSM#(numeric type btnBits);
    method Action putButtons(Bit#(btnBits) btns);

    // Strip any external signals from this. The LEDs shouldn't have any
    // implicit conditions, and it's not an action
    (* always_ready *)
    method Bit#(TAdd#(2, TAdd#(btnBits, 2))) getLeds();
endinterface

// Since this has provisos and interface arguments that cannot be expressed in Verilog, we
// cannot synthesize this module.
module mkCompFSM#(Vector#(btnBits, Price) costs, Vector#(btnBits, Price) coins) (IfcCompFSM#(btnBits))
    provisos(Log#(btnBits, btnBitsl2),                // Get the number of bits to express a number in Bit#(btnBits)
             Alias#(Bit#(btnBits), buttons),          // Save typing...
             Add#(2, TAdd#(2, btnBits), ledBits),      // To show that ledBits is btnBits extended twice
             Add#(1, a__, TLog#(TAdd#(1, btnBits))),          // Req. by compiler for the countOnes. Effectively states btnBits cannot be zero. I think.
             Add#(b__, btnBitsl2, TLog#(TAdd#(1, btnBits)))   // Req. by compiler for the truncate.
    );

    // We need to do priority set/reset on this var. Assume the case where a button is pressed
    // just as we reset the pressed_buttons bitfield.
    //IfcPrioritySR#(Maybe#(buttons)) pressed_buttons <- mkPrioritySR(tagged Invalid);

    // Scratch that...just use a FIFO.
    // I mean, you don't want to lose money ;)
    // The code for the PrioritySR version is still there, but commented out.
    FIFOF#(buttons) pressed_buttons <- mkSizedFIFOF(8);
    Reg#(Bit#(ledBits)) leds <- mkReg(0);

    // State machine "variables"
    Reg#(Bit#(btnBits))    selectedItemBits <- mkReg(0);
    UInt#(btnBitsl2)       selectedItem = truncate(countZerosLSB(selectedItemBits)); // Permanent bit -> index resolver\
    Reg#(Price)            currentCoins <- mkReg(0);
    Reg#(UInt#(10))        timeoutCounter <- mkReg(0);

    // Helper vars
    Bit#(2) led_pad0 = 0;
    Bit#(2) led_pad1 = ~0;

    // Helper functions
    function Stmt awaitCoinOrTimeout();
        return seq
            timeoutCounter <= 0;
            $display("Starting timeout run...");
            while(!pressed_buttons.notEmpty()) par
                if(timeoutCounter == `TIMEOUT_CYCLES) seq
                    action
                        // Timed out, flash LEDs and block
                        $display("COIN TIMEOUT, ABORTING");
                        leds <= ~0;                                 // Light up the error state
                    endaction

                    while(True) seq
                        delay(1);
                    endseq 
                endseq
                else action
                    timeoutCounter <= timeoutCounter + 1;
                endaction
            endpar
        endseq;
    endfunction

    // =======================================
    // The actual state machine
    // =======================================
    Stmt worker = seq
                while(True) seq
                    $display("Machine awaiting buttons");
                    // Wait for a button press...
                    //await(isValid(pressed_buttons)); // Don't need this now, it's an implicit condition of the next rule

                    action
                        //buttons x = fromMaybe(0, pressed_buttons);
                        buttons x = pressed_buttons.first();
                        pressed_buttons.deq();
                        selectedItemBits <= x;

                        UInt#(btnBitsl2) itm = truncate(countZerosLSB(x));
                        //selectedItem <= itm;
                        leds <= {led_pad0,x,led_pad0};
                        $display("Requested item %d, price %d", itm, costs[itm]);

                        //pressed_buttons.reset();
                    endaction

                    while(currentCoins < costs[selectedItem]) seq
                        // Await button press
                        awaitCoinOrTimeout();

                        // Figure out what was put in
                        action
                            //buttons x = fromMaybe(0, pressed_buttons);
                            buttons x = pressed_buttons.first();
                            pressed_buttons.deq();
                            UInt#(btnBitsl2) coin = truncate(countZerosLSB(x));

                            $display("Inserted coin %d, value %d. Total value %d", coin, coins[coin], currentCoins + coins[coin]);
                            currentCoins <= currentCoins + coins[coin];

                            //pressed_buttons.reset();
                        endaction
                    endseq

                    // We now have enough money, vend!
                    repeat(3) seq
                        $display("VEND");
                        leds <= {led_pad1, 0, led_pad1};
                        delay(`FLASH_CYCLES);
                        leds <= {led_pad0, selectedItemBits, led_pad0};
                        delay(`FLASH_CYCLES);
                    endseq

                    // Reset.
                    action
                        $display("RESETTING");
                        leds <= {led_pad0, 0, led_pad0};
                        currentCoins <= 0;
                        selectedItemBits <= 0;
                    endaction
                endseq
            endseq;
    FSM workerFsm <- mkFSM(worker);
    
    // ======================================
    // State machine to reset the machine.
    // This seems...overkill...
    // ======================================
    Stmt resetter = seq
        $display("+=+= RESETTING MACHINE =+=+");
        workerFsm.abort();
        workerFsm.start();
    endseq;
    FSM resetterFsm <- mkFSM(resetter);
    
    // External interface stuff
    method Action putButtons(buttons btns);
        // We need to use pack() here to convert it into a Bits#(x) type that countOnes expects.
        $display("Pressed buttons %b", btns);

        if(countOnes(btns) > 1)   // Can always reset if more than one button is pressed.
            resetterFsm.start();
        else if(countOnes(btns) != 0) // Make sure something was actually pressed...
            pressed_buttons.enq(btns);
            //pressed_buttons <= tagged Valid btns;
    endmethod

    method Bit#(ledBits) getLeds();
        return leds;
    endmethod
endmodule

endpackage