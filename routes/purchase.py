from fastapi import APIRouter, HTTPException, Query
from database.database import (
    get_one_purchase_id,
     get_one_client,
    get_all_purchase,
    create_purchase,
    delete_purchase  
    )
from models.purchase import Purchase, UpdatePurchase

purchase = APIRouter()



@purchase.get('/api/purchases')
async def get_purchase(category: str = Query(None)):
    response = await get_all_purchase()
    if category:
        filtered_purchases = [purchase for purchase in response if purchase.category == category]
        if filtered_purchases:
            return filtered_purchases
        raise HTTPException(404, f"There are no purchases in the category {category}")
    return response



@purchase.get('/api/purchases/{id}', response_model=Purchase)
async def get_client_by_id(id: str):
    response = await get_one_purchase_id(id)
    if response:
        return response
    raise HTTPException(404, f"There is no client with the id {id}")

@purchase.post('/api/purchases', response_model=Purchase)
async def save_purchase(purchase: Purchase):
    findPurchase = await  get_one_client(purchase.cod)
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