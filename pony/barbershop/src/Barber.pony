use "random"

actor Barber
    let _ahr: U64
    let _print: USize
    let _env: Env
    
    new create(ahr: U64, print: USize, env: Env) =>
        _ahr = ahr
        _print = print
        _env = env

    be enter(customer: Customer, room: WaitingRoom) =>
        customer.start()
        busyWaiting(MT.int(_ahr) + 10)
        customer.done()
        room.next()
        
    fun busyWaiting(limit: U64): U64 =>
        var test: U64 = 0
        var k: U64 = 0
        while (k < limit) do
            test = test + 1
            k = k + 1
        end
    test
        
    be wait() =>
        if (_print == 1) then
            _env.out.print("Barber: No customers in waiting room. Going to have a sleep.")
        end
        
    be exit() => true
