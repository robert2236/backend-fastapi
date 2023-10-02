from typing import Optional
from pydantic import BaseModel, Field, validator
from bson import ObjectId
import datetime


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, values, **kwargs):
     if not ObjectId.is_valid(v):
        raise ValueError('Invalid ObjectId')
     return str(v)


class Purchase(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id', default=None)
    name: str
    cod: int
    category: str
    supplier: str
    price: float
    stock: int
    stock_min: int
    stock_max: int
    datePurchase: datetime.datetime = datetime.datetime.now()
    dateExpiration: datetime.datetime = datetime.datetime.now()

class UpdatePurchase(BaseModel):
    name: Optional[str] = None
    cod: Optional[int] = None
    category: Optional[bool] = None
    supplier: Optional[bool] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    stock_min: Optional[int] = None
    stock_max: Optional[int] = None
    

class Config:
        orm_mode = True
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: str
        }

