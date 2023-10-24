from typing import Optional
from pydantic import BaseModel, Field, validator
from bson import ObjectId
from datetime import datetime



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
    code: int
    category: str
    supplier: str
    price_usd: float
    price_bs: float
    stock: float
    total: float
    datePurchase: Optional[datetime]
    dateExpiration: Optional[datetime]

class UpdatePurchase(BaseModel):
    name: Optional[str] = None
    code: Optional[int] = None
    category: Optional[bool] = None
    supplier: Optional[bool] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    
    

class Config:
        orm_mode = True
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: str
        }

