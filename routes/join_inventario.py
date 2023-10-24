from fastapi import APIRouter, HTTPException, Query
from database.database import (
    get_all_product,
    get_all_purchase
      
    )
from models.clients import Client, UpdateClient
from fastapi_pagination import Page, add_pagination, paginate

inventario = APIRouter()


@inventario.get('/api/inventario')
async def get_merged_data():
    products = await get_all_product()
    purchases = await get_all_purchase()

    merged_data = []

    for product in products:
        for purchase in purchases:
            if product.code == purchase.code:
                merged_data.append({
                    'code': product.code,
                    'name': product.name,
                    'units': product.units,
                    'stock': purchase.stock
                })
                break

    return merged_data
    