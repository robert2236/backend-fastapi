from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from routes.task import task
from routes.user import user
from routes.client import client
from routes.purchase import purchase
from decouple import config



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
