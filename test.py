from subsystems import Shooter

m_angle_adj = Shooter().angle_adj

cmd = ""
m_angle_adj.enable()

while True:
    cmd = input("CMD: ")
    if cmd == "w":
        m_angle_adj.start()
    elif cmd == "s":
        m_angle_adj.start(True)
    else:
        m_angle_adj.stop()
        m_angle_adj.disable()
        break