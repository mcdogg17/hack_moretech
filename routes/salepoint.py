from fastapi import APIRouter, Depends, HTTPException

from recsys.recommended_system import select_suitable
from controllers.controllers import SalePointController, QueueController
from schemas.schema import SalePointFind

router = APIRouter(prefix="/salepoints", tags=["salepoints"])


@router.get("/")
def list_salepoints(salepoints: SalePointController = Depends()):
    '''
    Функция для получения списка всех объектов отделений
    '''
    db_salepoints = salepoints.all()

    return db_salepoints


@router.post("/find_salepoint")
def get_salepoint(salepoint: SalePointFind,
                  salepoints: SalePointController = Depends(),
                  queues: QueueController = Depends()):
    '''
    Функция для поиск списка оптимальных объектов отделений
    по расстоянию, времени ожидания, рабочему времени и т.д.
    '''
    db_salepoints = select_suitable(float(salepoint.latitude),
                                    float(salepoint.longitude),
                                    salepoint.service_id,
                                    salepoint.range_km, salepoints)

    if not db_salepoints:
        raise HTTPException(
            status_code=404,
            detail="Отделения не найдены"
        )

    return db_salepoints


@router.post("/find_salepoint_by_id")
def get_salepoint_by_id(id: int, salepoints: SalePointController = Depends()):
    '''
    Функция для поиска объекта отделения по id
    '''
    db_salepoints = salepoints.find(id)

    if not db_salepoints:
        raise HTTPException(
            status_code=404,
            detail="Отделение не найдены"
        )

    return db_salepoints