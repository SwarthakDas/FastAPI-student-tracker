from pydantic import BaseModel

class registerBatch(BaseModel):
    pass

class getBatch(BaseModel):
    name: str
    strength: int
    subjects: str | None
