package com.nbody

import org.scalatest.FunSuite
import VectorMethods._

/**
  * Created by jpl216 on 06/03/17.
  */
class VectorMethods$Test extends FunSuite {

  test("magnitude of 0 0 0 3d vector should be 0") {
    val m = Vector[Double](0,0,0).Magnitude
    assert(m==0)
  }
  test("1 1 1 3d vector - 1 1 1 3d vector should be 0 0 0") {
    val m = Vector[Double](1,1,1)-Vector[Double](1,1,1)
    assert(m==Vector[Double](0,0,0))
  }
  test("0 0 0 3d vector + 1 1 1 3d vector should be 1 1 1") {
    val m = Vector[Double](0,0,0)+Vector[Double](1,1,1)
    assert(m==Vector[Double](1,1,1))
  }
  test("calling (1,1,1) 3d vector to VecMltpC(2) should give a (2,2,2) vector"){
    val m = Vector[Double](1,1,1).VecMltpC(2)
    assert(m==Vector[Double](2,2,2))
  }

}
