actor Customer
    
    let _id: USize
    let _customerFactory: CustomerFactory
    let _print: USize
    let _env: Env 
    
    new create(id: USize, customerFactory: CustomerFactory, print: USize, env: Env) =>
        _id = id
        _customerFactory = customerFactory
        _print = print
        _env = env 
        
    be full() =>
        if (_print == 1) then
            _env.out.print("Customer " + _id.string() + ": The waiting room is full. I am leaving.")
        end
        _customerFactory.returned(this)

    be wait() =>
        if (_print == 1) then
            _env.out.print("Customer " + _id.string() + ": Barber is busy. I will wait in the waiting room.")
        end
         
    be start() =>
        if (_print == 1) then
            _env.out.print("Customer " + _id.string() + ": I am now being served.")
        end
         
    be done() =>
        if (_print == 1) then
            _env.out.print("Customer " + _id.string() + ": I have been served.")
        end
         _customerFactory.done()
    
