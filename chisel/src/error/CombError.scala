/*
 * This code is part of the HDL comparison.
 * 
 * Copyright: 2013, Technical University of Denmark, DTU Compute
 * Author: Martin Schoeberl (martin@jopdesign.com)
 * License: Simplified BSD License
 * 
 * Shows a problem with Chisel.
 */

package error

import Chisel._
import Node._

import scala.collection.mutable.HashMap

class ErrorContainer() extends Module {
  val io = new Bundle {
    val led = Bits(OUTPUT, 8)
  }
  
  var tck = Module(new CombErr());
  
  val led = Reg(init = Bits(0, 8))
  
  when (tck.io.ticka === Bits(1) || tck.io.tickb === Bits(1)) {
    led := ~led
  }
  io.led := led
}

/**
 * Generate a 2 Hz tick to drive the FSM input test bench.
 */
class CombErr() extends Module {
  val io = new Bundle {
    val ticka = Bits(OUTPUT, 1)
    val tickb = Bits(OUTPUT, 1)
  }

  val CNT_MAX = UInt(3);
  
  val r1 = Reg(init = UInt(0, 25))
  
  val limit = r1 === CNT_MAX

  // The following is the error: both variables have the same value:
  // 0 when limit is true, 1 when false
  val ticka = when(limit) { Bits(0) } .otherwise { Bits(1) }
  val tickb = when(limit) { Bits(1) } .otherwise { Bits(0) }
  
  r1 := r1 + UInt(1)
  when (limit) {
    r1 := UInt(0)
  }
  
  // Observe the values in the VCD file
// Maybe this issue has been fixed in Chisel 2.0 as the following is not
// allowed anymore
//  io.ticka := ticka
//  io.tickb := tickb
  io.ticka := Bits(0)
  io.tickb := Bits(0)
}

class ErrorTest(ec: ErrorContainer) extends Tester(ec, Array(ec.io)) {
  defTests {
    val ret = true
    val vars = new HashMap[Node, Node]()
    val ovars = new HashMap[Node, Node]()

    for (i <- 0 until 10) {
      step(vars, ovars)
      println("iter: "+i)
      println("ovars: "+ovars)
      println(" led/litVal "+ovars(c.io.led).litValue())
    }

    ret
  }
}

object CombErrMain {
  def main(args: Array[String]): Unit = {
    chiselMainTest(args, () => Module(new ErrorContainer())) {
      f => new ErrorTest(f)
    }

  }
}
