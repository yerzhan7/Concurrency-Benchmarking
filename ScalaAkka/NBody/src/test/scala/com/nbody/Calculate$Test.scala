package com.nbody

import org.scalatest.FunSuite
import Calculate._

import scala.collection.mutable.Queue
import scala.math.BigDecimal
class Calculate$Test extends FunSuite {
  def round(a: Vector[Double]): Vector[Double] = {
    Vector[Double](
      BigDecimal(a(0)).setScale(5, BigDecimal.RoundingMode.HALF_UP).toDouble,
      BigDecimal(a(1)).setScale(5, BigDecimal.RoundingMode.HALF_UP).toDouble,
      BigDecimal(a(2)).setScale(5, BigDecimal.RoundingMode.HALF_UP).toDouble)
  }

  test("DT should equal 0.01") {
    assert(DT == 0.01)
  }
  test("eulerSteps should equal 1000.0") {
    assert(eulerSteps == 1000.0)
  }
  test("eulerDT should equal 0.01/1000.0") {
    assert(eulerDT == 0.01/1000.0)
  }
  test("gravity constant should equal 1.0") {
    assert(GR == 1.0)
  }
  test("AB1 constant should equal 0.375") {
    assert(
      BigDecimal(AB1).setScale(5, BigDecimal.RoundingMode.HALF_UP).toDouble
        == -0.375)
  }
  test("AB2 constant should equal 1.54167 at 5dp") {
    assert(
      BigDecimal(AB2).setScale(5, BigDecimal.RoundingMode.HALF_UP).toDouble
        == 1.54167)
  }
  test("AB3 constant should equal -2.45833 at 5dp") {
    assert(
      BigDecimal(AB3).setScale(5, BigDecimal.RoundingMode.HALF_UP).toDouble
        == -2.45833)
  }
  test("AB4 constant should equal 2.29167 at 5dp") {
    assert(
      BigDecimal(AB4).setScale(5, BigDecimal.RoundingMode.HALF_UP).toDouble
        == 2.29167)
  }
  /*
  .     Set(x,y,z,ux,uy,uz,mass)
  body1.Set(0,0,0,0,0,0,1)
  body2.Set(1,0,0,0,0,0,1)
  body3.Set(0,1,1,234,302,234,10) */
  test("force between two bodies") {
    val pos1 = Vector[Double](0, 0, 0)
    val pos2 = Vector[Double](1, 0, 0)
    val pos3 = Vector[Double](0, 1, 1)
    val masses123 = Array[Double](1, 1, 10)

    assert(force2B(pos1, pos2, masses123(0), masses123(1)) == Vector[Double](1, 0, 0))
    val ansVec1: Vector[Double] = force2B(pos1, pos3, masses123(0), masses123(2))
    val ans1 = round(ansVec1)
    assert(ans1 == round(Vector[Double](0, 3.53553, 3.53553)))

    val ansVec2: Vector[Double] = force2B(pos3, pos1, masses123(0), masses123(2))
    val ans2 = round(ansVec2)
    assert(ans2 == round(Vector[Double](0, -3.53553, -3.53553)))
  }
  test("force from all other bodies") {
    val posA = new Array[Vector[Double]](3)
    posA(0) = Vector[Double](0, 0, 0)
    posA(1) = Vector[Double](0, -1, -1)
    posA(2) = Vector[Double](0, 1, 1)
    val masses123 = Array[Double](1, 10, 10)
    assert(round(totalForce(0, posA, masses123)) == round(Vector[Double](0, 0, 0)))
    assert(round(totalForce(1, posA, masses123)) == round(Vector[Double](0,12.374369,12.374369)))
    assert(round(totalForce(2, posA, masses123)) == round(Vector[Double](0,-12.374369,-12.374369)))
  }
  test("euler_steps(EulerDT) for both position and velocity") {
    val posA = new Array[Vector[Double]](3)
    posA(0) = Vector[Double](0, 0, 0)
    posA(1) = Vector[Double](0, -1, -1)
    posA(2) = Vector[Double](0, 1, 1)
    val velA = new Array[Vector[Double]](3)
    velA(0) = Vector[Double](0, 0, 0)
    velA(1) = Vector[Double](0, 0, 0)
    velA(2) = Vector[Double](100, 100, 100)
    val masses123 = Array[Double](1,10,10)
    assert(round(euler_stepPos(0, posA, velA(0), masses123)) == round(Vector[Double](0, 0, 0)))
    assert(round(euler_stepVel(0, posA, velA(0), masses123)) == round(Vector[Double](0,0,0)))
    assert(round(euler_stepPos(1, posA, velA(1), masses123)) == round(Vector[Double](0, -1, -1)))
    assert(round(euler_stepVel(1, posA, velA(1), masses123)) == round(Vector[Double](0.0, 1.0E-5, 1.0E-5)))
    assert(round(euler_stepPos(2, posA, velA(2), masses123)) == round(Vector[Double](0.001, 1.001, 1.001)))
    assert(round(euler_stepVel(2, posA, velA(2), masses123)) == round(Vector[Double](100.0, 99.99999, 99.99999)))

  }
  test("euler_steps for both position and velocity") {
    /*
    body_array[0].Set(0,0,0,0,0,0,1)
    body_array[1].Set(0,-1,-1,0,0,0,10)
    body_array[2].Set(0,1,1,100,100,100,10) // random floats for velocity
    */
    val posA = new Array[Vector[Double]](3)
    posA(0) = Vector[Double](0, 0, 0)
    posA(1) = Vector[Double](0, -1, -1)
    posA(2) = Vector[Double](0, 1, 1)
    val velA = new Array[Vector[Double]](3)
    velA(0) = Vector[Double](0, 0, 0)
    velA(1) = Vector[Double](0, 0, 0)
    velA(2) = Vector[Double](100, 100, 100)
    val masses123 = Array[Double](1,10,10)
    assert(round(euler_stepPos(0, posA, velA(0), masses123,0.01)) == round(Vector[Double](0, 0, 0)))
    assert(round(euler_stepVel(0, posA, velA(0), masses123,0.01)) == round(Vector[Double](0,0,0)))
    assert(round(euler_stepPos(1, posA, velA(1), masses123,0.01)) == round(Vector[Double](0, -1, -1)))
    assert(round(euler_stepVel(1, posA, velA(1), masses123,0.01)) == round(Vector[Double](0,0.012374,0.012374)))
    assert(round(euler_stepPos(2, posA, velA(2), masses123,0.01)) == round(Vector[Double](1, 2, 2)))
    assert(round(euler_stepVel(2, posA, velA(2), masses123,0.01)) == round(Vector[Double](100,99.987626,99.987626)))
  }
  test("AB4_stepy") {
    var positionStates = new Queue[Array[Vector[Double]]]
    var velocityStates = new Queue[Array[Vector[Double]]]

    val posA = new Array[Vector[Double]](3)
    posA(0) = Vector[Double](0, 0, 0)
    posA(1) = Vector[Double](0, -1, -1)
    posA(2) = Vector[Double](0, 1, 1)

    val velA = new Array[Vector[Double]](3)
    velA(0) = Vector[Double](0, 0, 0)
    velA(1) = Vector[Double](0, 0, 0)
    velA(2) = Vector[Double](100, 100, 100)

    val masses123 = Array[Double](1,10,10)

    positionStates.enqueue(posA.clone())
    velocityStates.enqueue(velA.clone())
    val step:Double = 0.01
    for(i<-1 to 3) {
      val posAfixed = posA.clone()
      val velAfixed = velA.clone()
      posA(0)=euler_stepPos(0,posAfixed,velAfixed(0),masses123,step)
      posA(1)=euler_stepPos(1,posAfixed,velAfixed(1),masses123,step)
      posA(2)=euler_stepPos(2,posAfixed,velAfixed(2),masses123,step)
      velA(0)=euler_stepVel(0,posAfixed,velAfixed(0),masses123,step)
      velA(1)=euler_stepVel(1,posAfixed,velAfixed(1),masses123,step)
      velA(2)=euler_stepVel(2,posAfixed,velAfixed(2),masses123,step)
      positionStates.enqueue(posA.clone())
      velocityStates.enqueue(velA.clone())
    }
    //body 0 position
    assert(round(AB4_PosAndVec(0,positionStates,velocityStates,masses123)(0))==round(Vector[Double](7.528551069814374E-5, -9.766972872791184E-4, -9.766972872791184E-4)))
    //body 0 velocity
    assert(round(AB4_PosAndVec(0,positionStates,velocityStates,masses123)(1))==round(Vector[Double](0.009203512690456854, -0.10132972210407891, -0.10132972210407891)))

    //body 1 position
    assert(round(AB4_PosAndVec(1,positionStates,velocityStates,masses123)(0))==round(Vector[Double](3.128473074515985E-5, -0.9993992306380816, -0.9993992306380816)))
    //body 1 velocity
    assert(round(AB4_PosAndVec(1,positionStates,velocityStates,masses123)(1))==round(Vector[Double](0.0032361046404008483, 0.02870963183016327, 0.02870963183016327)))
  }
}
