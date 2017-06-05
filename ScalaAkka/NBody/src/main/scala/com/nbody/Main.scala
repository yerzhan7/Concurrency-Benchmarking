package com.nbody

import java.io._

import akka.actor.{Actor, ActorRef, ActorSystem, Props}

import scala.collection.mutable.Queue
import scala.math._

//commandline: (1 or 0 - dumplog) (>2 - numBodies) (>1 - numSteps)

object Main extends App{
    val printSteps = 100

    var ticks: Int = 1
    var numBodies: Int = 2
    var printBool:Boolean = false 

    if(args.length>0){
        if(!argParse(args)){
            println("Usage: scala nbody <output log 0/1> <number of bodies (1 or more)> <number of steps (1 or more)>")
            System.exit(1)
        }
    }

    val starMass: Double = 10000
    val planetMass: Double = 10

    val system = ActorSystem("NBody")
    val nBodyArray = new Array[ActorRef](numBodies)
    val bodiesPos = new Array[Vector[Double]](numBodies)
    val bodiesVel = new Array[Vector[Double]](numBodies)
    val bodiesMass = new Array[Double](numBodies)


    //Generate bodies

    //'Star'
    nBodyArray(0) = system.actorOf(Props(new BodyActor
    //id , position vector, velocity vector, mass
    (0, Vector[Double](0, 0, 0), Vector[Double](0, 0, 0), starMass)),
        name = "Star")
    bodiesPos(0) = Vector[Double](0, 0, 0)
    bodiesVel(0) = Vector[Double](0, 0, 0)
    bodiesMass(0) = starMass

    //Other bodies
    for (i <- 1 until numBodies) {
        val initPosVec = Vector[Double](100 + (100 * i), 0, 0)
        val initVelVec = Vector[Double](0, sqrt(starMass / (100 + (100 * i))), 0)
        nBodyArray(i) = system.actorOf(Props(
            new BodyActor(i, initPosVec, initVelVec, planetMass)), name = "Planet" + i)
        bodiesPos(i) = initPosVec
        bodiesVel(i) = initVelVec
        bodiesMass(i) = planetMass
    }
    val worldActor = system.actorOf(Props(
        new WorldActor(numBodies, ticks, nBodyArray, bodiesPos, bodiesVel, bodiesMass)), name = "World")

    if(printBool)
    {
        val nPrintedSteps:Int = ticks/printSteps
        println(f"$numBodies $nPrintedSteps")
        for(i<-0 until numBodies) {
            val posX=bodiesPos(i)(0)
            val posY=bodiesPos(i)(1)
            val massi = bodiesMass(i)
            println(f"$posX%.1f $posY%.1f $massi%.1f")
        }
    }
    //Begin simulation
    worldActor ! Start


    case object Start
    case object Tick
    case object EulerTick

    case class UpdateState(bodiesPos: Array[Vector[Double]],
                           bodiesVel: Array[Vector[Double]])
    case class Update(positionStates: Queue[Array[Vector[Double]]],
                      velocityStates: Queue[Array[Vector[Double]]],
                      bodiesMass: Array[Double])
    case class UpdateReply(id: Int, position: Vector[Double], velocity: Vector[Double])

    case class EulerUpdate(bodiesPos: Array[Vector[Double]],
                           bodiesVel: Array[Vector[Double]],
                           bodiesMass: Array[Double])
    case class EulerReply(id: Int, position: Vector[Double], velocity: Vector[Double])

    class WorldActor(val numBodies: Int,
                     val totalTicks: Int,
                     val nBodyArray: Array[ActorRef],
                     val bodiesPos: Array[Vector[Double]],
                     val bodiesVel: Array[Vector[Double]],
                     val bodiesMass: Array[Double]) extends Actor {
        var positionStates = new Queue[Array[Vector[Double]]]
        var velocityStates = new Queue[Array[Vector[Double]]]
        var bodCounter: Int = 0
        var ticks: Int = 0
        var eulTicks: Int = 0


        def receive = {
            //This seems somewhat redundant - could just begin with a 'Tick'
            case Start => {
                self ! EulerTick
            }
            case EulerTick => {
                if (eulTicks == 0 || eulTicks == 1000 || eulTicks == 2000 || eulTicks == 3000) {
                    positionStates.enqueue(bodiesPos.clone())
                    velocityStates.enqueue(bodiesVel.clone())
                }
                if (eulTicks <3000)
                {
                    eulTicks += 1
                    for (body <- nBodyArray) {
                        body ! EulerUpdate(bodiesPos.clone(), bodiesVel.clone(), bodiesMass)
                    }
                }
                //else we have all euler initialization param and we make the system tick
                else
                {
                    self ! Tick
                }
            }

            case Tick => {
                //output current state
                //tell body actors to update current state
                if (ticks < totalTicks) {
                    ticks += 1
                    if(printBool && ticks%printSteps==0) {
                      for (i <- 0 until numBodies) {
                          val posX = bodiesPos(i)(0)
                          val posY = bodiesPos(i)(1)
                          print(f"$posX%.1f $posY%.1f ")
                      }
                    println()
                    }
                    for (body <- nBodyArray) {
                        body ! Update(positionStates, velocityStates, bodiesMass)
                    }

                } else {
                    //End simulation at specified tick count
                    context.system.terminate()
                }
            }

            case EulerReply(id, newPosition, newVelocity) => {
                bodCounter += 1
                bodiesPos(id) = newPosition
                bodiesVel(id) = newVelocity
                if (bodCounter == numBodies) {
                    bodCounter = 0
                    self ! EulerTick
                }
            }
            case UpdateReply(id, newPosition, newVelocity) => {
                bodCounter += 1
                bodiesPos(id) = newPosition
                bodiesVel(id) = newVelocity
                if (bodCounter == numBodies) {
                    bodCounter = 0
                    self ! UpdateState(bodiesPos,bodiesVel)
                }
            }
            case UpdateState(newBodiesPos, newBodiesVel) =>
            {
                positionStates.dequeue()
                velocityStates.dequeue()
                positionStates.enqueue(newBodiesPos.clone())
                velocityStates.enqueue(newBodiesVel.clone())
                self ! Tick
            }
        }
    }

    class BodyActor(val id: Int,
                    val position: Vector[Double],
                    val velocity: Vector[Double],
                    val mass: Double
                   ) extends Actor {

        var myPosition = position
        var myVelocity = velocity

        def receive = {
            case EulerUpdate(oldBodiesPos, oldBodiesVel, oldBodiesMass) => {
                myPosition = Calculate.euler_stepPos(
                    id, oldBodiesPos, oldBodiesVel(id), oldBodiesMass)
                myVelocity = Calculate.euler_stepVel(
                    id, oldBodiesPos, oldBodiesVel(id), oldBodiesMass)
                //Send new position and velocity
                sender ! EulerReply(id, myPosition, myVelocity)
            }

            case Update(positionStates, velocityStates, oldBodiesMass) => {
                val AB4results: Array[Vector[Double]] = Calculate.AB4_PosAndVec(
                    id, positionStates, velocityStates, oldBodiesMass)
                myPosition = AB4results(0)
                myVelocity= AB4results(1)
                //Send new position and velocity
                sender ! UpdateReply(id, myPosition, myVelocity)
            }

        }
    }

    //Argument parsing function
    def argParse(args: Array[String]): Boolean = {
        if(args.length != 3) {
            return false
        }
        else
        {
            if(args(0)=="1"){
                printBool = true 
            }
            else if(args(0)!="0"){
                return false
            }

            try {
                numBodies = args(1).toInt
            } catch {
                case e: Exception => return false
            }
            if(numBodies <1){
                return false
            }

            try {
                ticks = args(2).toInt
            } catch {
                case e: Exception => return false
            }
            if(args(2).toInt<1){
                return false
            }
        }
        //Arguments parsed successfully
        return true
    }
}
