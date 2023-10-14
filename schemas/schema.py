from pydantic import BaseModel


class SalePointFind(BaseModel):
    latitude: str
    longitude: str
    service_id: int
    range_km: int = 3
