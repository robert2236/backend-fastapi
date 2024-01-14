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
from fastapi_pagination import Page, add_pagination, paginate


product = APIRouter()


@product.get('/api/products', response_model=Page[Product])
async def get_products(code: int = Query(None)):
    response = await get_all_product()
    
    if code:
        filtered_products = [product for product in response if product.code == code]
        if filtered_products:
            return paginate(filtered_products)
        raise HTTPException(404, f"There are no products associated with the code {code}")
    
    return paginate(response)

add_pagination(product)

@product.get('/api/products/total')
async def get_total_price_stocks():
    products = await get_all_product()
    total_price = sum(product.price for product in products)
    total_stocks = sum(product.units for product in products)
    return {'total_price': total_price, 'total_stocks': total_stocks}

@product.get('/api/products/date')
async def get_products():
    products = await get_all_product()
    product_data = []
    for product in products:
        product_data.append({
            'units': product.units,
            'dateProducts': product.dateProducts
        })
    return product_data

@product.get('/api/products/{id}', response_model=Product)
async def get_products_by_id(id: str):
    response = await get_one_product_id(id)
    if response:
        return response
    raise HTTPException(404, f"There is no products with the id {id}")

@product.post('/api/products', response_model=Product)
async def save_product(product: Product):
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




