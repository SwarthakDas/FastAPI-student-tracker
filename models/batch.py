from pydantic import BaseModel,Field

class Batch(BaseModel):
    name: str
    strength: int
    subjects: list = Field(default_factory=list)
