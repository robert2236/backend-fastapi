from fastapi import APIRouter, HTTPException, Request
from database.database import (
    get_one_form_id,
    get_one_form,
    get_all_form,
    create_form,
    delete_form  
    )
from models.forms import Form
from fastapi_paginate import Page, add_pagination, paginate

form = APIRouter()

@form.get('/api/forms/', response_model=Page[Form])
async def get_form():
    response = await get_all_form()  
    return paginate(response)

add_pagination(form)

@form.get('/api/forms/{id}', response_model=Form)
async def get_form_by_id(id: str):
    response = await get_one_form_id(id)
    if response:
        return response
    raise HTTPException(404, f"There is no form with the id {id}")

@form.post('/api/forms', response_model=Form)
async def save_form(form: Form):
    findClient = await get_one_form(form.comment)
    if findClient:
        raise HTTPException(409, "Form already exists")

    response = await create_form(form.dict())
    print(response)
    if response:
        return response
    raise HTTPException(400, "Something went wrong")

@form.delete('/api/forms/{id}')
async def remove_client(id: str):
    response = await delete_form(id)
    if response:
        return "Successfully client"
    raise HTTPException(404, f"There is no form with the id {id}")
    