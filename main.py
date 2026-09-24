from subsystems import chassis

m_chassis = chassis.Chassis()

while True:
    cmd = input("Enter command (w/a/s/d for movement, any other key to stop, q to quit): ")
    if cmd == 'q':
        break
    elif cmd == 'w':
        m_chassis.drive(1, 0)
    elif cmd == 's':
        m_chassis.drive(-1, 0)
    elif cmd == 'a':
        m_chassis.drive(0, -1)
    elif cmd == 'd':
        m_chassis.drive(0, 1)
    else:
        m_chassis.drive(0, 0)

m_chassis.drive(0, 0)
