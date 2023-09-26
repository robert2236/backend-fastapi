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
    
class Client(BaseModel):
      id: Optional[PyObjectId] = Field(alias='_id', default=None)
      name: str
      ci: int
      email: str
      phone: int
      fecha: datetime.datetime = datetime.datetime.now()

    

class UpdateClient(BaseModel):
      name: Optional[str] = None
      ci: Optional[str] = None
      email: Optional[str] = None
      phone: Optional[int] = None

class Config:
        orm_mode = True
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: str
        }
