from pydantic import BaseModel

class addSubject(BaseModel):
    code: str
    name: str
    marks: int

class addSubjectRes(BaseModel):
    message: str

class getSubject(BaseModel):
    code:str

class getSubjectRes(BaseModel):
    code: str
    name:str
    marks: int
    exams: list|None = None

class updateSubject(BaseModel):
    code: str
    name: str | None = None
    marks: int | None = None

class updateSubjectRes(BaseModel):
    message: str

class subjectAverageReq(BaseModel):
    code: str

class subjectAverageRes(BaseModel):
    average: float | None
