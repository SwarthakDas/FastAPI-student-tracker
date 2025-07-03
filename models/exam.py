from pydantic_settings import BaseSettings
from bson import ObjectId

class Exam(BaseSettings):
    term: str
    marks: dict[ObjectId,int]