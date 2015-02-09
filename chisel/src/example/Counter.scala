// A counter

package example

import Chisel._
import Node._

class Counter(size: Int) extends Module {
  val io = new Bundle {
    val out = UInt(OUTPUT, size)
  }
  val r1 = Reg(init = UInt(0, size))
  r1 := r1 + UInt(1)
  io.out := r1

}

class CounterTest(c: Counter) extends Tester(c) {
  val ret = true

  for (i <- 0 until 5) {
    step(1)
    println(i)
    println(peek(c.io.out))
  }

}
// The sbt build tool passes some arguments to our main,
// which gives some arguments for the Chisel code generation

object CounterMain {
  def main(args: Array[String]): Unit = {
    //    chiselMain(args, () => Module(new Counter(10)));
    chiselMainTest(args, () => Module(new Counter(4))) {
      c => new CounterTest(c)
    }
  }
}
