from fastapi import APIRouter, Query
from database.database import get_all_product, get_all_purchase
from fastapi_pagination import Page, add_pagination, paginate
from typing import List

inventario = APIRouter()


@inventario.get('/api/inventario', response_model=Page[dict])
async def get_merged_data():
    products = await get_all_product()
    purchases = await get_all_purchase()
    merged_data = {}
    total_disponible = 0  

    for product in products:
        for purchase in purchases:
            if product.code == purchase.code:
                key = (product.name, product.code)
                if key not in merged_data:
                    merged_data[key] = {
                        'code': product.code,
                        'name': product.name,
                        'units': product.units,
                        'stock': purchase.stock,
                        'price_usd': purchase.price_usd,
                    }
                else:
                    merged_data[key]['stock'] += purchase.stock

    for data in merged_data.values():
        data['disponible'] = data['stock'] - data['units']
        total_disponible += data['disponible'] 
        
    paginated_data =  paginate(list(merged_data.values()))

    return (paginated_data)

add_pagination(inventario)

