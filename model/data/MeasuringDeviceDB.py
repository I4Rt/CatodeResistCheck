from model.data.BaseData import *
from model.data.MeasurementDB import *


class MeasuringDeviceDB(BaseData):
    __tablename__ = 'measuring_device_db'
    
    recId = Column(Integer, nullable=False)
    devId = Column(Integer, nullable=False)
    
    measurements = relationship('MeasurementDB', cascade="all,delete", backref='measuring_device_db', lazy='select')
    
    __table_args__ = (UniqueConstraint('recId', 'devId'), )
    
    def __init__(self, recId:bytes|int, devId:bytes|int, id=None):
        super().__init__(id)
        if type(recId) == int:
            self.recId = recId
        elif type(recId) == bytes:
            self.recId = int.from_bytes(recId, byteorder='big')
        else:
            raise Exception('Wrong recId type')
        
        if type(devId) == int:
            self.devId = devId
        elif type(devId) == bytes:
            self.devId = int.from_bytes(devId, byteorder='big')
        else:
            raise Exception('Wrong recId type')
        
    @classmethod
    def getByRecDevId(cls, recId, devId):
        with DBSessionMaker.getSession() as ses:
            return ses.query(cls).filter(
                        cls.recId == recId,
                        cls.devId == devId  
                    ).first()
    
    def _saveMeasurement(self, resist, voltage):           # TODO: move this method away
        try:
            voltageDB = MeasurementDB('voltage', voltage, self.id)
            voltageDB.save()
            
            resistDB = MeasurementDB('resist', resist, self.id)
            resistDB.save()
            
            return True
        except Exception as e:
            print(e)
            pass
        return False