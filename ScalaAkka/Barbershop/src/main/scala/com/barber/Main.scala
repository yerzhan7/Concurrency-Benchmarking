package com.barber

import java.util.Random
import java.util.concurrent.atomic.AtomicLong
import akka.actor.{Actor, ActorRef, ActorSystem, Props}

import scala.collection.mutable.ArrayBuffer

object Main extends App {
    //Arguments
    var print: Boolean = false   //Print logs
    var haircuts = 500          //Total haircuts
    var capacity = 100          //Waiting room size
    var apr = 100               //Average customer production rate
    var ahr = 100               //Average haircut rate

    //Parse args
    if (args.length > 0) {
        if (!argParse(args)) {
            println("Usage: ./barbershop [output log 0/1] [total haircuts >0] [waiting room size >0] [avg customer production rate >0] [average haircut rate >0]")
            System.exit(1)
        }
    }

    val idGenerator = new AtomicLong(0)
    //Create actors
    val system = ActorSystem("Barbershop")
    val barber = system.actorOf(Props(new BarberActor(ahr)), "Barber")
    val shop = system.actorOf(Props(new ShopActor(capacity, barber)), "Shop")
    val factory = system.actorOf(Props(new FactoryActor(haircuts, shop, idGenerator, apr)), "Factory")

    factory ! Start



    case object Start   //Begin benchmark
    case object Exit    //Benchmark finished, terminate actors
    case object Full    //Waiting room is full
    case object Next    //Send next customer to barber
    case object Wait    //Tell customer/barber to wait
    case object Begin   //Start haircut
    case object End     //Finish haircut
    case object Done    //Customer finished, leaving system

    case class Enter(customer: ActorRef)                    //Customer enters shop
    case class Haircut(customer: ActorRef, shop: ActorRef)  //Customer sits in barber chair
    case class Returned(customer: ActorRef)                 //Waiting room full, customer returns to factory

    trait BusyWait {
        def busyWait(limit: Int): Unit = {
            var j = 0
            var i = 0
            while (i < limit) {
                i += 1
                j += 1
            }
        }
    }

    class BarberActor(val ahr: Int) extends Actor with BusyWait {
        val random = new Random()

        def receive = {
            case Haircut(customer, shop) => {
                customer ! Begin
                busyWait(random.nextInt(ahr) + 10)
                customer ! End
                shop ! Next
            }
            case Wait => {
                if (print) {
                    println("Barber: No customers in waiting room. Going to have a sleep.")
                }
            }
            case Exit => {
                context.stop(self)
            }
        }
    }

    class ShopActor(val capacity: Int,
                    val barber: ActorRef) extends Actor {
        val waiting = new ArrayBuffer[ActorRef]()
        //Could alternately use 'ListBuffer'
        var barberAsleep = true

        def receive = {
            case Enter(customer) => {
                if (waiting.size == capacity) {
                    customer ! Full
                } else {
                    waiting.append(customer)
                    if (barberAsleep) {
                        barberAsleep = false
                        self ! Next
                    } else {
                        customer ! Wait
                    }
                }
            }
            case Next => {
                if (waiting.size > 0) {
                    val customer = waiting.remove(0)
                    barber ! Haircut(customer, self)
                } else {
                    barber ! Wait
                    barberAsleep = true
                }
            }
            case Exit => {
                barber ! Exit
                context.stop(self)
            }
        }
    }

    class FactoryActor(val haircuts: Int,
                       val shop: ActorRef,
                       val idGenerator: AtomicLong,
                       val apr: Int) extends Actor with BusyWait {
        var completedHaircuts = 0
        val random = new Random()

        def receive = {
            case Start => {
                var i = 0
                while (i < haircuts) {
                    sendCustomerToRoom()
                    busyWait(random.nextInt(apr) + 10)
                    i += 1
                }
            }
            case Returned(customer) => {
                idGenerator.incrementAndGet()
                sendCustomerToRoom(customer)
            }
            case Done => {
                completedHaircuts += 1
                if (completedHaircuts == haircuts) {
                    if(print) {
                        println("Total attempts: " + idGenerator.get())
                    }
                    shop ! Exit
                    context.system.terminate()
                }
            }
        }

        def sendCustomerToRoom(): Unit = {
            val id = idGenerator.incrementAndGet()
            val customer = context.system.actorOf(Props(new CustomerActor(id, self)), "Customer-" + id)
            sendCustomerToRoom(customer)
        }

        def sendCustomerToRoom(customer: ActorRef) {
            shop ! Enter(customer)
        }
    }

    class CustomerActor(val id: Long,
                        val factory: ActorRef) extends Actor {
        def receive = {
            case Full => {
                if(print) {
                    println("Customer " + id + ": The waiting room is full. I am leaving.")
                }
                factory ! Returned(self)
            }
            case Wait => {
                if(print) {
                    println("Customer " + id + ": Barber is busy. I will wait in the waiting room.")
                }
            }
            case Begin => {
                if (print) {
                    println("Customer " + id + ": I am now being served.")
                }
            }
            case End => {
                if(print) {
                    println("Customer " + id + ": I have been served.")
                }
                factory ! Done
                context.stop(self)
            }
        }
    }

    def argParse(args: Array[String]): Boolean = {
        if (args.length != 5) {
            return false
        }

        //Print logs
        if (args(0) == "1") {
            print = true
        } else if (args(0) != "0") {
            return false
        }

        //Total haircuts
        try {
            haircuts = args(1).toInt
        } catch {
            case e: Exception => return false
        }
        if (haircuts < 1) {
            return false
        }

        //Waiting room size
        try {
            capacity = args(2).toInt
        } catch {
            case e: Exception => return false
        }
        if (capacity < 1) {
            return false
        }

        //Avg customer production rate
        try {
            apr = args(3).toInt
        } catch {
            case e: Exception => return false
        }
        if (apr < 1) {
            return false
        }

        //Avg haircut rate
        try {
            ahr = args(4).toInt
        } catch {
            case e: Exception => return false
        }
        if (ahr < 1) {
            return false
        }

        //Successfully parsed
        return true
    }
}
