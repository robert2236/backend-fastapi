from models.models import Task, UpdateTask
from models.user import User
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId



client = AsyncIOMotorClient('mongodb://localhost:27017')
database = client.taskdb
collection = database.tasks
user_collection = database.users


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