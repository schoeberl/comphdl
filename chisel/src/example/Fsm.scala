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
  }
  
  var tck = new Tick();
  
  val led = Reg(resetVal = Bits(0, 8))
  
  when (tck.tick === Bits(1)) {
    // led := Cat(led(6, 0), led(7))
    led := ~led
  }
  io.led := led
}

/**
 * Generate a 2 Hz tick to drive the FSM input test bench.
 */
class Tick() extends Component {
  val io = new Bundle {
    val tick = Bits(OUTPUT, 1)
  }
  // BeMicro has a 16 MHz clock
  val CNT_MAX = UFix(3) // UFix(16000000/2-1);
  
  val r1 = Reg(resetVal = UFix(0, 25))
  
  val limit = r1 === CNT_MAX
  val tick = Mux(limit, Bits(0), Bits(1))

  r1 := r1 + UFix(1)
  when (limit) {
    r1 := UFix(0)
  }
  
  
  io.tick := tick
}

class FsmTest(fsm: FsmContainer) extends Tester(fsm, Array(fsm.io)) {
  defTests {
    val ret = true
    val vars = new HashMap[Node, Node]()

    for (i <- 0 until 5) {
      step(vars, isTrace = false)
      println(fsm.io.led)
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
