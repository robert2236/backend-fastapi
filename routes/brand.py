from fastapi import APIRouter, HTTPException, Query
from database.database import (
    get_one_brand_id,
     get_one_brand,
    get_all_brand,
    create_brand,
    delete_brand,
    update_brand  
    )
from models.brands import Marca, UpdateMarca
from fastapi_pagination import Page, add_pagination, paginate

brand = APIRouter()

@brand.get('/api/brands', response_model=Page[Marca])
async def get_clients():
    response = await get_all_brand()
    return paginate(response)

add_pagination(brand)

@brand.get('/api/brands/{id}', response_model=Marca)
async def get_brand_by_id(id: str):
    response = await get_one_brand_id(id)
    if response:
        return response
    raise HTTPException(404, f"There is no brand with the id {id}")

@brand.post('/api/brands', response_model=Marca)
async def save_brandt(brand: Marca):
    findClient = await get_one_brand(brand.name)
    if findClient:
        raise HTTPException(409, "Brand already exists")

    response = await create_brand(brand.dict())
    print(response)
    if response:
        return response
    raise HTTPException(400, "Something went wrong")


@brand.put('/api/brands/{id}', response_model=Marca)
async def put_brand(id: str, data: UpdateMarca):
    response = await update_brand(id, data)
    if response:
        return response
    raise HTTPException(404, f"There is no brand with the id {id}")



@brand.delete('/api/brands/{id}')
async def remove_brand(id: str):
    response = await delete_brand(id)
    if response:
        return "Successfully deleted task"
    raise HTTPException(404, f"There is no user with the id {id}")

