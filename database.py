"""File with DB methods and Clasees."""
import datetime
from contextlib import contextmanager
from typing import Any, Generator

import dateutil.parser
from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

engine = create_engine('sqlite:///taxi.db')
Base = declarative_base()  # type: Any

Session = scoped_session(sessionmaker(autoflush=True, autocommit=False, bind=engine))


@contextmanager
def session_scope() -> Generator:
    """Creation session."""
    session = Session()
    try:
        yield session
        # session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


class Drivers(Base):
    """Class for Drivers table."""

    __tablename__ = "drivers"
    id = Column(Integer, autoincrement=True, primary_key=True, comment='айди водителя')
    name = Column(String, nullable=False)
    car = Column(String, nullable=False)

    def insert_drivers(self, name: str, car: str) -> Any:
        """Method for insert in table."""
        with session_scope() as session:
            session.add(Drivers(name=name, car=car))
            session.commit()

    def show_drivers(self, id: int) -> Any:
        """Method for select from Drivers."""
        with session_scope() as session:
            show_dr = session.query(Drivers).filter(Drivers.id == id).all()
            print(str(show_dr))
            return show_dr

    def delete_driver(self, driver_id: int) -> Any:
        """Method for delete from Drivers."""
        with session_scope() as session:
            session.query(Drivers).filter(Drivers.id == driver_id).delete()
            session.commit()

    def __repr__(self) -> str:
        """Reload method for print from Drivers."""
        return str({"id": self.id, "name": self.name, "car": self.car})


class Clients(Base):
    """Class for Clients table."""

    __tablename__ = "clients"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String, nullable=False)
    is_vip = Column(Boolean)

    def insert_clients(self, name: str, vip: bool = False) -> Any:
        """Method for insert into CLient."""
        with session_scope() as session:
            session.add(Clients(name=name, is_vip=vip))
            session.commit()

    def show_clients(self, client_id: int) -> Any:
        """Method for select from Clients."""
        with session_scope() as session:
            show_clie = session.query(Clients).filter(Clients.id == client_id).all()
            print(str(show_clie))
            return show_clie

    def delete_clients(self, client_id: int) -> Any:
        """Method for delete from Drivers."""
        with session_scope() as session:
            session.query(Clients).filter(Clients.id == client_id).delete()
            session.commit()

    def __repr__(self) -> str:
        """Reload method for print from Clients."""
        return str({"id": self.id, "name": self.name, "vip": self.is_vip})


class Orders(Base):
    """Class for Orders table."""

    __tablename__ = 'orders'
    id = Column(Integer, autoincrement=True, primary_key=True)
    address_from = Column(String, nullable=False)
    address_to = Column(String, nullable=False)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    driver_id = Column(Integer, ForeignKey('drivers.id'), nullable=False)
    date_created = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    status = Column(String, nullable=False)
    status_valid = ['not accepted', 'in progress', 'done', 'cancelled']

    def show_order(self, order_id: int) -> Any:
        """Method for select from Orders."""
        with session_scope() as session:
            show_ord = session.query(Orders).filter(Orders.id == order_id).all()
            return show_ord

    def insert_order(self, address_from: str, address_to: str, client_id: int, driver_id: int, date: str, status: str) \
            -> Any:
        """Method for insert into Order."""
        with session_scope() as session:
            session.add(Orders(address_from=address_from, address_to=address_to, client_id=client_id,
                               driver_id=driver_id, date_created=dateutil.parser.isoparse(date), status=status))
            session.commit()

    def update_orders(self, order_id: int, new_status: str) -> Any:
        """Method for update Orders for status == In progress ."""
        with session_scope() as session:
            session.query(Orders).filter(Orders.id == order_id).update({Orders.status: new_status}
                                                                       )
            session.commit()

    def update_orders_not_accepted(self, order_id: int, new_status: str, new_date: str, new_driver: int,
                                   new_client: int) -> Any:
        """Method for update Orders for status == not accepted ."""
        with session_scope() as session:
            session.query(Orders).filter(Orders.id == order_id).update({Orders.status: new_status,
                                                                        Orders.date_created: dateutil.parser.isoparse(
                                                                            new_date),
                                                                        Orders.driver_id: new_driver,
                                                                        Orders.client_id: new_client})
            session.commit()

    def __repr__(self) -> str:
        """Reload method for print from Orders."""
        return str({"id": self.id, "address_from": self.address_from, "address_to": self.address_to,
                    "client_id": self.client_id, "driver_id": self.driver_id, "date_created": self.date_created,
                    "status": self.status})


Base.metadata.create_all(engine)


def striper(string: str) -> dict:
    """Method to convert str from responce to dict."""
    edited_str = string.replace('[', "").replace(']', '').replace("'", '"')
    dict_from_str = eval(edited_str)
    return dict_from_str
