actor WaitingRoom

    let _capacity: USize
    let _barber: Barber
    var _barberAsleep: Bool = true 
    let _waitingCustomers: Array[Customer] // Waiting room Queue
    
    new create(capacity: USize, barber: Barber) =>
        _capacity = capacity
        _barber = barber
        _waitingCustomers = Array[Customer]

    be enter(customer: Customer, room: WaitingRoom) =>
        if (_waitingCustomers.size() == _capacity) then
            customer.full()
        else
            _waitingCustomers.push(customer)

            if (_barberAsleep == true) then
                _barberAsleep = false
                this.next()
            else
                customer.wait()
            end
       end
            
    be next() =>
        if (_waitingCustomers.size() > 0) then
            try
                let customer = _waitingCustomers.shift()                         
                _barber.enter(customer, this)
            end
        else
            _barber.wait()
            _barberAsleep = true
        end
            
    be exit() =>
        _barber.exit()
        
