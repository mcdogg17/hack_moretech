from pydantic import BaseModel


class SalePointFind(BaseModel):
    latitude: str
    longitude: str
    service_id: int
    range_km: int = 3


class SalePointFindById(BaseModel):
    id: int


class SalePointLoad(BaseModel):
    salepoint_id: int


class QueueCreate(BaseModel):
    salepoint_id: int
    opportunities: str


class UserLogin(BaseModel):
    username: str
    password: str


class QueueItemAdd(BaseModel):
    salepoint_id: int
    service_id: int


class QueueItemGet(BaseModel):
    salepoint_id: int


class QueueItemDelete(BaseModel):
    queue_id: int
    ticket_number: str


class Service(BaseModel):
    id: int


class Atm(BaseModel):
    id: int

