from config import *

from model.static.ConnectionHolder import ConnectionHolder

from model.MeasuringDevice import *

from time import sleep

if __name__ == "__main__":
    Base.metadata.create_all(e)
    
    CONST_REC_ID = 2
    
    ConnectionHolder.changePort(COM_NAME, baudrate=9600, timeout=2, parity='N')
    ser = ConnectionHolder.getConnection()
    devices = MeasuringDevice.getAll()
    
    while True:
        if ser:
            for md in devices:
                md.makeMeasurement(ser)
        else:
            ConnectionHolder.changePort(COM_NAME, baudrate=9600, timeout=2, parity='N')
            ser = ConnectionHolder.getConnection()
            sleep(0.5)
        