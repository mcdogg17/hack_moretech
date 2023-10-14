from fastapi import APIRouter, Depends, HTTPException
from controllers.controllers import AtmController


router = APIRouter(prefix="/atms", tags=["atms"])


@router.get("/")
def list_loads(atms: AtmController = Depends()):
    '''
    Функция для получения списка всех объектов банкомата
    '''
    db_atms = atms.all()
    if not db_atms:
        raise HTTPException(
            status_code=404,
            detail="Банкомат не найден"
        )
    return db_atms


@router.post("/find_atm")
def get_service(id: int, atms: AtmController = Depends()):
    '''
    Функция для поиска объекта банкомата по id
    '''
    db_atms = atms.find(id=id)

    if not db_atms:
        raise HTTPException(
            status_code=404,
            detail="Банкомат не найден"
        )

    return db_atms
