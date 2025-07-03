from pydantic import BaseModel

class registerBatchRes(BaseModel):
    message: str

class registerBatch(BaseModel):
    name: str
    strength: int

class getBatch(BaseModel):
    name: str
    
class getBatchRes(BaseModel):
    name: str
    strength: int
    subjects: str | None
