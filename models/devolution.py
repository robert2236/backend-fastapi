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
    
class Devolution(BaseModel):
      id: Optional[PyObjectId] = Field(alias='_id', default=None) 
      cod: int
      name: str   
      observation: str
      units: int

class Config:
        orm_mode = True
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: str
        }
