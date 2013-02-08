// A counter

package example

import Chisel._
import Node._
import scala.collection.mutable.HashMap

class Blink() extends Component {
  val io = new Bundle {
    val led = UFix(OUTPUT, 1)
  }
  val CNT_MAX = UFix(16000000-1);
  val r1 = Reg(resetVal = UFix(0, 25))
  val blk = Reg(resetVal = UFix(0, 1))
  when (r1 === CNT_MAX) {
    r1 := UFix(0)
    blk := ~blk
  }
  r1 := r1 + UFix(1)  
  io.led := blk

}

// The sbt build tool passes some arguments to our main,
// which gives some arguments for the Chisel code generation

object BlinkMain {
  def main(args: Array[String]): Unit = {
    chiselMain(args, () => new Blink());
  }
}
