actor Main
    new create(env: Env) =>

        var print: USize = 0
        var haircuts: USize = 500
        var waitingSize: USize = 100
        var apr: U64 = 100 // average production rate
        var ahr: U64 = 100 // average haircut rate

        if env.args.size() > 1 then
            if env.args.size() != 6 then
                argErr(env)
                return
            end

            try 
                if ((env.args(1).usize() != 0) and (env.args(1).usize() != 1)) or
                   (env.args(2).usize() < 1) or (env.args(3).usize() < 1) or
                   (env.args(4).u64() < 1) or (env.args(5).u64() < 1) then

                    argErr(env)
                    return
                else
                    print = env.args(1).usize()
                    haircuts = env.args(2).usize()
                    waitingSize = env.args(3).usize()
                    apr = env.args(4).u64()
                    ahr = env.args(5).u64()
                end
            else
                argErr(env)
                return
            end
            
        end            

        let barber = Barber(ahr, print, env)
        let room = WaitingRoom(waitingSize, barber)
        let factoryActor = CustomerFactory(apr, room, haircuts, print, env)
        
        factoryActor.start()

    fun argErr(env: Env) =>
        env.out.print("Usage: ./barbershop [output log 0/1] [total haircuts >0] [waiting room size >0] [avg customer production rate >0] [average haircut rate >0]")
