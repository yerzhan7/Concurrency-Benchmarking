use "collections"
use "debug"

actor Body
    let _id: USize
    let _world: World
    let _mass: F64

    let _h: F64 // General tick for Adam-Bashforth steps
    let _h_in: F64 // Tick for initial Euler steps

    let _gr: F64 = 1 // Global gravity constant for calculating force

    // Constants for Adams-Bashforth method:
    let _ab1: F64 = -3 / 8
    let _ab2: F64 = 37 / 24
    let _ab3: F64 = -59 / 24
    let _ab4: F64 = 55 / 24

    new create(id: USize, world: World, mass: F64, h: F64, h_in: F64) =>
        _id = id
        _world = world
        _mass = mass
        _h = h
        _h_in = h_in

    be euler_step(positions: Array[Vector val] val, velocities: Array[Vector val] val, masses: Array[F64] val) =>
        var my_pos: Vector val = Vector()
        var my_vel: Vector val = Vector()
        try
            my_pos = positions(_id)
            my_vel = velocities(_id)
        end

        let new_position: Vector val = my_pos + my_vel.mult_const(_h_in)
        let new_velocity: Vector val = my_vel + total_force(positions, masses).mult_const(_h_in / _mass)

        _world.report(new_position, new_velocity, _id) // Report my new position/velocity to the world

    be adams_bashforth_step(pos: Array[Array[Vector val] val] val,
                            vel: Array[Array[Vector val] val] val,
                            masses: Array[F64] val) =>

        let u1234: Vector val = try vel(0)(_id).mult_const(_ab1) +
                                    vel(1)(_id).mult_const(_ab2) +
                                    vel(2)(_id).mult_const(_ab3) +
                                    vel(3)(_id).mult_const(_ab4)
                                else Vector()
                                end

        let f1234: Vector val = try total_force(pos(0), masses).mult_const(_ab1) +
                                    total_force(pos(1), masses).mult_const(_ab2) +
                                    total_force(pos(2), masses).mult_const(_ab3) +
                                    total_force(pos(3), masses).mult_const(_ab4)
                                else Vector()
                                end

        let new_position: Vector val = try pos(3)(_id) + u1234.mult_const(_h)
                                       else Vector()
                                       end

        let new_velocity: Vector val = try vel(3)(_id) + f1234.mult_const(_h / _mass)
                                       else Vector()
                                       end

        _world.report(new_position, new_velocity, _id) // Report my new position/velocity to the world

    // Distance btw 2 bodies
    fun distance(p1: Vector val, p2: Vector val): F64 => (p1 - p2).magnitude()

    // Newtons Gravity Force Function
    fun f(x: F64): F64 => (-1 / (x * x))

    // Force vector btw 2 bodies
    fun force(p1: Vector val, p2: Vector val, m1: F64, m2: F64): Vector val =>
        let dist: F64 = distance(p1, p2)
        let diff: Vector val = p1 - p2
        let fm: F64 = m1 * m2 * f(dist) * _gr
        diff.mult_const(fm / dist)

    // Total Force on this body
    fun total_force(positions: Array[Vector val] val, masses: Array[F64] val): Vector val =>
        var sum: Vector val = Vector()
        var my_pos: Vector val = Vector()
        try my_pos = positions(_id) end
        for i in Range[USize](0, positions.size()) do
            if i != _id then
                var other_pos: Vector val = Vector()
                try other_pos = positions(i) end
                var other_mass: F64 = 0
                try other_mass = masses(i) end
                sum = sum + force(my_pos, other_pos, _mass, other_mass)
            end
        end
        sum
