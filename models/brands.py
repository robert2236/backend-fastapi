from typing import Optional
from pydantic import BaseModel, Field, validator
from bson import ObjectId



class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, values, **kwargs):
     if not ObjectId.is_valid(v):
        raise ValueError('Invalid ObjectId')
     return str(v)
    
class Marca(BaseModel):
        id: Optional[PyObjectId] = Field(alias='_id', default=None)
        name: str
        description: str
        owner: str
        category: str
        logo: str

class UpdateMarca(BaseModel):
     name: Optional[str] = None
     description: Optional[str] = None
     owner: Optional[str] = None
     category: Optional[str] = None
     logo: Optional[str] = None

class Config:
        orm_mode = True
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: str
        }

        