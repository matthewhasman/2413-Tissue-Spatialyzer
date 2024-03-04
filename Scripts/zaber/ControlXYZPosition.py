from zaber_motion import Units
from zaber_motion.ascii import Connection
from Fluigent.SDK import fgt_init, fgt_close
from Fluigent.SDK import fgt_set_pressure, fgt_get_pressure, fgt_get_pressureRange

pressure_mbar = -400

fgt_init()

fgt_set_pressure(0, pressure_mbar)

with Connection.open_serial_port("COM6") as connection:
    connection.enable_alerts()

    device_list = connection.detect_devices()

    device = device_list[0]

    xAxis = device.get_lockstep(1)
    yAxis = device.get_axis(3)
    zAxis = device.get_axis(4)
    
    xAxis.home()
    yAxis.home()
    zAxis.home()

    while (True):
        pressureMeasurement = fgt_get_pressure(0)
        print('Current pressure: {}'.format(pressureMeasurement))

        option = input("Absolute (0) or Relative (1) or q to quit")

        if int(option) != 0 and int(option) != 1 and option.lower() != 'a' and option.lower() != 'r' and option.lower() != 'q':
            continue

        if option.lower() == 'q':
            break
        
        xDist = input("Enter x distance to move (mm):")
        yDist = input("Enter y distance to move (mm):")
        zDist = input("Enter z distance to move (mm):")

        xAxis.wait_until_idle()
        yAxis.wait_until_idle()
        zAxis.wait_until_idle()

        try:
            if int(option) == 0 or option.lower()=='a':
                if xDist != "":
                    xDist = int(xDist)
                    xAxis.move_absolute(xDist, Units.LENGTH_MILLIMETRES, wait_until_idle=False)

                if yDist != "":
                    yDist = int(yDist)
                    yAxis.move_absolute(yDist, Units.LENGTH_MILLIMETRES, wait_until_idle=False)
                
                if zDist != "":
                    zDist = int(zDist)
                    zAxis.move_absolute(zDist, Units.LENGTH_MILLIMETRES, wait_until_idle=False)
                
            elif int(option) == 1 or option.lower()=='r':
                if xDist != "":
                    xDist = int(xDist)
                    xAxis.move_relative(xDist, Units.LENGTH_MILLIMETRES, wait_until_idle=False)
                
                if yDist != "":
                    yDist = int(yDist)
                    yAxis.move_relative(yDist, Units.LENGTH_MILLIMETRES, wait_until_idle=False)

                if zDist != "":
                    zDist = int(zDist)    
                    zAxis.move_relative(zDist, Units.LENGTH_MILLIMETRES, wait_until_idle=False)
        except Exception as e:
            print ("An error occured:", e)

        print('Absolute x position (mm): ' + str(xAxis.get_position(Units.LENGTH_MILLIMETRES)))
        print('Absolute y position (mm): ' + str(yAxis.get_position(Units.LENGTH_MILLIMETRES)))
        print('Absolute z position (mm): ' + str(zAxis.get_position(Units.LENGTH_MILLIMETRES)))

fgt_set_pressure(0, 0)
fgt_close()
