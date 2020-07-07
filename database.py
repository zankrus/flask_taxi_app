import time
import datetime
from contextlib import contextmanager
import dateutil.parser
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
    __tablename__ = "clients"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String, nullable=False)
    is_vip = Column(Boolean)

    def insert_clients(self, name, vip: bool = False):
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
    __tablename__ = 'orders'
    id = Column(Integer, autoincrement=True, primary_key=True)
    address_from = Column(String, nullable=False)
    address_to = Column(String, nullable=False)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    driver_id = Column(Integer, ForeignKey('drivers.id'), nullable=False)
    date_created = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    status = Column(String, nullable=False)
    status_valid = ['not accepted', 'in progress', 'done', 'cancelled']

    def show_order(self, order_id):
        with session_scope() as session:
            show_ord = session.query(Orders).filter(Orders.id == order_id).all()
            return show_ord

    def insert_order(self, address_from, address_to, client_id, driver_id, date, status):
        with session_scope() as session:
            session.add(Orders(address_from=address_from, address_to=address_to, client_id=client_id,
                               driver_id=driver_id, date_created=dateutil.parser.isoparse(date), status=status))
            session.commit()

    def update_orders(self, order_id, new_status, new_date, new_driver, new_client):
        with session_scope() as session:
            session.query(Orders).filter(Orders.id == order_id).update({Orders.status: new_status,
                                                                        Orders.date_created: dateutil.parser.isoparse(
                                                                            new_date),
                                                                        Orders.driver_id: new_driver,
                                                                        Orders.client_id: new_client})
            session.commit()

    def __repr__(self):
        return str({"id": self.id, "address_from": self.address_from, "address_to": self.address_to,
                    "client_id": self.client_id, "driver_id": self.driver_id, "date_created": self.date_created,
                    "status": self.status})


Base.metadata.create_all(engine)


def striper(string: str):
    edited_str = string.replace('[', "").replace(']', '').replace("'", '"')
    dict_from_str = eval(edited_str)
    return dict_from_str
