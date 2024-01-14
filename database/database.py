from models.models import Task, UpdateTask
from models.user import User
from models.clients import Client
from models.suppliers import Supplier
from models.purchase import Purchase
from models.brands import Marca
from models.products import Product
from models.forms import Form
from models.devolution import Devolution
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import datetime
import bcrypt




client = AsyncIOMotorClient('mongodb+srv://inventario_cedrocolor:gNUISVh9mRjJY6gN@inventario.2zqyvib.mongodb.net/')
database = client.taskdb
collection = database.tasks
user_collection = database.users
client_collection = database.clients
supplier_collection = database.suppliers
purchase_collection = database.purchases
brand_collection = database.brands
products_collection = database.products
form_collection = database.forms
devolution_collection = database.devolutions
inventario_collection = database.inventario


#Funciones para obtener total de entradas, salidas, marcas, clientes

async def total_elementos_coleccion(nombre_coleccion: str):
    # Obtener la colección específica según el nombre proporcionado
    if nombre_coleccion == "purchase":
        coleccion = purchase_collection
    elif nombre_coleccion == "products":
        coleccion = products_collection
    elif nombre_coleccion == "brands":
        coleccion = brand_collection
    elif nombre_coleccion == "clients":
        coleccion = client_collection
    elif nombre_coleccion == "devolutions":
        coleccion = devolution_collection
    elif nombre_coleccion == "suppliers":
        coleccion = supplier_collection

    total = await coleccion.count_documents({})
    return total




async def get_one_task_id(id):
    task = await collection.find_one({"_id": ObjectId(id)})
    return task


async def get_one_task(title):
    task = await collection.find_one({"title": title})
    return task


async def get_all_tasks():
    tasks = []
    cursor = collection.find({})
    async for document in cursor:
        tasks.append(Task(**document))
    return tasks


async def create_task(task):
    new_task = await collection.insert_one(task)
    created_task = await collection.find_one({"_id": new_task.inserted_id})
    return created_task


async def update_task(id: str, data: UpdateTask):
    task = {k: v for k, v in data.dict().items() if v is not None}
    await collection.update_one({"_id": ObjectId(id)}, {"$set": task})
    document = await collection.find_one({"_id": ObjectId(id)})
    return document

async def delete_task(id):
    await collection.delete_one({"_id": ObjectId(id)})
    return True


# Funciones para el modelo de usuario


async def get_login(user):
    existing_user = await user_collection.find_one({"username": user.username})

    if existing_user:
        stored_password = existing_user['password']
        
        if bcrypt.checkpw(user.password.encode('utf-8'), stored_password.encode('utf-8')):
            return existing_user
    
    return None


async def get_one_user_id(id):
    user = await user_collection.find_one({"_id": ObjectId(id)})
    return user

async def get_one_user(username):
    user = await user_collection.find_one({"username": username})
    return user

async def get_all_users():
    users = []
    cursor = user_collection.find({})
    async for document in cursor:
        users.append(User(**document))
    return users

async def create_user(user):
    new_user = await user_collection.insert_one(user)
    created_user = await user_collection.find_one({"_id": new_user.inserted_id})
    return created_user

async def update_user(id: str, data):
    user = {k: v for k, v in data.dict().items() if v is not None}
    await user_collection.update_one({"_id": ObjectId(id)}, {"$set": user})
    document = await user_collection.find_one({"_id": ObjectId(id)})
    return document

async def delete_user(id):
    await user_collection.delete_one({"_id": ObjectId(id)})
    return True

# Funciones para el modelo de clientes

async def get_one_client_id(id):
    client = await client_collection.find_one({"_id": ObjectId(id)})
    return client

async def get_one_client(ci):
    client = await client_collection.find_one({"ci": ci})
    return client

async def get_all_clients():
    clients = []
    cursor = client_collection.find({})
    async for document in cursor:
        if isinstance(document.get("fecha", ""), str) and len(document.get("fecha", "")) > 0:
            try:
                # Parse the datetime string
                fecha = datetime.datetime.strptime(document["fecha"], "%Y-%m-%d %H:%M:%S")
            except ValueError:
                # Handle the case where the datetime string is not valid
                fecha = None
        else:
            fecha = None
        clients.append(Client(**document))
    return clients



async def create_client(user):
    new_client = await client_collection.insert_one(user)
    created_client = await client_collection.find_one({"_id": new_client.inserted_id})
    return created_client

async def update_client(id: str, data):
    client = {k: v for k, v in data.dict().items() if v is not None}
    await client_collection.update_one({"_id": ObjectId(id)}, {"$set": client})
    document = await client_collection.find_one({"_id": ObjectId(id)})
    return document

async def delete_client(id):
    await client_collection.delete_one({"_id": ObjectId(id)})
    return True

# Funciones para el modelo de proveedores

async def get_one_supplier_id(id):
    supplier = await supplier_collection.find_one({"_id": ObjectId(id)})
    return supplier

async def get_one_supplier(rif):
    supplier = await supplier_collection.find_one({"rif": rif})
    return supplier

async def get_all_supplier():
    clients = []
    cursor = supplier_collection.find({})
    async for document in cursor:
        if isinstance(document.get("fecha", ""), str) and len(document.get("fecha", "")) > 0:
            try:
                # Parse the datetime string
                fecha = datetime.datetime.strptime(document["fecha"], "%Y-%m-%d %H:%M:%S")
            except ValueError:
                # Handle the case where the datetime string is not valid
                fecha = None
        else:
            fecha = None
        clients.append(Supplier(**document))
    return clients

async def create_supplier(user):
    new_supplier = await supplier_collection.insert_one(user)
    created_supplier = await supplier_collection.find_one({"_id": new_supplier.inserted_id})
    return created_supplier

async def update_supplier(id: str, data):
    supplier = {k: v for k, v in data.dict().items() if v is not None}
    await supplier_collection.update_one({"_id": ObjectId(id)}, {"$set": supplier})
    document = await supplier_collection.find_one({"_id": ObjectId(id)})
    return document

async def delete_supplier(id):
    await supplier_collection.delete_one({"_id": ObjectId(id)})
    return True


# Funciones para la gestion de compras

async def get_one_purchase_id(id):
    purchase = await purchase_collection.find_one({"_id": ObjectId(id)})
    return purchase

async def get_one_purchase(code):
    client = await purchase_collection.find_one({"code": code})
    return client


async def get_all_purchase():
    purchases = []
    cursor = purchase_collection.find({})
    async for document in cursor:
        if isinstance(document.get("fecha", ""), str) and len(document.get("fecha", "")) > 0:
            try:
                # Parse the datetime string
                fecha = datetime.datetime.strptime(document["fecha"], "%Y-%m-%d %H:%M:%S")
            except ValueError:
                # Handle the case where the datetime string is not valid
                fecha = None
        else:
            fecha = None
        purchases.append(Purchase(**document))
    return purchases

async def update_purchase(id: str, data):
    purchase = {k: v for k, v in data.dict().items() if v is not None}
    await purchase_collection.update_one({"_id": ObjectId(id)}, {"$set": purchase})
    document = await purchase_collection.find_one({"_id": ObjectId(id)})
    return document   

async def create_purchase(purchase):
    new_purchase = await purchase_collection.insert_one(purchase)
    created_purchase = await purchase_collection.find_one({"_id": new_purchase.inserted_id})
    return created_purchase

async def delete_purchase(id):
    await purchase_collection.delete_one({"_id": ObjectId(id)})
    return True

# Funciones para la gestion de marca

async def get_one_brand_id(id):
    brand = await brand_collection.find_one({"_id": ObjectId(id)})
    return brand

async def get_one_brand(name):
    client = await brand_collection.find_one({"name": name})
    return client

async def get_all_brand():
    brands = []
    cursor = brand_collection.find({})
    async for document in cursor:
        if isinstance(document.get("fecha", ""), str) and len(document.get("fecha", "")) > 0:
            try:
                # Parse the datetime string
                fecha = datetime.datetime.strptime(document["fecha"], "%Y-%m-%d %H:%M:%S")
            except ValueError:
                # Handle the case where the datetime string is not valid
                fecha = None
        else:
            fecha = None
        brands.append(Marca(**document))
    return brands

async def create_brand(brand):
    new_brand = await brand_collection.insert_one(brand)
    created_brand = await brand_collection.find_one({"_id": new_brand.inserted_id})
    return created_brand

async def update_brand(id: str, data):
    brand = {k: v for k, v in data.dict().items() if v is not None}
    await brand_collection.update_one({"_id": ObjectId(id)}, {"$set": brand})
    document = await brand_collection.find_one({"_id": ObjectId(id)})
    return document


async def delete_brand(id):
    await brand_collection.delete_one({"_id": ObjectId(id)})
    return True


# Funciones para la gestion de productos

async def get_one_product_id(id):
    brand = await products_collection.find_one({"_id": ObjectId(id)})
    return brand

async def get_one_product(code):
    client = await products_collection.find_one({"code": code})
    return client

async def get_all_product():
    products = []
    cursor = products_collection.find({})
    async for document in cursor:
        if isinstance(document.get("fecha", ""), str) and len(document.get("fecha", "")) > 0:
            try:
                # Parse the datetime string
                fecha = datetime.datetime.strptime(document["fecha"], "%Y-%m-%d %H:%M:%S")
            except ValueError:
                # Handle the case where the datetime string is not valid
                fecha = None
        else:
            fecha = None
        products.append(Product(**document))
    return products

async def create_product(product):
    new_product = await products_collection.insert_one(product)
    created_product = await products_collection.find_one({"_id": new_product.inserted_id})
    return created_product

async def update_product(id: str, data):
    product = {k: v for k, v in data.dict().items() if v is not None}
    await products_collection.update_one({"_id": ObjectId(id)}, {"$set": product})
    document = await products_collection.find_one({"_id": ObjectId(id)})
    return document


async def delete_product(id):
    await products_collection.delete_one({"_id": ObjectId(id)})
    return True

# Funciones para las devoluciones
async def get_one_devolution_id(id):
    brand = await devolution_collection.find_one({"_id": ObjectId(id)})
    return brand

async def get_one_devolution(cod):
    devolution = await devolution_collection.find_one({"cod": cod})
    return devolution

async def get_all_devolution():
    devolutions = []
    cursor = devolution_collection.find({})
    async for document in cursor:
        if isinstance(document.get("fecha", ""), str) and len(document.get("fecha", "")) > 0:
            try:
                # Parse the datetime string
                fecha = datetime.datetime.strptime(document["fecha"], "%Y-%m-%d %H:%M:%S")
            except ValueError:
                # Handle the case where the datetime string is not valid
                fecha = None
        else:
            fecha = None
        devolutions.append(Devolution(**document))
    return devolutions

async def create_devolution(devolution):
    new_devolution = await devolution_collection.insert_one(devolution)
    created_devolution = await devolution_collection.find_one({"_id": new_devolution.inserted_id})
    return created_devolution


async def delete_devolution(id):
    await devolution_collection.delete_one({"_id": ObjectId(id)})
    return True


# Funciones para el formulario

async def get_one_form_id(id):
    form = await form_collection.find_one({"_id": ObjectId(id)})
    return form

async def get_one_form(comment):
    form = await form_collection.find_one({"comment": comment})
    return form


async def get_all_form():
    forms = []
    cursor = form_collection.find({})
    async for document in cursor:
        if isinstance(document.get("fecha", ""), str) and len(document.get("fecha", "")) > 0:
            try:
                # Parse the datetime string
                fecha = datetime.datetime.strptime(document["fecha"], "%Y-%m-%d %H:%M:%S")
            except ValueError:
                # Handle the case where the datetime string is not valid
                fecha = None
        else:
            fecha = None
        forms.append(Form(**document))

    return forms

async def create_form(form):
    new_form = await form_collection.insert_one(form)
    created_form = await form_collection.find_one({"_id": new_form.inserted_id})
    return created_form

async def delete_form(id):
    await form_collection.delete_one({"_id": ObjectId(id)})
    return True

#Obtener total en numero de comentarios

async def total_comentarios():
    total = await form_collection.count_documents({})
    return total
