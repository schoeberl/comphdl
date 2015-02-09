/*
 * This code is part of the HDL comparison.
 * 
 * Copyright: 2013, Technical University of Denmark, DTU Compute
 * Author: Martin Schoeberl (martin@jopdesign.com)
 * License: Simplified BSD License
 * 
 * A simple finite state machine (FSM) with logic to drive as test bench. 
 */

package example

import Chisel._
import Node._

class FsmContainer() extends Module {
  val io = new Bundle {
    val led = Bits(OUTPUT, 8)
  }
  
  var tck = Module(new Tick())
  
  val led = Reg(init = Bits(1, 8))
  val led_next = Cat(led(6, 0), led(7))
  
  when (tck.io.tick === Bits(1)) {
    led := led_next
  }
  io.led := ~led
}

/**
 * Generate a 2 Hz tick to drive the FSM input test bench.
 */
class Tick() extends Module {
  val io = new Bundle {
    val tick = Bits(OUTPUT, 1)
  }
  // BeMicro has a 16 MHz clock
  val CNT_MAX = UInt(16000000/2-1)
  
  val r1 = Reg(init = UInt(0, 25))
  
  val limit = r1 === CNT_MAX
  val tick = limit
  
  r1 := r1 + UInt(1)
  when (limit) {
    r1 := UInt(0)
  }
  
  io.tick := tick

  // **** uninteresting stuff below ****
  
// the following does not work - example in package error
//  val ticka = when(limit) { Bits(0) } .otherwise { Bits(1) }
//  val tickb = when(limit) { Bits(1) } .otherwise { Bits(0) }
  
// this is a very verbose version
//  val ticka = Bits(width=1)
//  ticka := Bits(0)
//  when (limit) { ticka := Bits(0, 1) } .otherwise{ ticka := Bits(1, 1) }
//  val tickb = Bits(width=1)
//  tickb := Bits(0)
//  when (limit) { tickb := Bits(1, 1) } .otherwise{ tickb := Bits(0, 1) }
    
  // That's the MUX version. Do we know which is which? True first? 0 first? 
  // val ticka = Mux(limit, Bits(1), Bits(0))
  
  // no if in Chisel
  // val ticka = if (limit) then Bits(1) else Bits(0)

}

class FsmTest(fsm: FsmContainer) extends Tester(fsm) {
  val ret = true

  for (i <- 0 until 10) {
    step(1)
    println("iter: "+i)
//    println("led/litVal "+peek(c.io.led).litValue())
    println("led/litVal "+peek(c.io.led))
  }
}

object FsmMain {
  def main(args: Array[String]): Unit = {
    // chiselMain(args, () => Module(new FsmContainer()));
    // Looks like the MainTest is also fine for Verilog code generation
    chiselMainTest(args, () => Module(new FsmContainer())) {
      f => new FsmTest(f)
    }

  }
}
