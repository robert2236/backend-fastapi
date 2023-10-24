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
    
class Product(BaseModel):
   id: Optional[PyObjectId] = Field(alias='_id', default=None)
   code: int
   name: str
   description: str
   price_usd: float
   price_bs: float
   units: float
   total: float
   dateProducts: datetime.datetime = datetime.datetime.now()

class UpdateProduct(BaseModel):
    name: Optional[str] = None
    code: Optional[int] = None
    description: Optional[str] = None
    price: Optional[int] = None
    units: Optional[int] = None

class Config:
        orm_mode = True
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: str
        }