from fastapi import APIRouter, Depends, HTTPException
from controllers.controllers import QueueItemController, QueueController, ServiceController
from schemas.schema import QueueItemAdd, QueueItemGet, QueueItemDelete

router = APIRouter(prefix="/queues", tags=["queues"])


def calculate_queue_load(queue):
    '''
    Функция для расчёта времени ожидания последнего клиента в очереди
    '''
    res_time_in_q = 0
    for item in queue.items:
        i_time = item.service.time_to_complete
        res_time_in_q += int(i_time)
    return res_time_in_q


@router.post("/{salepoint_id}/items/")
def add_queue_item(queue_item: QueueItemAdd,
                   queue_items: QueueItemController = Depends(),
                   queues: QueueController = Depends(),
                   services: ServiceController = Depends()):
    '''
    Функция для добавления объекта элемента очереди в оптимальную очередь по salepoint_id и service_id
    '''
    service_opp = services.find(service_id).opportunities
    list_queues = queues.find_with_opp(salepoint_id, service_opp)
    if len(list_queues) == 0:
        raise HTTPException(status_code=404, detail="Очереди не найдена")

    res_queue = {"ids": [], "res_time": []}
    for queue in list_queues:
        res_queue["ids"].append((list_queues.index(queue), queue.id))
        res_queue["res_time"].append(calculate_queue_load(queue))

    min_time_ind = res_queue["res_time"].index(min(res_queue["res_time"]))
    queue_id = res_queue["ids"][min_time_ind][0]

    id = res_queue["ids"][min_time_ind][1]
    print(list_queues[queue_id])
    if list_queues[queue_id].items:
        ticket_number = str(int(list_queues[queue_id].items[-1].ticket_number) + 1)
    else:
        ticket_number = '1'

    item = queue_items.add(ticket_number, id, service_id)
    return item


@router.get("/{salepoint_id}/")
def get_queue_items(salepoint: QueueItemGet, queues: QueueController = Depends()):
    '''
    Функция для поиска объекта элемента очереди по salepoint_id
    '''
    queues_ = queues.find(salepoint_id)
    if len(queues_) == 0:
        raise HTTPException(status_code=404, detail="Очереди не найдены")

    for item in queues_:
        item.load_in_moment = calculate_queue_load(item)
    return queues_


@router.delete("/{queue_id}/items/{ticket_number}/")
def delete_queue_item(queue_item: QueueItemDelete, queue_items: QueueItemController = Depends()):
    '''
    Функция для удаления объекта элемента очереди по queue_id, ticket_number
    '''
    queue = queue_items.find_queue(queue_id)
    if queue is None:
        raise HTTPException(status_code=404, detail="Очередь не найдена")

    item = queue_items.find_queue_item(ticket_number)
    if item is None:
        raise HTTPException(status_code=404, detail="Элемент очереди не найден")

    item = queue_items.delete(item)

    return item
