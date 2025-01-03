from model.data.MeasuringDeviceDB import *
from model.plant.MeasuringDeviceLogic import *

class MeasuringDevice(MeasuringDeviceDB, MeasuringDeviceLogic):
    
    def __init__(self, recId:int, devId:int, id=None):
        MeasuringDeviceDB.__init__(self, recId, devId, id)
        MeasuringDeviceLogic.__init__(self, 
                                      recId.to_bytes(1, byteorder='big'), 
                                      devId.to_bytes(1, byteorder='big')
                                      )
        
        print(self.recId, self.devId)
        print(self._recId, self._devId)
        

    @classmethod        
    def DBDeviceAdapter(cls, mddb:MeasuringDeviceDB):
        return cls(mddb.recId, mddb.devId, mddb.id)
        
    
    @classmethod
    def getLast(cls) -> "MeasuringDevice":
        return cls.DBDeviceAdapter(MeasuringDeviceDB.getLast())
    
    @classmethod
    def getAll(cls) -> list["MeasuringDevice"]:
        return list(map(lambda x: cls.DBDeviceAdapter(x), MeasuringDeviceDB.getAll()))
    
    @classmethod
    def getByID(cls, id:int) -> "MeasuringDevice":
        return cls.DBDeviceAdapter(MeasuringDeviceDB.getByID(id))
    
    @classmethod
    def getByDevRecId(cls, recId:int, devId:int) -> "MeasuringDevice":
        return cls.DBDeviceAdapter(MeasuringDeviceDB.getByRecDevId(recId, devId))
    
    def makeMeasurement(self, ser:Serial):
        res, code, voltage, resist = self.readData(ser)
        
        if res:
            
            res =  self._saveMeasurement(resist, voltage)
            print('Device', self.devId, self.recId, 
                  '\n Measuring is done:', 
                  '\n    -code', code, 
                  '\n    -voltage', voltage, 
                  '\n    -resist',resist,
                  '\n')
        else:
            print('Device', self.devId, self.recId, 
                  '\n Measuring error', code,
                  '\n')
            return False