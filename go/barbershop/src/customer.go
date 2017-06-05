package main

import "fmt"

type Customer struct {
    id int                      //Customer ID
    cust chan int               //Channel to customer
    ch_factory chan interface{}    //Channel to factory
}

func (c *Customer) start(id int, ch_factory chan interface{}){
    //Setup
    c.id = id + 1
    c.ch_factory = ch_factory
    c.cust = make(chan int)

    go c.receive()
}

func (c *Customer) receive(){
    for msg := range c.cust {
        switch {
            case msg == FULL:
                if(logging){
                    fmt.Printf("Customer %d: The waiting room is full. I am leaving.\n", c.id)
                }
                //Return to factory
                c.ch_factory <- c.id
            case msg == WAIT:
                if(logging){
                    fmt.Printf("Customer %d: Barber is busy. I will wait in the waiting room.\n", c.id)
                }
            case msg == BEGIN:
                if(logging){
                    fmt.Printf("Customer %d: I am now being served.\n", c.id)
                }
        }
    }

    if(logging){
        fmt.Printf("Customer %d: I have been served.\n", c.id)
    }
    //Report completion to factory
    c.ch_factory <- true
    return
}
