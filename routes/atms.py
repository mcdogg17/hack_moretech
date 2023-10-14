from fastapi import APIRouter, Depends, HTTPException
from controllers.controllers import AtmController


router = APIRouter(prefix="/atms", tags=["atms"])


@router.get("/")
def list_loads(atms: AtmController = Depends()):
    db_salepoints = atms.all()
    return db_salepoints


@router.post("/find_atm")
def get_service(id: int, atms: AtmController = Depends()):
    db_services = atms.find(id=id)

    if not db_services:
        raise HTTPException(
            status_code=404,
            detail="Atm not found"
        )

    return db_services
