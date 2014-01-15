package TestFSM;

import CompFSM::*;
import StmtFSM::*;

(* synthesize *)
module mkTestFSM(Empty);
    // DUT
    IfcCompFSM testFSM <- mkCompFSM();
    
    // Write the actual tester as a FSM...
    Stmt driver = seq
		      testFSM.start();
		      delay(400); // Wait for the end...
		  endseq;
    
    mkAutoFSM(driver);
endmodule

endpackage