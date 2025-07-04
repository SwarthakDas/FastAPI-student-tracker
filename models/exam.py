from pydantic import BaseModel

class Exam(BaseModel):
    code: str
    term: str
    marks: dict[int,int]
    