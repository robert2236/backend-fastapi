from fastapi import APIRouter, HTTPException
from database.database import (
    get_one_user_id,
    get_one_user,
    get_all_users,
    create_user,
    update_user,
    delete_user  
    )
from models.user import User, UpdateUser
import bcrypt
import jwt
import secrets

def generar_token(usuario_id, secret_key):
    payload = {"usuario_id": usuario_id}
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return token


user = APIRouter()

@user.get('/api/usuarios')
async def get_users():
    response = await get_all_users()
    return response

@user.get('/api/usuarios/{id}', response_model=User)
async def get_task(id: str):
    response = await get_one_user_id(id)
    if response:
        return response
    raise HTTPException(404, f"There is no user with the id {id}")

@user.post("/api/usuarios", response_model=User)
async def save_user(user: User):
    userFound = await get_one_user(user.username)
    if userFound:
        raise HTTPException(409, "user already exists")
    
    
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    user.password = hashed_password.decode('utf-8')
   
    response = await create_user(user.dict())
    print(response)
    if response:
        # Generate the authentication token
        secret_key = secrets.token_hex(32)
        token = generar_token(response.id, secret_key)
        return {"response": response, "token": token}
        
    raise HTTPException(400, "Something went wrong")

@user.put('/api/usuarios/{id}', response_model=User)
async def put_user(id: str, data: UpdateUser):
    response = await update_user(id, data)
    if response:
        return response
    raise HTTPException(404, f"There is no user with the id {id}")

@user.delete('/api/usuarios/{id}')
async def remove_user(id: str):
    response = await delete_user(id)
    if response:
        return "Successfully deleted task"
    raise HTTPException(404, f"There is no user with the id {id}")
    