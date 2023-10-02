from fastapi import APIRouter
from pymongo import MongoClient

inventario = APIRouter()
client = MongoClient("mongodb://localhost:27017")
db = client["taskdb"]

@inventario.get("/join_data/{code}")
async def join_data(code: int):
    try:
        client.server_info()
        product = db["products"].find_one({"code": code})
        purchase = db["purchases"].find_one({"cod": code})
        if not product or not purchase:
            return {"message": "No se encontraron datos para el código proporcionado"}

        return {
            "stock_producto": product["stock"],
            "unidades_compra": purchase["units"]
        }
    except Exception as e:
        return {"message": f"Error al conectar a la base de datos: {str(e)}"}