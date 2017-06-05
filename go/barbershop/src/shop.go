package main

type Shop struct{
    capacity int                //Waiting room size
    queue []*Customer           //Waiting room
    waiting int                 //Current waiting customers
    ch_shop chan interface{}    //Channel to self
    ch_barber chan interface{}  //Channel to barber
}

func (s *Shop) start(capacity int, ch_barber chan interface{}) chan interface{}{
    s.capacity = capacity
    s.waiting= 0
    s.ch_barber = ch_barber
    s.queue = make([]*Customer, capacity)
    s.ch_shop = make(chan interface{})

    go s.receive()
    return s.ch_shop
}

func (s *Shop) receive(){
    barber_sleep := true

    for {
        select{
        //Receive signal over 'shop' channel
        case msg := <-s.ch_shop:
            switch msg.(type) {
                //Customer arrives
                case *Customer:
                    customer := msg.(*Customer)
                    if(s.waiting == s.capacity){
                        //Send away
                        customer.cust <- FULL
                    } else {
                        if(barber_sleep){
                            barber_sleep = false
                            //Send to barber
                            s.ch_barber <- customer
                        } else {
                            //Put in queue
                            s.queue[s.waiting] = customer
                            s.waiting++
                            customer.cust <- WAIT
                        }
                    }
                //Factory sends 'finished' signal
                case bool:
                    //Tell barber to finish
                    s.ch_barber <- EXIT
                    return
            }
        //Barber asks for next customer
        case <-s.ch_barber:
            if(s.waiting > 0){
                //Send to barber from queue
                s.waiting--
                s.ch_barber <- s.queue[s.waiting]
            } else {
                //Tell barber to sleep
                barber_sleep = true
                s.ch_barber <- WAIT
            }
        }
    }
}
