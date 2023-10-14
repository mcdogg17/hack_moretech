from fastapi import APIRouter, Depends, HTTPException
from controllers.controllers import ServiceController

router = APIRouter(prefix="/services", tags=["services"])


@router.get("/")
def list_services(services: ServiceController = Depends()):
    '''
    Функция для получения списка всех объектов услуг
    '''
    db_services = services.all(skip=skip, max=max)
    if not db_services:
        raise HTTPException(
            status_code=404,
            detail="Услуги не найдена"
        )
    return db_services


@router.get("/find_service")
def get_service(id: int, services: ServiceController = Depends()):
    '''
    Функция для поиска объекта услуги по id
    '''
    db_services = services.find(id=id)

    if not db_services:
        raise HTTPException(
            status_code=404,
            detail="Услуга не найдена"
        )

    return db_services
