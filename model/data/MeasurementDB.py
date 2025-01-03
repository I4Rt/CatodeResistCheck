from model.data.BaseData import *

class MeasurementDB(BaseData):
    __tablename__ = 'measurement_db'
    
    value = Column(Double, nullable=False)
    value_type = Column(String, nullable=False)
    
    measurement_device_id = Column(Integer, ForeignKey('measuring_device_db.id', ondelete="CASCADE"), nullable=False)

    def __init__(self, valType:str, val:float, measurement_device_id:int, id=None):
        super().__init__(id)
        self.value_type = valType
        self.value = val
        self.measurement_device_id = measurement_device_id