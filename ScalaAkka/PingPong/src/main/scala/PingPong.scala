import akka.actor.{Actor, ActorRef, ActorSystem, Props}
case class Start(sender: ActorRef)
case class Ping(num: Int)
case class Pong(num: Int)

object PingPongTest extends App {
    var printBool: Boolean = false
    var cycles: Int = 1 //default (will be overwritten by argParse)
    if (args.length > 0) {
        if (!argParse(args)) {
          println("Usage: scala pingpong <output log 0/1> <number of cycles > 1>")
            System.exit(1) //terminate programme with invalid input params
        }
    }
    val system = ActorSystem("PingPongSystem")
    val pong = system.actorOf(Props(new Pong(cycles,printBool)), name = "pong")
    val ping = system.actorOf(Props(new Ping(cycles,printBool)), name = "ping")
    // start them going
    ping ! Start(pong)

    def argParse(args: Array[String]): Boolean = {
        if (args.length != 2) {
            return false
        }
        else {
            if (args(0) == "1") {
                printBool = true
            }
            else if (args(0) != "0") {
                return false
            }

            try {
                cycles = args(1).toInt
            } catch {
                case e: Exception => return false
            }
            if (cycles < 1) {
                return false
            }
        } //Arguments parsed successfully
        return true
    }

    class Ping(cycles: Int,printBool:Boolean) extends Actor {
        def receive = {
            case Start(thesender: ActorRef) =>
                val num:Int = 1
                    if(printBool){
                        println("Ping " + num)
                    }
                    thesender ! Pong(1)
            case Ping(num: Int) =>
                if (num <= cycles) {
                    if(printBool){
                        println("Ping " + num)
                    }
                    sender ! Pong(num)
                }
                else {
                    context.system.terminate()
                }
        }
    }

    class Pong(cycles: Int,printBool:Boolean) extends Actor {
        def receive = {
            case Pong(num: Int) =>
                if (num<= cycles) {
                    if(printBool) {
                        println("Pong " + num)
                    }
                    sender ! Ping((num+1))
                }
        }
    }
}

