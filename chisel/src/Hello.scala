// Hello World Chisel/Scala

// shouldn't the (Scala) source tree be organized in packets as in Java?

package example

import Chisel._
import Node._


class Adder(size: Int) extends Component
{
  val io = new Bundle {
    val op1 = UFix(INPUT, size)
    val op2 = UFix(INPUT, size)
    val out = UFix(OUTPUT, size)
  }

  io.out := io.op1 + io.op2

}

// The sbt build tool passes some arguments to our main,
// which gives some arguments for the Chisel code generation

object HelloMain {
  def main(args: Array[String]): Unit = { 
    chiselMain( args, () => new Adder(10));
  }
}
