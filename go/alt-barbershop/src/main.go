package main

import (
    "os"
    "fmt"
    "math/rand"
    "strconv"
)

//Globals
var (
    logging = false //Print output
    haircuts = 500  //Default number of haircuts
    capacity = 100  //Default waiting room capacity
    apr = 100       //Default average customer production rate
    ahr = 100       //Default average haircut rate
)

func main() {
    //Parse args
    if(len(os.Args) != 1){
        if(!argParse(os.Args[1:])){
            fmt.Println("Usage: ./barbershop [output log 0/1] [total haircuts >0] [waiting room size >0] [avgerage customer production rate >0] [average haircut rate >0]")
        return
        }
    }

    var report = make(chan int)
    var shop = make(chan chan int, capacity)
    go barber(shop)
    go factory(shop, report)

    var total = <-report
    fmt.Println("Total customers generated =", total)
}

func barber(shop chan chan int) {
    for ch, ok := <-shop; ok; ch, ok = <-shop {
        ch <- 0     //Start haircut
        busyWait(ahr)
        ch <- 0     //Finish
    }
}

func customer(id int, shop chan chan int, returns chan int) {
    ch := make(chan int)
    select {
    //Try to enter shop
    case shop <- ch:
        <-ch
        //Start
        <-ch
        //End
        returns <- 0  //Inform factory of completion
    //Shop is full
    default:
    }
}

func factory(shop chan chan int, report chan int){
    var id = 0
    var completed = 0
    var returns = make(chan int)

    for {
        select {
        //Customer has returned
        case <-returns:
            completed++
            //If required number of haircuts completed, tell main
            if(completed == haircuts){
                report <- id
                return
            }
        //Create new customer
        default:
            busyWait(apr)
            go customer(id, shop, returns)
            id++
        }
    }
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
        j = rand.Intn(limit)
    }
    return j
}
