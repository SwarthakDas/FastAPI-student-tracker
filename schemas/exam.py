from pydantic import BaseModel

class addExam(BaseModel):
    term: str

class addExamRes(BaseModel):
    message: str

class getExam(BaseModel):
    code: str
    term: str

class getExamRes(BaseModel):
    code: str
    term: str
    marks: dict[str, int] | None = None

class updateMarksReq(BaseModel):
    code: str
    term: str
    roll: int
    marks: int

class updateMarksRes(BaseModel):
    message: str

class topperReq(BaseModel):
    code: str
    term: str

class topperRes(BaseModel):
    name: str
    roll: int
    marks: int

class compareReq(BaseModel):
    code: str
    term1: str
    term2: str

class compareRes(BaseModel):
    term1_total: int | None
    term2_total: int | None
    diff: int | None
