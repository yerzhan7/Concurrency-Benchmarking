package main

import "sync"

type Factory struct {
    apr int                     //Average customer production rate
    ch_self chan interface{}    //For customers to communicate with factory
    ch_report chan int          //For reporting result to main
    ch_shop chan interface{}    //For sending customers to shop
    array []Customer
}

func (f *Factory) start(haircuts int, apr int, ch_shop chan interface{}, wg *sync.WaitGroup) chan int {
    f.apr = apr
    f.ch_self= make(chan interface{})
    f.ch_report = make(chan int)
    f.ch_shop = ch_shop
    defer wg.Done()

    //Produce customers
    f.array = make([]Customer, haircuts)
    for i := 0; i < haircuts; i++ {
        f.array[i].start(i, f.ch_self)
        f.sendCustomerToShop(i)
        //Busy wait
        busyWait(f.apr)
    }

    go f.receive()
    return f.ch_report
}

func (f *Factory) receive(){
    var completed_haircuts int = 0
    var total_attempts int = 0

    //Receive
    for {
        msg := <-f.ch_self
        switch msg.(type)  {
        case int:
            //Customer has returned
            //Increment total attempts
            total_attempts++
            //Send back
            id := msg.(int)
            f.sendCustomerToShop(id-1)
        case bool:
            //Customer is finished - increment counter
            total_attempts++
            completed_haircuts++
            if(completed_haircuts == haircuts){
                //Tell shop to finish
                f.ch_shop <- true
                //Send report of total attempts
                f.ch_report <- total_attempts
                return
            }
        }
    }

}

func (f *Factory) sendCustomerToShop(id int){
    //Send customer reference to shop
    f.ch_shop <- &f.array[id]
}
