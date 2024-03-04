from zaber_motion import Units
from zaber_motion.ascii import Connection

with Connection.open_serial_port("COM6") as connection:
    connection.enable_alerts()

    device_list = connection.detect_devices()
    print("Found {} devices".format(len(device_list)))

    device = device_list[0]

    xAxis = device.get_lockstep(1)
    yAxis = device.get_axis(3)
    zAxis = device.get_axis(4)
    
    xAxis.home()
    yAxis.home()
    # zAxis.home()

    xAxis.move_absolute(10, Units.LENGTH_MILLIMETRES, wait_until_idle=False)
    yAxis.move_absolute(10, Units.LENGTH_MILLIMETRES, wait_until_idle=False)
    # zAxis.move_absolute(10, Units.LENGTH_MILLIMETRES, wait_until_idle=False)

    xAxis.wait_until_idle()
    yAxis.wait_until_idle()
    # zAxis.wait_until_idle()
