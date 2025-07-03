from pydantic import BaseModel

class registerExam(BaseModel):
    pass

class getExam(BaseModel):
    batch: str
    subject:str
    term: str
    marks: dict[str,int]
