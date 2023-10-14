import json
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import Atm, SalePoint, Load
from dependencies import get_db_settings

settings = get_db_settings()
engine = create_engine(
    f"postgresql://{settings.username}:{settings.password}@{settings.host}:{settings.port}/{settings.database}")

Session = sessionmaker(bind=engine)
session = Session()


# Заполнение таблицы с банкоматами
with open('atms.json', 'r', encoding='utf-8') as file:
    data = json.load(file)["atms"]

for record in data:
    salepoint = Atm(
        address=record["address"],
        latitude=str(record["latitude"]),
        longitude=str(record["longitude"]),
        all_day=record["allDay"],
        services=json.dumps(record["services"])
    )
    session.add(salepoint)

session.commit()


# Заполнение таблицы отделений
with open('offices.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

for record in data:
    serv = []
    while len(serv) < 5:
        i = random.randint(1, 7)
        if i not in serv:
            serv.append(i)
    salepoint = SalePoint(
        salepoint_name=record['salePointName'],
        address=record['address'],
        status=record['status'],
        rko=record['rko'],
        office_type=record['officeType'],
        salepoint_format=record['salePointFormat'],
        suo_availability=record['suoAvailability'],
        has_ramp=record['hasRamp'],
        latitude=record['latitude'],
        longitude=record['longitude'],
        metro_station=record['metroStation'],
        distance=record['distance'],
        kep=record['kep'],
        my_branch=record['myBranch'],
        open_hours=json.dumps({'for_leg': record['openHours']}),
        open_hours_individual=json.dumps({"for_phyth": record['openHoursIndividual']}),
        services=json.dumps(serv)
    )

    session.add(salepoint)

session.commit()




# Заполнение тестовой загруженности для дальнейшего расчёта загруженности
salepoints = session.query(SalePoint).all()

prob_loads = [[20, 40, 30, 50, 75, 55, 35], [15, 30, 37, 54, 70, 55, 30], [25, 40, 25, 40, 65, 65, 25]]
for salepoint in salepoints:
    open_hours_individual = json.loads(salepoint.open_hours_individual)
    load_data = []
    days = ["пн", "вт", "ср", "чт", "пт", "сб", "вс"]

    for index, day in enumerate(days):

        load_item = {"day": day, "time": []}

        if len(open_hours_individual["for_phyth"]) == 7:
            hours_data = open_hours_individual["for_phyth"][index]["hours"]

            if hours_data != "выходной":

                start_hour, end_hour = hours_data.split("-")
                from datetime import datetime, timedelta

                start = datetime.strptime(start_hour, '%H:%M')
                end = datetime.strptime(end_hour, '%H:%M')

                hour_list = []
                current_time = start
                while current_time <= end:
                    hour_list.append(current_time.strftime('%H:%M'))
                    current_time += timedelta(hours=1)

                for hours_range in hour_list:
                    load_item["time"].append({"hour": hours_range, "load": random.randint(20, 100)})
            print(load_item)
            load_data.append(load_item)

    load_json = json.dumps(load_data, ensure_ascii=False)
    load = Load(salepoint_id=salepoint.id, load=load_json)

    session.add(load)

session.commit()