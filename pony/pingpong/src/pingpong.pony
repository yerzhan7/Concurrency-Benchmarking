actor Main
    new create(env: Env)=>
        //Default arguments
        var numPingPongs: U32 = 1
        var output: Bool = false

        //Parse command line arguments
        if env.args.size() > 1 then
            //Check correct number of args
            if env.args.size() != 3 then
                argErr(env)
                return
            end
            //Get output flag
            try
                //Hacky method means any nonzero value is interpreted as 'true'
                output = (env.args(1).u32() != 0)
            else
                argErr(env)
                return
            end
            //Get numPingPongs
            try
                if(env.args(2).u32() < 1) then
                    argErr(env)
                    return
                else
                    numPingPongs = env.args(2).u32()
                end
            else
                argErr(env)
                return
            end
        end

        //Create actors, begin run
        var ping = Ping.create(env, output, numPingPongs)

    fun argErr(env: Env) =>
        env.out.print("Usage: ./pingpong <print output 0/1> <number of pingpongs > 1>")

actor Ping
    let _partner: Pong
    let _numPingPongs: U32
    let _env: Env
    let _output: Bool

    new create(env: Env, output: Bool, numPingPongs: U32)=>
        _env = env
        _output = output
        _numPingPongs = numPingPongs
        //if _output then _env.out.print("Ping actor spawned") end
        //Create Pong actor
        _partner = Pong.create(_env, _output, this)
         
        //Start the run
        this.ping(1)

    be ping(num: U32) =>
        if num <= _numPingPongs then
            if _output then _env.out.print("Ping " + num.string()) end
            _partner.pong(num)
        //else
        //    if _output then _env.out.print("Execution finished") end
        end

actor Pong
    let _partner: Ping
    let _env: Env
    let _output: Bool

    new create(env: Env, output: Bool, partner: Ping)=>
        _env = env
        _output = output
        _partner = partner
        //if _output then _env.out.print("Pong actor spawned") end

    be pong(num: U32) =>
        if _output then _env.out.print("Pong " + (num).string()) end
        _partner.ping(num + 1)
