package main

import "fmt"
import "os"
import "strconv"
import "math/rand"
import "sync"
import "runtime"

//Globals
var logging bool = false//Print output
var haircuts int = 500  //Default number of haircuts
var capacity int = 100  //Default waiting room capacity
var apr int = 100       //Default average customer production rate
var ahr int = 100       //Default average haircut rate

//Communication consts
const FULL int = 0
const WAIT int = 1
const BEGIN int = 2
const NEXT int = 3
const EXIT int = 4

func main() {
    
    runtime.GOMAXPROCS(1024)//Max number of Cores
    
    //Parse args
    if(len(os.Args) != 1){
        if(!argParse(os.Args[1:])){
            fmt.Println("Usage: ./barbershop [output log 0/1] [total haircuts >0] [waiting room size >0] [avg customer production rate >0] [average haircut rate >0]")
        return
        }
    }

    //Setup system
    var wg = new(sync.WaitGroup)
    wg.Add(1)
    var factory Factory
    var shop Shop
    var barber Barber

    ch_barber := barber.start(ahr)
    ch_shop := shop.start(capacity, ch_barber)
    //Start
    ch_factory := factory.start(haircuts, apr, ch_shop, wg)

    if logging{
        fmt.Println("Total attempts:", <-ch_factory)
    }
    wg.Wait()
}

func argParse(args []string) bool{
    if(len(args) != 5){
        return false
    }
    //Print logs
    if(args[0] == "1"){
        logging = true
    } else if (args[0] != "0") {
        return false
    }

    var err error
    haircuts, err = strconv.Atoi(args[1])
    capacity, err = strconv.Atoi(args[2])
    apr, err = strconv.Atoi(args[3])
    ahr, err = strconv.Atoi(args[4])

    if (err != nil){
        return false
    }
    if (haircuts < 1 || capacity < 1 || apr < 1 || ahr < 1){
        return false
    }

    return true
}

func busyWait(limit int) int{
    //Generate random number up to 'limit' (with extra bits to stop compiler optimisation?)
    k := rand.Intn(limit) + 10
    j := 0
    for i := 0; i < k; i++ {
        j++
    }
    return j
}
