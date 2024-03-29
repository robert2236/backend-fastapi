from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from routes.task import task
from routes.user import user
from routes.client import client
from routes.purchase import purchase
from routes.brand import brand
from routes.product import product
from routes.devolution import devolution
from routes.join_inventario import inventario
from routes.tasa import tasa
from routes.form import form
from routes.supplier import supplier
from decouple import config
from routes.total import total



app = FastAPI()


print(config("FRONTEND_URL"))

origins = [
    config("FRONTEND_URL"),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(task)
app.include_router(user)
app.include_router(client)
app.include_router(purchase)
app.include_router(brand)
app.include_router(product)
app.include_router(inventario)
app.include_router(form)
app.include_router(devolution)
app.include_router(tasa)
app.include_router(supplier)
app.include_router(total)