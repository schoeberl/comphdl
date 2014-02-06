BSC=bsc
BSCFLAGS=-verilog

compFsmTest: PrioritySetReset.bo CompFSM.bo TestFSM.bo
	$(BSC) $(BSCFLAGS) -e mkTestFSM -o $@

%.bo: %.bsv
	$(BSC) $(BSCFLAGS) $<

mkCompFSM.v: CompFSM.bsv
	$(BSC) $(BSCFLAGS) $<

.PHONY: clean

clean:
	rm -rf mk*.v *.bo *~
	rm -rf compFsmTest *.log *.cmd *.xmsgs *.wdb *.tcl *.isim isim # ISim files