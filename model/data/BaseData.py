from config import *
from model.abstracts.Jsonifyer import *
from sqlalchemy import or_, and_
from datetime import datetime

from model.abstracts.DBSessionMaker import *

class BaseData(Jsonifyer, Base):
    __abstract__ = True
    
    id = Column(Integer, primary_key=True)
    
    def __init__(self, id = None):
        Jsonifyer.__init__(self)
        self.id = id
             
    def __save(self):
        with DBSessionMaker.getSession() as ses:
            ses.add(self)
            ses.commit()
            return self.id
        
    def save(self):
        self:self.__class__ = self.getByID(self.__save())
        
    @classmethod 
    def getAll(cls) -> list["BaseData"]:
        with DBSessionMaker.getSession() as ses:
            value = ses.query(cls).all()
            return value

    @classmethod
    def getLast(cls) -> "BaseData":
        with DBSessionMaker.getSession() as ses:
            value = ses.query(cls).order_by(cls.id.desc()).first()
            return value
        
    @classmethod 
    def getByID(cls, searchId:int) -> "BaseData":
        with DBSessionMaker.getSession() as ses:
            value = ses.query(cls).filter_by(id=searchId).first()
            return value

    def delete(self):
        with DBSessionMaker.getSession() as ses:
            ses.delete(self)
            ses.commit()
            
    @classmethod
    def deleteAll(cls):
        with DBSessionMaker.getSession() as ses:
            res = ses.query(cls).delete()
            ses.commit()
            
    @classmethod
    def deleteByID(cls, targetId):
        with DBSessionMaker.getSession() as ses:
            res = ses.query(cls).filter_by(id=targetId).delete()
            ses.commit()
              
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.getParamsList()}>"
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__} {self.getParamsList()}"
    
    
    
        
    