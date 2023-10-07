from typing import Optional
from pydantic import BaseModel, Field
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



class User(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id', default=None)
    username: str
    password: str

class UpdateUser(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None



class Config:
        orm_mode = True
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: str
        }
