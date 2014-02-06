// This package provides a mechanism for a dual ported variable, with
// either write capability, or reset capability. The write capability
// shadows the reset capability.
// Reset resets the value of this to resetVal, as specified in the parameters.
// Aside from the reset, this works exactly like a standard Reg#(data).
package PrioritySetReset;

export IfcPrioritySR(..);
export mkPrioritySR;

interface IfcPrioritySR#(type data);
    method data _read();
    method Action _write(data a);
    method Action reset();
endinterface

module mkPrioritySR#(data resetVal) (IfcPrioritySR#(data))
    provisos(Bits#(data, data_sz)); // Make sure we can actually represent it...
    
    RWire#(data) setWire   <- mkRWire();
    PulseWire    resetWire <- mkPulseWire();
    Reg#(data)   dataReg   <- mkReg(resetVal);
    
    rule updateReg(isValid(setWire.wget) || resetWire);
	if(isValid(setWire.wget))
	    dataReg <= fromMaybe(unpack(0), setWire.wget());
	else // Reset *must* be asserted
	    dataReg <= resetVal;
    endrule
    
    method data _read();
	return dataReg;
    endmethod
    
    method Action _write(data x);
	setWire.wset(x);
    endmethod
    
    method Action reset();
	resetWire.send();
    endmethod
endmodule
endpackage