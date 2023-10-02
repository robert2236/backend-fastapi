from fastapi import APIRouter, HTTPException
from database.database import (
    get_one_client_id,
    get_one_client,
    get_all_clients,
    create_client,
    update_client,
    delete_client  
    )
from models.clients import Client, UpdateClient

client = APIRouter()

@client.get('/api/clients')
async def get_clients():
    response = await get_all_clients()
    return response

@client.get('/api/clients/{id}', response_model=Client)
async def get_client_by_id(id: str):
    response = await get_one_client_id(id)
    if response:
        return response
    raise HTTPException(404, f"There is no client with the id {id}")

@client.post('/api/clients', response_model=Client)
async def save_client(client: Client):
    findClient = await get_one_client(client.ci)
    if findClient:
        raise HTTPException(409, "Client already exists")

    response = await create_client(client.dict())
    print(response)
    if response:
        return response
    raise HTTPException(400, "Something went wrong")

@client.put('/api/clients/{id}', response_model=Client)
async def put_client(id: str, data: UpdateClient):
    response = await update_client(id, data)
    if response:
        return response
    raise HTTPException(404, f"There is no client with the id {id}")

@client.delete('/api/clients/{id}')
async def remove_client(id: str):
    response = await delete_client(id)
    if response:
        return "Successfully client"
    raise HTTPException(404, f"There is no user with the id {id}")
    