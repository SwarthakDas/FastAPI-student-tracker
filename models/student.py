from pydantic_settings import BaseSettings
from bson import ObjectId

class Student(BaseSettings):
    name: str
    roll: int
    dob: int
    batch: ObjectId