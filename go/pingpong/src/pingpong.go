package main

import (
    "flag"
    "strconv"
    "fmt"
    "runtime"
    "os"
)

func Ping(count uint64, ping chan uint64, pong chan uint64, out chan bool, logging bool){
    var msg uint64

    for {
        msg = <-ping
        if msg >= count{
            break
        }
        if logging {
            fmt.Println("Ping", msg)
        }
        pong <- msg
    }

    out <- true
}

func Pong(ping chan uint64, pong chan uint64, logging bool){
    var msg uint64

    for {
        msg = <-pong
        if logging {
            fmt.Println("Pong", msg)
        }
        ping <- msg + 1
    }
}

func main() {

    runtime.GOMAXPROCS(1024)

    flag.Parse()

    s := flag.Arg(1)
    p := flag.Arg(0)

    var numPingPongs uint64 = 1
    var logging bool = false
    var err error = nil
    var numParam = flag.NArg()

    //string to int
    if (numParam > 1) {
        numPingPongs, err =  strconv.ParseUint(s, 0, 64)
        logging, err =  strconv.ParseBool(p)
    }

    if (err != nil || (numParam > 0 && numParam !=2) || numPingPongs < 1) {
        fmt.Println("Usage: go run pingpong <print output 0/1> <number of pingpongs>")
        os.Exit(1)
    }

    ping := make(chan uint64)
    pong := make(chan uint64)
    out := make(chan bool)

    //Start ping pong goroutines
    go Ping(numPingPongs, ping, pong, out, logging)
    go Pong(ping, pong, logging)

    ping <- 0

    <-out
    fmt.Println("Done")
}
