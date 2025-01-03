from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base

from multiprocessing import Manager

Base = declarative_base()
e = create_engine("postgresql://postgres:qwerty@localhost:5432/catode_resist_check", echo=False)


COM_NAME = '/dev/ttyUSB0'