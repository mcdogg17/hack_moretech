<br />
<div align="center">
  <a href="https://github.com/mcdogg17/hack_moretech">
  <img src="https://bankreg.ru/bankr.ru/wp-content/uploads/2017/07/vtb-bank.png" alt="Logo" width="130" height="80">  
</a>

<h3 align="center">Backend</h3>

  <p align="center">
    Репозиторий серверной части приложения по нахождению
оптимального отделения для Банка "ВТБ".
    <br>
  </p>
</div>

## Other project repositories:
* <a href=https://github.com/DanonAno/HackVTBOpenMaps>iOS-приложение</a>
* <a href=https://www.figma.com/file/6VFcVmFslHYfpFMRNC2PmX/Хакатон-ВТБ>Figma</a>


## About the project

Сервис предоставляет возможности взаимодействия клиента с приложением.
Также благодаря нашему приложению можно получить оптимальное по всем параметрам
отделение банка. Учитываются такие параметры, как расстояние, время в пути, время в очереди.
На стороне backend'a реализованы все необходимые функции для работы с базой данных. Сервис позволяет
пользователю записаться в электронную очередь в удобное отделение банка. Для 
безопасности были написаны тесты системы по методам SAST, DAST, SQLMap.

Сервис полностью задокументирован. Swagger-документация доступна по следуещему адресу: 

```88.218.169.17:88/docs/```


### Stack

* Python
* FastAPI
* Geopy
* Pydantic
* SQLAlchemy
* PostgreSQL
* Docker
* Docker Compose


## Installation

Для простой установки и использования проект завернут в контейнер и вместе с
базой данных оркестрируется через Docker Compose.

Для установки используйте следующие команды:

* Склонируйте репозиторий
* Выполните следующие команды:

```docker-compose build```

```docker-compose up```

```docker exec -it <your_container_name> bash```

```python3 filling/fill.py```

Приложение будет доступно на всех доступных адресах и порту 88. (`localhost:88` or `0.0.0.0:88`)

## P.S.

Для упрощения проверки нашего сервиса, мы развернули его на сервере и он доступен
по адресу `88.218.169.17:88`. Также актуальная документация `88.218.169.17:88/docs`.
