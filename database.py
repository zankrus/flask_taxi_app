import time
import datetime
from contextlib import contextmanager

from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, Boolean, TIMESTAMP, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationships, scoped_session

engine = create_engine('sqlite:///taxi.db')
Base = declarative_base()

Session = scoped_session(sessionmaker(autoflush=True, autocommit=False, bind=engine))


@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        # session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


class Drivers(Base):
    __tablename__ = "drivers"
    id = Column(Integer, autoincrement=True, primary_key=True, comment='айди водителя')
    name = Column(String, nullable=False)
    car = Column(String, nullable=False)

    def insert_drivers(self, name, car):
        with session_scope() as session:
            session.add(Drivers(name=name, car=car))
            session.commit()
    def show_drivers(self, id):
        with session_scope() as session:
            show_dr = session.query(Drivers).filter(Drivers.id == id).all()
            print(str(show_dr))
            return show_dr
    def delete_driver(self, id):
        with session_scope() as session:
            session.query(Drivers).filter(Drivers.id == id).delete()
            session.commit()


    def __repr__(self):
        return str({"id": self.id, "name": self.name, "car": self.car})


class Clients(Base):
    Session = sessionmaker(bind=engine)
    session = Session()
    __tablename__ = "clients"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String, nullable=False)
    is_vip = Column(Boolean)

    def insert_clients(self, name, vip: bool= False):
        with session_scope() as session:
            session.add(Clients(name=name, is_vip=vip))
            session.commit()
    def show_clients(self, id):
        with session_scope() as session:
            show_clie = session.query(Clients).filter(Clients.id == id).all()
            print(str(show_clie))
            return show_clie
    def delete_clients(self, id):
        with session_scope() as session:
            session.query(Clients).filter(Clients.id == id).delete()
            session.commit()

    def __repr__(self):
        return str({"id": self.id, "name": self.name, "vip": self.is_vip})

class Orders(Base):
    Session = sessionmaker(bind=engine)
    session = Session()
    __tablename__ = 'orders'
    id = Column(Integer, autoincrement=True, primary_key=True)
    address_from = Column(String, nullable=False)
    address_to = Column(String, nullable=False)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    driver_id = Column(Integer, ForeignKey('drivers.id'), nullable=False)
    date_created = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    status = Column(String, nullable=False)


#


Base.metadata.create_all(engine)
