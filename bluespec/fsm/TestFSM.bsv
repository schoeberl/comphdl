package TestFSM;

import CompFSM::*;
import StmtFSM::*;
import Vector::*;

(* synthesize *)
module mkTestFSM(Empty);
    // DUT
    Vector#(4, Price) prices = replicate(0);
    Vector#(4, Price) coins = replicate(0);

    prices[0] = 20;
    prices[1] = 100;
    prices[2] = 40;
    prices[3] = 55;

    coins[0] = 1;
    coins[1] = 5;
    coins[2] = 10;
    coins[3] = 25;

    IfcCompFSM#(4) testFSM <- mkCompFSM(prices, coins);
    Reg#(Bit#(8)) oldLeds <- mkReg(~0);

    rule printLeds;
        Bit#(8) newLeds = testFSM.getLeds();
        if(newLeds != oldLeds) begin
            $display("LEDS: %b", newLeds);
            oldLeds <= newLeds;
        end
    endrule

    // Write the actual tester as a FSM...
    Stmt driver = seq
            $display("======================================");
            $display("         COMPHDL VENDING TEST         ");
            $display("======================================");

            $display("DRV: Resetting machine");
            testFSM.putButtons(~0);

            // Wait for the machine to reset
            delay(50);

            $display("DRV: Selecting item 1");
            testFSM.putButtons('h1);


            $display("DRV: Adding coinage");
            testFSM.putButtons('h2);
            testFSM.putButtons('h4);
            testFSM.putButtons('h1);
            testFSM.putButtons('h1);
            testFSM.putButtons('h1);
            testFSM.putButtons('h1);
            testFSM.putButtons('h1);
		    delay(500000); // Wait for the end...
		  endseq;
    
    mkAutoFSM(driver);
endmodule

endpackage