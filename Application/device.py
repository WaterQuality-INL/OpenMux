from palmsens.instrument import Instrument
import palmsens.mscript
from palmsens.serial import Serial


class Emstat4(Instrument):
    def __init__(self, COM, timeout):
        """
        initializing EmStat4 communication via Istrument class
        :param COM: COMport ID for serial communication
        """
        self.COM = COM
        self.name = __class__.__name__
        # Init serial comm using Palmsens API
        self.ser = Serial(COM, timeout=timeout)
        # Init instrument
        super().__init__(self.ser)

    def openSerial(self):
        """ To start COM port communication. Call before sending methodScript"""
        if not self.ser.connection.is_open:
            self.ser.open()

    def closeSerial(self):
        """ Close COM port communication. Call after finishing communication"""
        if self.ser.connection.is_open:
            self.ser.close()

    def parseData(self, data):
        """
        Parse data according to methodScript communication protocol
        :param data: List object
        :return: list object. parsed data
        """
        return palmsens.mscript.parse_result_lines(data)

    def parseline(self, line: str):
        """
        Parse a single line. returns x, y and [channel id, channel bit map].
        """
        data = palmsens.mscript.parse_mscript_data_package(line)
        if data is not None:
            #        time           # potential     #Metadata [channel id, channel, channel bit map]
            if data.__len__() == 5:
                return [data[0].value, data[1].value, [data[2].value, data[3].value, data[4].value]]
            elif data.__len__() == 6:
                return [data[0].value, data[1].value, data[2].value, [data[3].value, data[4].value, data[5].value]]
        else:
            return None
