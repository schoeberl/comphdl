/*
 * This code is part of the HDL comparison.
 * 
 * Copyright: 2013, Technical University of Denmark, DTU Compute
 * Author: Martin Schoeberl (martin@jopdesign.com)
 * License: Simplified BSD License
 * 
 * Blinking LED: the FPGA version of Hello World
 */

package example

import Chisel._
import Node._

import scala.collection.mutable.HashMap

class FsmContainer() extends Component {
  val io = new Bundle {
    val led = Bits(OUTPUT, 8)
    val cnt = UFix(OUTPUT, 25)    
  }
  
  var tck = new Tick();
  
  val led = Reg(resetVal = Bits(0, 8))
  
  when (tck.io.ticka === Bits(1) || tck.io.tickb === Bits(1)) {
    // led := Cat(led(6, 0), led(7))
    led := ~led
  }
  io.led := led
  io.cnt := tck.io.cnter
}

/**
 * Generate a 2 Hz tick to drive the FSM input test bench.
 */
class Tick() extends Component {
  val io = new Bundle {
    val ticka = Bits(OUTPUT, 1)
    val tickb = Bits(OUTPUT, 1)
    val cnter = UFix(OUTPUT, 25)
  }
  // BeMicro has a 16 MHz clock
  val CNT_MAX = UFix(16000000/2-1);
  
  val r1 = Reg(resetVal = UFix(0, 25))
  
  val limit = r1 === CNT_MAX
//  val ticka = limit
  
//  val ticka = when(limit) { Bits(0) } .otherwise { Bits(1) }
//  val tickb = when(limit) { Bits(1) } .otherwise { Bits(0) }
  
  val ticka = Bits(width=1)
  ticka := Bits(0)
  when (limit) { ticka := Bits(0, 1) } .otherwise{ ticka := Bits(1, 1) }
  val tickb = Bits(width=1)
  tickb := Bits(0)
  when (limit) { tickb := Bits(1, 1) } .otherwise{ tickb := Bits(0, 1) }
    
  // Do I like MUX? Probably not
  // val ticka = Mux(limit, Bits(1), Bits(0))
  // no if in Chisel
  // val ticka = if (limit) then Bits(1) else Bits(0)

  r1 := r1 + UFix(1)
  when (limit) {
    r1 := UFix(0)
  }
  
  io.ticka := ticka
  io.tickb := tickb
  
  io.cnter := r1
}

class FsmTest(fsm: FsmContainer) extends Tester(fsm, Array(fsm.io)) {
  defTests {
    val ret = true
    val vars = new HashMap[Node, Node]()
    val ovars = new HashMap[Node, Node]()

    for (i <- 0 until 10) {
      vars.clear // ?? why?
      step(vars, ovars)
      println("iter: "+i)
      println("ovars: "+ovars)
      println("cnt/litValue: "+ovars(c.io.cnt).litValue()+" led/litVal "+ovars(c.io.led).litValue())
//      println(vars(fsm.io.led))
    }

    ret
  }
}

// The sbt build tool passes some arguments to our main,
// which gives some arguments for the Chisel code generation

object FsmMain {
  def main(args: Array[String]): Unit = {
    // chiselMain(args, () => new FsmContainer());
    chiselMainTest(args, () => new FsmContainer()) {
      f => new FsmTest(f)
    }

  }
}
