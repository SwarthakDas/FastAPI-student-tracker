from pydantic import BaseModel
from bson import ObjectId

class Student(BaseModel):
    name: str
    roll: int
    dob: int
    batch: str