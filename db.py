from sqlalchemy import *
import sqlalchemy as db
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus as urlquote
from sqlalchemy.sql import table, column, select, update, insert


engine = create_engine('mysql+pymysql://root:%s@localhost/count'%urlquote('root'), echo=True, future=True)
# use session_factory() to get a new Session
_SessionFactory = sessionmaker(bind=engine)

Base = declarative_base()

def configTable(mytable):
    metadata = MetaData(bind=engine)
    mytable = Table(mytable, metadata, autoload=True)
    return mytable
def session_factory():
    Base.metadata.create_all(engine)
    return _SessionFactory()
