from pydantic_settings import BaseSettings
from bson import ObjectId

class Subject(BaseSettings):
    code: str
    marks: int
    exams: ObjectId