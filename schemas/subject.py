from pydantic import BaseModel

class registerSubject(BaseModel):
    pass

class getSubject(BaseModel):
    batch:str
    code: str
    marks: int
    exams: str | None
