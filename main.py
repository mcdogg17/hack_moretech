from fastapi import FastAPI
from routes import queue, service, salepoint, user, atms
from database import Model, engine

Model.metadata.create_all(bind=engine)
app = FastAPI()

# Подключение всех роутов
app.include_router(queue.router)
app.include_router(service.router)
app.include_router(salepoint.router)
app.include_router(user.router)
app.include_router(atms.router)