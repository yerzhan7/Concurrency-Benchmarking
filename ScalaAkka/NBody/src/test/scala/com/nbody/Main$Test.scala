package com.nbody
import Main._
import akka.actor.{Actor, ActorRef, ActorSystem, Props}
import akka.testkit.{ImplicitSender, TestActors, TestKit}
import org.scalatest.{BeforeAndAfterAll, FunSuite, FunSuiteLike, Matchers}

import scala.collection.mutable.Queue
class Main$Test extends TestKit(ActorSystem("MySpec"))
    with ImplicitSender
    with FunSuiteLike with Matchers with BeforeAndAfterAll {
    override def afterAll {
        TestKit.shutdownActorSystem(system)
    }

    val tooManyArgs = Array("1", "5", "5", "5")
    test("argParse rejects too many args") {
        assert(!argParse(tooManyArgs))
    }
    val args = Array("a", "10", "10")
    test("argParse first argument") {
        assert(!argParse(args))
        args(0) = "-1"
        assert(!argParse(args))
        args(0) = "1"
        assert(argParse(args))
    }
    test("argParse second argument") {
        args(1) = "a"
        assert(!argParse(args))
        args(1) = "1"
        assert(!argParse(args))
    }
    test("argParse third argument") {
        args(2) = "a"
        assert(!argParse(args))
        args(2) = "0"
        assert(!argParse(args))
    }
    test("argParse correctly updates variables") {
        args(0) = "0"
        args(1) = "5"
        args(2) = "6"
        argParse(args)
        assert(!Main.printBool)
        assert(Main.numBodies == 5)
        assert(Main.ticks == 6)
    }


    test("Euler Update and Reply") {
        val body1: ActorRef = system.actorOf(Props(new BodyActor
        (0, Vector[Double](0, 0, 0), Vector[Double](0, 0, 0), 10)),
            name = "TestBody1Euler")
        val bodiesPos = new Array[Vector[Double]](1)
        val bodiesVel = new Array[Vector[Double]](1)
        val bodiesMass = new Array[Double](1)

        bodiesPos(0) = Vector[Double](0, 0, 0)
        bodiesVel(0) = Vector[Double](0, 0, 0)
        bodiesMass(0) = 10
        body1 ! EulerUpdate(bodiesPos, bodiesVel, bodiesMass)
        expectMsg(EulerReply(0, Vector(0.0, 0.0, 0.0), Vector(0.0, 0.0, 0.0)))
    }
    test("AB4 Update and Reply") {
        val body1: ActorRef = system.actorOf(Props(new BodyActor
        (0, Vector[Double](0, 0, 0), Vector[Double](0, 0, 0), 10)),
            name = "TestBody1AB4")
        val bodiesPos = new Array[Vector[Double]](1)
        val bodiesVel = new Array[Vector[Double]](1)
        val bodiesMass = new Array[Double](1)

        bodiesPos(0) = Vector[Double](0, 0, 0)
        bodiesVel(0) = Vector[Double](0, 0, 0)
        bodiesMass(0) = 10
        var positionStates = new Queue[Array[Vector[Double]]]
        var velocityStates = new Queue[Array[Vector[Double]]]
        for (i <- 1 to 4) {
            positionStates.enqueue(bodiesPos.clone())
            velocityStates.enqueue(bodiesVel.clone())
        }
        body1 ! Update(positionStates, velocityStates, bodiesMass)
        expectMsg(UpdateReply(0, Vector(0.0, 0.0, 0.0), Vector(0.0, 0.0, 0.0)))
    }

    test("World Test") {
        val body1: ActorRef = system.actorOf(Props(new BodyActor
        (0, Vector[Double](0, 0, 0), Vector[Double](0, 0, 0), 10)),
            name = "TestBody1World")
        val body2: ActorRef = system.actorOf(Props(new BodyActor
        (1, Vector[Double](1, 1, 1), Vector[Double](0, 0, 0), 10)),
            name = "TestBody2World")
        //Arrays
        val bodiesPos = new Array[Vector[Double]](2)
        val bodiesVel = new Array[Vector[Double]](2)
        val bodiesMass = new Array[Double](2)

        bodiesPos(0) = Vector[Double](0, 0, 0)
        bodiesVel(0) = Vector[Double](0, 0, 0)
        bodiesPos(1) = Vector[Double](1, 1, 1)
        bodiesVel(1) = Vector[Double](0, 0, 0)
        bodiesMass(0) = 10
        bodiesMass(1) = 10

        val numBodies = 2
        val nBodyArray = new Array[ActorRef](numBodies)

        nBodyArray(0) = body1
        nBodyArray(1) = body2
        val ticks = 1
        val worldActor = system.actorOf(Props(
            new WorldActor(numBodies, ticks, nBodyArray, bodiesPos, bodiesVel, bodiesMass)), name = "World")
        worldActor ! Start
        expectNoMsg
    }
}
