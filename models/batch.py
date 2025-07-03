from pydantic_settings import BaseSettings
from bson import ObjectId

class Batch(BaseSettings):
    name: str
    strength: int
    subjects: ObjectId
