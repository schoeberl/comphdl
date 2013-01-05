#
# Copyright: 2013, Technical University of Denmark, DTU Compute
# Author: Martin Schoeberl (martin@jopdesign.com)
# License: Simplified BSD License
#

# Hardware Hello World

from myhdl import *

def blink(clk, led):

  CLK_FREQU = 16000000
  BLINK_FREQU = 1
  CNT_MAX = int(CLK_FREQU/BLINK_FREQU/2-1)
  
  cnt = Signal(intbv(0, min=0, max=CNT_MAX+1))
  blk = Signal(False)

  @always(clk.posedge)
  def hdl():
    if cnt == CNT_MAX:
      cnt.next = 0
      blk.next = not blk
    else:
      cnt.next = cnt+1

  @always_comb
  def comb():
    led.next = blk

  return hdl, comb

def ClkDriver(clk):

	interval = delay(1)
	@always(interval)
	def driveClk():
		clk.next = not clk

	return driveClk

clk = Signal(False)
led = Signal(False)
clk_driver = ClkDriver(clk)
inst = blink(clk, led)
sim = Simulation(clk_driver, inst)
sim.run(100)
toVHDL(blink, clk, led)