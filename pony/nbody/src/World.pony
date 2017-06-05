use "collections"
use "debug"

actor World
    let _env: Env
    let _print: USize
    let _bodies: Array[Body tag] = Array[Body] // Array of bodies
    let _body_qty: USize // Qty of bodies

    let _zero: Vector val = Vector() // Zero vector - acts as NULL pointer/reference

    // val positions and velocities of bodies at step 0, 1, 2 and 3 to send to all bodies for calculations
    var _pos_val: Array[Array[Vector val] val]
    var _vel_val: Array[Array[Vector val] val]

    // iso variables to record updates from bodies
    var _pos_temp: Array[Vector val] iso = recover iso Array[Vector val] end
    var _vel_temp: Array[Vector val] iso = recover iso Array[Vector val] end

    let _masses: Array[F64] val // Constant array of masses of bodies
    let _mass_star: F64 = 10000 // Constant mass the first body (star)
    let _mass_planet: F64 = 10 // Constant mass of each body, except the first body

    let _steps: U32 // Total number of steps
    let _euler_steps: U32 = 1000 // Number of steps for initial euler method in one _steps
    let _h: F64 = 0.01 // General tick (dt) for Adam-Bashforth steps
    let _h_in: F64 = _h / _euler_steps.f64()  // Tick (dt) for initial Euler steps
    let _print_step: U32 = (1 / _h).u32() // Print only every _print_step

    var _sim_cnt: U32 // Counter of steps
    var _euler_step_cnt: U32 // Euler step counter
    var _pending_msg_cnt: USize // Counter of how many msg left to receive from bodies at each step

    new create(body_qty: USize, steps: U32, env: Env, print: USize) =>
        _body_qty = body_qty
        _steps = steps
        _env = env
        _print = print

        _pos_val = Array[Array[Vector val] val].init(recover val Array[Vector val] end, 4)
        _vel_val = Array[Array[Vector val] val].init(recover val Array[Vector val] end, 4)

        // Setting up time
        _sim_cnt = 0
        _euler_step_cnt = 0
        _pending_msg_cnt = 0

        if print == 1 then
            _env.out.print(_body_qty.string() + " " + (_h * _steps.f64()).u64().string())
        end

        // Creating Bodies with initial position, velocity and mass
        let masses: Array[F64] iso = recover iso Array[F64] end
        for body_id in Range[USize](0, _body_qty) do
            var pos: Vector val
            var velo: Vector val
            var mass: F64
            if body_id == 0 then // IF first - Star
                pos = _zero  // Position (0,0,0)
                velo = _zero // Velocity (0,0,0)
                mass = _mass_star
            else // ELSE Planet
                pos = Vector((100.0 + (100.0 * body_id.f64())).f64(), 0, 0)
                velo = Vector(0,(10000.0 / (100.0 + (100 * body_id.f64()))).sqrt())
                mass = _mass_planet
            end

            masses.push(mass)
            try _bodies.push(Body(body_id, this, masses(body_id), _h, _h_in)) end // Bodies
            _pos_temp.push(pos)  // Initial Position
            _vel_temp.push(velo) // Initial Velocity
            Debug.out("DBG: Created a body " + body_id.string() + ": position - " + pos.string() + ", velocity - " + velo.string() + ", mass - " + mass.string())
            if print == 1 then
                _env.out.print(pos.film() + " " + mass.string())
            end
        end
        _masses = consume masses
        Debug.out("DBG: Created " + _body_qty.string() + " bodies for simulation.")

    be run_sim() =>
        if _euler_step_cnt < (3 * _euler_steps) then // Firstly, do Euler steps to calculate initial steps 1, 2 and 3
            _euler_step_cnt = _euler_step_cnt + 1
            (let euler_step_div, let euler_step_mod) = _euler_step_cnt.divmod(_euler_steps)

            if euler_step_mod == 1 then // Euler - record step 0, 1 and 2 as val
                Debug.out("DBG: Requesting Euler updates from the bodies - recorded step " + euler_step_div.string())
                _pending_msg_cnt = _body_qty

                // Create a sendable arrays of Velocities and Positions of all bodies at current state for an update
                var pos_iso = recover iso Array[Vector val].init(_zero, _body_qty) end // An array to fill pos_iso field after destructive read
                try _pos_val(euler_step_div.usize()) = _pos_temp = consume pos_iso end
                var vel_iso = recover iso Array[Vector val].init(_zero, _body_qty) end
                try _vel_val(euler_step_div.usize()) = _vel_temp = consume vel_iso end

                // Sending/Requesting an update for new step
                for body in _bodies.values() do
                    try body.euler_step(_pos_val(euler_step_div.usize()), _vel_val(euler_step_div.usize()), _masses) end
                end

            else // Euler do not record as val - send the results immediately for the next Euler step
                Debug.out("DBG: Requesting Euler updates from the bodies.")
                _pending_msg_cnt = _body_qty
                var pos_iso = recover iso Array[Vector val].init(_zero, _body_qty) end
                let pos_val: Array[Vector val] val = _pos_temp = consume pos_iso
                var vel_iso = recover iso Array[Vector val].init(_zero, _body_qty) end
                let vel_val: Array[Vector val] val = _vel_temp = consume vel_iso

                for body in _bodies.values() do
                    body.euler_step(pos_val, vel_val, _masses)
                end
            end

        else // Now we've calculated initial 4 positions/velocities using Euler required for Adams-Bashforth.
             // Do Adams-Bashforth steps
            if (_print == 1) and (_sim_cnt != 0)  and (_sim_cnt.mod(_print_step) == 0) then
                for body_id in Range[USize](0, _body_qty) do
                    try _env.out.write(_pos_temp(body_id).film() + " ") end
                end
                _env.out.write("\n")
            end
            
            _sim_cnt = _sim_cnt + 1
            if _sim_cnt <= _steps then
                Debug.out("DBG: Time is " + _sim_cnt.string()  + " ticks. Requesting Adams-Bashforth updates from the bodies.")
                _pending_msg_cnt = _body_qty

                if _sim_cnt == 1 then // IF the first step THEN need to record euler step 3 as val
                    var pos_iso = recover iso Array[Vector val].init(_zero, _body_qty) end
                    try _pos_val(3) = _pos_temp = consume pos_iso end
                    var vel_iso = recover iso Array[Vector val].init(_zero, _body_qty) end
                    try _vel_val(3) = _vel_temp = consume vel_iso end

                else // ELSE shift positions and velocities and record new step 3 as val
                    var pos_iso = recover iso Array[Vector val].init(_zero, _body_qty) end
                    try _pos_val.shift() end
                    _pos_val.push(_pos_temp = consume pos_iso)
                    var vel_iso = recover iso Array[Vector val].init(_zero, _body_qty) end
                    try _vel_val.shift() end
                    _vel_val.push(_vel_temp = consume vel_iso)

                end

                let sendable_pos: Array[Array[Vector val] val] val = build_sendable(_pos_val)
                let sendable_vel: Array[Array[Vector val] val] val = build_sendable(_vel_val)

                for body in _bodies.values() do
                    body.adams_bashforth_step(sendable_pos, sendable_vel, _masses)
                end

            end
        end

    // Reporting of new position and velocity by body
    be report(pos: Vector val, vel: Vector val, id: USize) =>
        Debug.out("DBG: Got an update (" + _sim_cnt.string() + ") from body " + id.string() + ": new position is " + pos.string() + ", new velocity is " + vel.string())

        try // Dummy try block - there is no way an exception can happen here
            _pos_temp(id) = pos
            _vel_temp(id) = vel
        end

        _pending_msg_cnt = _pending_msg_cnt - 1
        if _pending_msg_cnt == 0 then // IF msgs received from ALL bodies THEN run next step sim
            run_sim()
        end

    fun build_sendable(array: Array[Array[Vector val] val]): Array[Array[Vector val] val] val =>
        let array_iso = recover iso Array[Array[Vector val] val] end
        array_iso.reserve(array.size())
        for value in array.values() do
            array_iso.push(value)
        end

        consume array_iso
