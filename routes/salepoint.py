from fastapi import APIRouter, Depends, HTTPException

from recsys.recommended_system import select_suitable
from controllers.controllers import SalePointController, QueueController
from routes.queue import get_queue_items
from schemas.schema import SalePointFind, SalePointFindById, QueueCreate

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
def get_salepoint_by_id(salepoint: SalePointFindById, salepoints: SalePointController = Depends()):
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


@router.post("/{salepoint_id}/queues/")
def create_queue(queue: QueueCreate,
                 salepoints: SalePointController = Depends(),
                 queues: QueueController = Depends()):
    '''
    Функция для создания объекта очереди по salepoint_id
    '''
    salepoint = salepoints.find(salepoint_id)
    if salepoint is None:
        raise HTTPException(status_code=404, detail="Отделение не найдены")
    queue = queues.add(salepoint_id, opportunities)
    return queue
