from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Model


class Service(Model):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True, index=True)
    service_name = Column(String)
    opportunities = Column(String)
    time_to_complete = Column(Integer)
    queue_item = relationship("QueueItem", back_populates="service")


class Queue(Model):
    __tablename__ = "queues"
    id = Column(Integer, primary_key=True, index=True)
    salepoint_id = Column(Integer, ForeignKey("salepoint.id"))
    salepoint = relationship("SalePoint", back_populates="queues")
    items = relationship("QueueItem", back_populates="queue")
    opportunities = Column(String)


class QueueItem(Model):
    __tablename__ = "queue_items"
    id = Column(Integer, primary_key=True, index=True)
    ticket_number = Column(String, index=True)
    queue_id = Column(Integer, ForeignKey("queues.id"))
    queue = relationship("Queue", back_populates="items")
    service_id = Column(Integer, ForeignKey("services.id"), nullable=True)
    service = relationship("Service", back_populates="queue_item")


class SalePoint(Model):
    __tablename__ = 'salepoint'

    id = Column(Integer, primary_key=True, autoincrement=True)
    salepoint_name = Column(String)
    address = Column(String)
    status = Column(String)
    rko = Column(String)
    office_type = Column(String)
    salepoint_format = Column(String)
    suo_availability = Column(String)
    has_ramp = Column(String)
    latitude = Column(String)
    longitude = Column(String)
    metro_station = Column(String)
    distance = Column(Integer)
    kep = Column(String)
    my_branch = Column(String)
    open_hours = Column(String)
    open_hours_individual = Column(String)
    services = Column(String)
    queues = relationship("Queue", back_populates="salepoint")
    load = relationship("Load", back_populates="salepoint")


class User(Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True)
    password = Column(String)
    full_name = Column(String, unique=True)
    opportunity = Column(String)
    privilege = Column(Boolean)


class Load(Model):
    __tablename__ = 'load'
    id = Column(Integer, primary_key=True, index=True)
    salepoint_id = Column(Integer, ForeignKey("salepoint.id"))
    salepoint = relationship("SalePoint", back_populates="load")
    load = Column(String)


class Atm(Model):
    __tablename__ = 'atm'
    id = Column(Integer, primary_key=True, autoincrement=True)
    address = Column(String)
    latitude = Column(String)
    longitude = Column(String)
    all_day = Column(Boolean)
    services = Column(String)