import json
from typing import List

from controllers.controllers import SalePointController, QueueController
from fastapi import Depends
from geopy.distance import great_circle, geodesic
from models.models import SalePoint
from routes.queue import get_queue_items 


def select_suitable(latitude: float, longitude: float,
                    service_id: int, range_km: int = 3,
                    salepoints: SalePointController = Depends(),
                    queues: QueueController = Depends() ) -> List[SalePoint]:
    '''
    Функция (вспомогательная) для расчёта списка оптимальных отделений
    '''
    result_branches = []
    list_of_branches = salepoints.all()

    for departament in list_of_branches:
        latitude_dep, longitude_dep = departament.latitude, departament.longitude
        services_dep = json.loads(departament.services)
        if great_circle((latitude, longitude), (latitude_dep, longitude_dep)).kilometers < range_km \
                and service_id in services_dep:
            distance = geodesic((latitude, longitude), (latitude_dep, longitude_dep)).kilometers
            departament.distance_to_salepoint = distance
            result_branches.append(departament)
   
    return sorted(result_branches, key=lambda salepoint: (salepoint.distance_to_salepoint,
           min(get_queue_items(salepoint.id, queues), key=lambda queue: queue.load_in_moment)))[:3]

    
    