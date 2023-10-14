from datetime import datetime, timedelta
from typing import List

from fastapi import HTTPException, Header
from fastapi.params import Depends
from sqlalchemy.orm import Session, joinedload

from models.models import Queue, QueueItem, Service, SalePoint, User, Load, Atm
from dependencies import get_db


class SalePointController:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def all(self) -> List[SalePoint]:
        query = self.db.query(SalePoint)
        return query.options(joinedload(SalePoint.load)).all()

    def find(self, id: int) -> SalePoint:
        query = self.db.query(SalePoint)
        return query.options(joinedload(SalePoint.queues), joinedload(SalePoint.load)).filter(SalePoint.id == id).first()


class QueueController:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def find(self, salepoint_id: int) -> List[Queue]:
        query = self.db.query(Queue)
        return query.filter(Queue.salepoint_id == salepoint_id).all()

    def find_with_opp(self, salepoint_id: int, opportunities: str) -> List[Queue]:
        query = self.db.query(Queue)
        return query.filter(Queue.salepoint_id == salepoint_id, Queue.opportunities == opportunities).options(joinedload(Queue.items)).all()

    def add(self, id: int, opportunities: str) -> Queue:
        queue_ = Queue(salepoint_id=id, opportunities=opportunities)
        self.db.add(queue_)
        self.db.commit()
        self.db.refresh(queue_)
        return queue_


class QueueItemController:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def find_queue(self, id: int) -> Queue:
        query = self.db.query(Queue)
        return query.filter(Queue.salepoint_id == id).first()

    def find_queue_item(self, ticket_number: str) -> QueueItem:
        query = self.db.query(QueueItem)
        return query.filter(QueueItem.ticket_number == ticket_number).first()

    def add(self, ticket_number: str, queue_id: int, service_id: int) -> QueueItem:
        item = QueueItem(ticket_number=ticket_number, queue_id=queue_id, service_id=service_id)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, item: QueueItem) -> QueueItem:
        self.db.delete(item)
        self.db.commit()
        return item


class ServiceController:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def all(self, skip: int = 0, max: int = 100) -> List[Service]:
        query = self.db.query(Service)
        return query.offset(skip).limit(max).all()

    def find(self, id: id) -> Service:
        query = self.db.query(Service)
        return query.filter(Service.id == id).first()


class UserController:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_user_by_id(self, id: int) -> User:
        query = self.db.query(User)
        return query.filter(User.id == id).first()

    def get_user_by_name(self, full_name: str) -> User:
        query = self.db.query(User)
        return query.filter(User.full_name == full_name).first()

    def get_user_by_login(self, login: str) -> User:
        query = self.db.query(User)
        return query.filter(User.login == login).first()


class LoadsController:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def all(self) -> List[Load]:
        query = self.db.query(Load)
        return query.all()

    def find(self, id: int) -> Load:
        query = self.db.query(Load)
        return query.filter(Load.id == id).first()


class AtmController:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def all(self) -> List[Atm]:
        query = self.db.query(Atm)
        return query.all()

    def find(self, id: int) -> Atm:
        query = self.db.query(Atm)
        return query.filter(Atm.id == id).first()
