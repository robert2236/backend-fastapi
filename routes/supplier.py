from fastapi import APIRouter, HTTPException, Query
from database.database import (
    get_one_supplier_id,
    get_one_supplier,
    get_all_supplier,
    create_supplier, 
    update_supplier,
    delete_supplier 
    )
from models.suppliers import Supplier, UpdateSupplier
from fastapi_pagination import Page, add_pagination, paginate

supplier = APIRouter()


@supplier.get('/api/suppliers', response_model=Page[Supplier])
async def get_suppliers(email: str = Query(None)):
    response = await get_all_supplier()
    if email:
        filtered_email = [supplier for supplier in response if supplier.email == email]
        if filtered_email:
             return paginate(filtered_email)
        raise HTTPException(404, f"There are no clients asociate with the email {email}")
    return paginate(response)

add_pagination(supplier)

@supplier.get('/api/suppliers/{rif}', response_model=Supplier)
async def get_supplier_by_rif(rif: str):
    response = await get_one_supplier(rif)
    if response:
        return response
    raise HTTPException(404, f"There is no client with the id {rif}")

@supplier.post('/api/suppliers', response_model=Supplier)
async def save_supplier(supplier: Supplier):
    findClient = await get_one_supplier(supplier.rif)
    if findClient:
        raise HTTPException(status_code=409, detail="El proveedor ya se encuentra registrado")
    response = await create_supplier(supplier.dict())
    print(response)
    if response:
        return response
    raise HTTPException(400, "Something went wrong")

@supplier.put('/api/suppliers/{id}', response_model=Supplier)
async def put_supplier(id: str, data: UpdateSupplier):
    response = await update_supplier(id, data)
    if response:
        return response
    raise HTTPException(404, f"There is no client with the id {id}")

@supplier.delete('/api/suppliers/{id}')
async def remove_client(id: str):
    response = await delete_supplier(id)
    if response:
        return "delete suppliuer successfully "
    raise HTTPException(404, f"There is no user with the id {id}")


