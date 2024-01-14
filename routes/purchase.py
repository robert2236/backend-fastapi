from fastapi import APIRouter, HTTPException, Query
from database.database import (
    get_one_purchase_id,
     get_one_client,
    get_all_purchase,
    update_purchase,
    create_purchase,
    delete_purchase  
    )
from models.purchase import Purchase, UpdatePurchase
from fastapi_pagination import Page, add_pagination, paginate

purchase = APIRouter()



@purchase.get('/api/purchases', response_model=Page[Purchase])
async def get_purchase(code: int = Query(0)):
    response = await get_all_purchase()
    if code:
        filtered_products = [product for product in response if product.code == code]
        if filtered_products:
            return paginate(filtered_products)
        raise HTTPException(404, f"There are no products associated with the code {code}")
    return paginate(response)

add_pagination(purchase)

@purchase.get('/api/purchases/{id}', response_model=Purchase)
async def get_purchase_id(id: str):
    response = await get_one_purchase_id(id)
    if response:
        return response
    raise HTTPException(404, f"There is no user with the id {id}")

@purchase.get('/api/purchases/total')
async def get_total_price_stocks():
    purchases = await get_all_purchase()
    total_purchase = sum(product.price for product in purchases)
    total_stocks = sum(product.stock for product in purchases)
    return {'total_price': total_purchase, 'total_stocks': total_stocks}

@purchase.get('/api/purchases/date')
async def get_purchase():
    purchases = await get_all_purchase()
    purchases_data = []
    for purchase in purchases:
        purchases_data.append({
            'stock': purchase.stock,
            'dateProducts': purchase.datePurchase
        })
    return purchases_data



@purchase.post('/api/purchases', response_model=Purchase)
async def save_purchase(purchase: Purchase):
    findPurchase = await  get_one_client(purchase.code)
    if findPurchase:
        raise HTTPException(409, "Purchase already exists")

    response = await create_purchase(purchase.dict())
    print(response)
    if response:
        return response
    raise HTTPException(400, "Something went wrong")


@purchase.delete('/api/purchases/{id}')
async def remove_purchase(id: str):
    response = await delete_purchase(id)
    if response:
        return "Successfully deleted task"
    raise HTTPException(404, f"There is no user with the id {id}")