use "random"

actor CustomerFactory
    let _apr: U64
    let _room: WaitingRoom
    let _haircuts: USize
    var _numHairCutsSoFar: USize = 0    
    var _idGenerator: USize = 0
    let _print: USize
    let _env: Env
    
    new create(apr: U64, room: WaitingRoom, haircuts: USize, print: USize, env: Env) =>        
        _apr = apr
        _room = room
        _haircuts = haircuts
        _print = print
        _env = env
        
    be start() =>
        var i: USize = 0
        
        while (i < _haircuts) do
            createCustomer()
            busyWaiting(MT.int(_apr) + 10)
            i = i + 1
        end
        
    fun busyWaiting(limit: U64): U64 =>
        var test: U64 = 0
        var k: U64 = 0
        
        while (k < limit) do
            test = test + 1
            k = k + 1
        end
        test
            
    fun ref createCustomer() =>    
        _idGenerator = _idGenerator + 1
        let customer =  Customer(_idGenerator, this, _print, _env)
        sendCustomerToRoom(customer)
                
    be returned(customer: Customer) =>
        _idGenerator = _idGenerator + 1 
        sendCustomerToRoom(customer)
        
    fun sendCustomerToRoom(customer: Customer) =>
        _room.enter(customer, _room)
        
    be done() =>
        _numHairCutsSoFar = _numHairCutsSoFar + 1
        if (_numHairCutsSoFar == _haircuts) then
            if (_print == 1) then
                _env.out.print("Total attempts: " + _idGenerator.string())
            end
            _room.exit()
        end
