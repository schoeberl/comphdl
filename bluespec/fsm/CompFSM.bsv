package CompFSM;

export IfcCompFSM(..);
export mkCompFSM;

import StmtFSM::*;

interface IfcCompFSM;
    method Action start();
endinterface

(* synthesize *)
module mkCompFSM(IfcCompFSM);
    Stmt worker = seq
		      $display("Hello");
		      $display("World");
		  endseq;
    
    FSM workerFsm <- mkFSM(worker);
    
    // Called from outside to start the FSM.
    method Action start();
	workerFsm.start();
    endmethod
endmodule

endpackage