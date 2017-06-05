package main

import "fmt"

type Barber struct{
    ahr int
    ch_barber chan interface{}
}

func (b *Barber) start(ahr int) chan interface{} {
    b.ahr = ahr
    b.ch_barber = make(chan interface{})

    go b.receive()
    return b.ch_barber
}

func (b *Barber) receive(){
    //Listen for customers
    for {
        msg := <-b.ch_barber
        switch msg.(type)  {
        case *Customer:
            //Customer has arrived
            customer := msg.(*Customer)
            customer.cust <- BEGIN
            //Do haircut
            busyWait(b.ahr)
            close(customer.cust) //Equivalent of 'END'
            //Ask shop for next customer
            b.ch_barber <- NEXT
        case int:
            //Message from shop
            //Extract message
            msg = msg.(int)
            if(msg == WAIT){
                //No customers waiting
                if(logging){
                    fmt.Println("Barber: No customers in waiting room. Going to have a sleep.")
                }
            } else if (msg == EXIT) {
                //No customers remaining
                return
            }
        }
    }
}
