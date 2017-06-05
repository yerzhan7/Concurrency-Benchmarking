package com.nbody

import VectorMethods._
import scala.collection.mutable.Queue

object Calculate {
    def DT:Double = 0.01 //steps for AB method
    def eulerSteps:Double = 1000.0 //micro-steps for Euler method
    def eulerDT: Double = DT/eulerSteps
    def GR:Double = 1.0 //gravity constant
    def AB1: Double = -3.0 / 8
    def AB2: Double = 37.0 / 24
    def AB3: Double = -59.0 / 24
    def AB4: Double = 55.0 / 24



    def AB4_PosAndVec(id: Int, positions: Queue[Array[Vector[Double]]], velocities: Queue[Array[Vector[Double]]],
                      masses: Array[Double]): Array[Vector[Double]] = {

        val u1: Vector[Double] = velocities(0)(id)
        val u2: Vector[Double] = velocities(1)(id)
        val u3: Vector[Double] = velocities(2)(id)
        val u4: Vector[Double] = velocities(3)(id)

        val u1234: Vector[Double] = u1.VecMltpC(AB1) + u2.VecMltpC(AB2) + u3.VecMltpC(AB3) + u4.VecMltpC(AB4)


        val pos1: Array[Vector[Double]] = positions(0)
        val pos2: Array[Vector[Double]] = positions(1)
        val pos3: Array[Vector[Double]] = positions(2)
        val pos4: Array[Vector[Double]] = positions(3)

        val f1234: Vector[Double] =
            totalForce(id, pos1, masses).VecMltpC(AB1) +
              totalForce(id, pos2, masses).VecMltpC(AB2) +
              totalForce(id, pos3, masses).VecMltpC(AB3) +
              totalForce(id, pos4, masses).VecMltpC(AB4)


        val ans = new Array[Vector[Double]](2)
        //position saved in ans(0)
        ans(0) = pos4(id) + u1234.VecMltpC(DT)
        //velocity saved in ans (1)
        ans(1) = u4 + f1234.VecMltpC(DT/masses(id))

        ans
    }


    def euler_stepPos(id: Int, positions: Array[Vector[Double]], velocity: Vector[Double],
                      masses: Array[Double], step:Double = eulerDT): Vector[Double] = {
        positions(id) + velocity.VecMltpC(step)
    }


    def euler_stepVel(id: Int, positions: Array[Vector[Double]], velocity: Vector[Double],
                      masses: Array[Double],step:Double = eulerDT): Vector[Double] = {
        velocity + totalForce(id, positions, masses).VecMltpC(step/masses(id))
    }


    def dist(pos1:Vector[Double], //Euclidean Distance Function
             pos2: Vector[Double]):Double = {
        (pos1-pos2).Magnitude
    }


    def newtonGF(x: Double):Double = { //Newton Gravity Force
        -1/(x*x)
    }


    def force2B(pos1:Vector[Double], pos2: Vector[Double], //Force bet 2 bodies
                mass1: Double, mass2: Double):Vector[Double] = {
        (pos1-pos2).VecMltpC(
            (mass1*mass2*newtonGF(dist(pos1,pos2))*GR)/dist(pos1,pos2))
    }


    def totalForce(id: Int, positions: Array[Vector[Double]], //Total Force from all bodies
                   masses: Array[Double]): Vector[Double] = {
        var sum = Vector[Double](0,0,0)
        for(i<-0 until positions.size){
            if(i != id){
                sum = sum + force2B(positions(id), positions(i), masses(id), masses(i))
            }
        }
        sum
    }
}
