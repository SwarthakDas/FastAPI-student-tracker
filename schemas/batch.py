from pydantic import BaseModel

class registerBatchRes(BaseModel):
    message: str

class registerBatch(BaseModel):
    name: str

class getBatch(BaseModel):
    name: str
    
class getBatchRes(BaseModel):
    name: str
    strength: int
    subjects: list | None = None

class BatchExamsReq(BaseModel):
    name: str

class BatchExamsRes(BaseModel):
    exams: list[str]