from models.models import Task, UpdateTask
from models.user import User
from models.clients import Client
from models.Suppliers import Suppliers
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import datetime



client = AsyncIOMotorClient('mongodb://localhost:27017')
database = client.taskdb
collection = database.tasks
user_collection = database.users
client_collection = database.clients
supplier_collection = database.suppliers


async def get_one_task_id(id):
    task = await collection.find_one({"_id": ObjectId(id)})
    return task


async def get_one_task(title):
    task = await collection.find_one({"title": title})
    return task


async def get_all_tasks():
    tasks = []
    cursor = collection.find({})
    async for document in cursor:
        tasks.append(Task(**document))
    return tasks


async def create_task(task):
    new_task = await collection.insert_one(task)
    created_task = await collection.find_one({"_id": new_task.inserted_id})
    return created_task


async def update_task(id: str, data: UpdateTask):
    task = {k: v for k, v in data.dict().items() if v is not None}
    await collection.update_one({"_id": ObjectId(id)}, {"$set": task})
    document = await collection.find_one({"_id": ObjectId(id)})
    return document

async def delete_task(id):
    await collection.delete_one({"_id": ObjectId(id)})
    return True


# Funciones para el modelo de usuario

async def get_one_user_id(id):
    user = await user_collection.find_one({"_id": ObjectId(id)})
    return user

async def get_one_user(username):
    user = await user_collection.find_one({"username": username})
    return user

async def get_all_users():
    users = []
    cursor = user_collection.find({})
    async for document in cursor:
        users.append(User(**document))
    return users

async def create_user(user):
    new_user = await user_collection.insert_one(user)
    created_user = await user_collection.find_one({"_id": new_user.inserted_id})
    return created_user

async def update_user(id: str, data):
    user = {k: v for k, v in data.dict().items() if v is not None}
    await user_collection.update_one({"_id": ObjectId(id)}, {"$set": user})
    document = await user_collection.find_one({"_id": ObjectId(id)})
    return document

async def delete_user(id):
    await user_collection.delete_one({"_id": ObjectId(id)})
    return True

# Funciones para el modelo de clientes

async def get_one_client_id(id):
    client = await client_collection.find_one({"_id": ObjectId(id)})
    return client

async def get_one_client(ci):
    client = await client_collection.find_one({"ci": ci})
    return client

async def get_all_clients():
    clients = []
    cursor = client_collection.find({})
    async for document in cursor:
        if isinstance(document.get("fecha", ""), str) and len(document.get("fecha", "")) > 0:
            try:
                # Parse the datetime string
                fecha = datetime.datetime.strptime(document["fecha"], "%Y-%m-%d %H:%M:%S")
            except ValueError:
                # Handle the case where the datetime string is not valid
                fecha = None
        else:
            fecha = None
        clients.append(Client(**document))
    return clients



async def create_client(user):
    new_client = await client_collection.insert_one(user)
    created_client = await client_collection.find_one({"_id": new_client.inserted_id})
    return created_client

async def update_client(id: str, data):
    client = {k: v for k, v in data.dict().items() if v is not None}
    await client_collection.update_one({"_id": ObjectId(id)}, {"$set": client})
    document = await client_collection.find_one({"_id": ObjectId(id)})
    return document

async def delete_client(id):
    await client_collection.delete_one({"_id": ObjectId(id)})
    return True

# Funciones para el modelo de proveedores

async def get_one_supplier_id(id):
    supplier = await supplier_collection.find_one({"_id": ObjectId(id)})
    return supplier

async def get_all_supplier():
    clients = []
    cursor = supplier_collection.find({})
    async for document in cursor:
        if isinstance(document.get("fecha", ""), str) and len(document.get("fecha", "")) > 0:
            try:
                # Parse the datetime string
                fecha = datetime.datetime.strptime(document["fecha"], "%Y-%m-%d %H:%M:%S")
            except ValueError:
                # Handle the case where the datetime string is not valid
                fecha = None
        else:
            fecha = None
        clients.append(Suppliers(**document))
    return clients

async def create_client(user):
    new_supplier = await supplier_collection.insert_one(user)
    created_supplier = await supplier_collection.find_one({"_id": new_supplier.inserted_id})
    return created_supplier

