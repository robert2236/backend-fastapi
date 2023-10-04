from fastapi import APIRouter, HTTPException
from database.database import (
    get_one_devolution_id,
    get_one_devolution,
    get_all_devolution,
    create_devolution,
    delete_devolution  
    )
from models.devolution import Devolution
from fastapi_paginate import Page, add_pagination, paginate

devolution = APIRouter()

@devolution.get('/api/devolution')
async def get_devolution():
    response = await get_all_devolution()
    return response

@devolution.get('/api/devolution/{id}', response_model=Devolution)
async def get_devolution_by_id(id: str):
    response = await get_one_devolution_id(id)
    if response:
        return response
    raise HTTPException(404, f"There is no products with the id {id}")

@devolution.post('/api/devolution', response_model=Devolution)
async def save_product(devolution: Devolution):
    findDevolution = await get_one_devolution(devolution.cod)
    if findDevolution:
        raise HTTPException(409, "Devolution already exists")

    response = await create_devolution(devolution.dict())
    print(response)
    if response:
        return response
    raise HTTPException(400, "Something went wrong")


@devolution.delete('/api/devolution/{id}')
async def remove_purchase(id: str):
    response = await delete_devolution(id)
    if response:
        return "Successfully deleted devolution"
    raise HTTPException(404, f"There is no devolution with the id {id}")