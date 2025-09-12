import serial.tools.list_ports
import serial


def see_ports():
    """ Returns the available ports at the moment """
    return serial.tools.list_ports.comports()


def connect_to(portID, bauds):
    # makes the connection to the selected port
    try:
        ser = serial.Serial(portID, baudrate=bauds)
    except serial.serialutil.SerialException:
        ser = "None"
    return ser


def read_port(serialCOM):
    # reads on entire line from the communication port
    data = serialCOM.readline()
    data = data.decode('utf8')
    print(data)
    # serial.serialutil.SerialException
    return data


def write_port(serialCOM, Command):
    # writes the user command in the connected port
    serialCOM.write(Command)
