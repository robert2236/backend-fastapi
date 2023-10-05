from fastapi import APIRouter, HTTPException
from database.database import (
    get_one_user_id,
    get_one_user,
    get_all_users,
    create_user,
    update_user,
    delete_user,
    get_login  
    )
from models.user import User, UpdateUser
import bcrypt
import jwt
import secrets
import traceback
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import JWTError
from fastapi_paginate import Page, add_pagination, paginate

def generar_token(usuario_id, secret_key):
    payload = {"usuario_id": usuario_id}
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return token

# Definir una clave secreta para firmar el token
SECRET_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJSb2xlIjoiQWRtaW4iLCJJc3N1ZXIiOiJJc3N1ZXIiLCJVc2VybmFtZSI6IkphdmFJblVzZSIsImV4cCI6MTY5NjQ1MTQ4NSwiaWF0IjoxNjk2NDUxNDg1fQ.dJP7LpEen9Ikv-FWj3z8kHWseYjLIxJ7QE9NLNGSQe4"
# Definir el algoritmo de encriptación
ALGORITHM = "HS256"
# Definir la duración del token (por ejemplo, 24 horas)
ACCESS_TOKEN_EXPIRE_MINUTES = 1440

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login")

# Función para generar el token de autenticación
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


user = APIRouter()

@user.get('/api/usuarios', response_model=Page[User])
async def get_users():
    response = await get_all_users()
    return paginate(response)

add_pagination(user)

@user.get('/api/usuarios/{id}', response_model=User)
async def get_task(id: str):
    response = await get_one_user_id(id)
    if response:
        return response
    raise HTTPException(404, f"There is no user with the id {id}")

@user.post("/api/user/login", response_model=User)
async def login_user(user: User):
    response = await get_login(user)
    if response:
        # Generar el token de autenticación
        access_token = create_access_token(
            data={"sub": user.username},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        # Autenticación exitosa
        return {
            "username": user.username,
            "password": user.password,
            "access_token": access_token,
            "token_type": "bearer"
        }
    else:
        # Autenticación fallida
        raise HTTPException(status_code=401, detail="Credenciales inválidas")


import traceback

@user.post("/api/usuarios", response_model=User)
async def save_user(user: User):
    try:
        userFound = await get_one_user(user.username)
        if userFound:
            raise HTTPException(409, "User already exists")
        
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
        user.password = hashed_password.decode('utf-8')
       
        response = await create_user(user.dict())
        print(response)
        
        if response:
            # Generate the authentication token
            secret_key = secrets.token_hex(32)
            token = generar_token(response.id, secret_key)
            print("token", token)
            return {"response": response, "token": token}
        
        raise HTTPException(400, "Something went wrong")
    
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(500, "Internal server error")

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
    