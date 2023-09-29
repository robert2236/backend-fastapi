from fastapi import APIRouter, HTTPException, Query
from database.database import (
    get_one_product_id,
     get_one_product,
    get_all_product,
    create_product,
    delete_product,
    update_product  
    )
from models.products import Product, UpdateProduct


product = APIRouter()


@product.get('/api/products')
async def get_products():
    response = await get_all_product()
    return response

@product.get('/api/products/{id}', response_model=Product)
async def get_products_by_id(id: str):
    response = await get_one_product_id(id)
    if response:
        return response
    raise HTTPException(404, f"There is no products with the id {id}")

@product.post('/api/products', response_model=Product)
async def save_product(product: Product):
    findClient = await get_one_product(product.name)
    if findClient:
        raise HTTPException(409, "Products already exists")

    response = await create_product(product.dict())
    print(response)
    if response:
        return response
    raise HTTPException(400, "Something went wrong")


@product.put('/api/products/{id}', response_model=Product)
async def put_brand(id: str, data: UpdateProduct):
    response = await update_product(id, data)
    if response:
        return response
    raise HTTPException(404, f"There is no brand with the id {id}")



@product.delete('/api/products/{id}')
async def remove_brand(id: str):
    response = await delete_product(id)
    if response:
        return "Successfully deleted task"
    raise HTTPException(404, f"There is no user with the id {id}")
