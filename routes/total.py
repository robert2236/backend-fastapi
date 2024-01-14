from fastapi import APIRouter, HTTPException, Query
from database.database import (
    total_elementos_coleccion
    )


total = APIRouter()

@total.get("/api/total-elementos")
async def obtener_total_elementos():
    total_purchase = await total_elementos_coleccion("purchase")
    total_products = await total_elementos_coleccion("products")
    total_brands = await total_elementos_coleccion("brands")
    total_clients = await total_elementos_coleccion("clients")
    total_devolutions = await total_elementos_coleccion("devolutions")
    total_supliers = await total_elementos_coleccion("suppliers")

    return {
        "total_purchase": total_purchase,
        "total_products": total_products,
        "total_brands": total_brands,
        "total_clients": total_clients,
        "total_devolutions": total_devolutions,
        "total_suppliers": total_supliers
    }