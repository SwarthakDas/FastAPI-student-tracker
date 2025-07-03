from pydantic import BaseModel

class registerStudentRes(BaseModel):
    message: str

class registerStudent(BaseModel):
    name: str
    roll: int
    dob: int

class getStudent(BaseModel):
    roll:str

class getStudentRes(BaseModel):
    name: str
    roll: int
    dob: int
    batch: str
