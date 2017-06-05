package com.nbody

import scala.math._

// 3-dimensional vectors ONLY
object VectorMethods {

  implicit class VectorImprovements(val v: Vector[Double]) {
    def Magnitude: Double = abs(sqrt(
      (v(0) * v(0)) + (v(1) * v(1)) + (v(2) * v(2))))

    def -(that: Vector[Double]): Vector[Double] =
      Vector[Double](
        v(0) - that(0),
        v(1) - that(1),
        v(2) - that(2))

    def +(that: Vector[Double]): Vector[Double] =
      Vector[Double](
        v(0) + that(0),
        v(1) + that(1),
        v(2) + that(2))

    def VecMltpC(c: Double): Vector[Double] = {
      Vector[Double](
        v(0)*c,
        v(1)*c,
        v(2)*c)
    }
  }
}

