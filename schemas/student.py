from pydantic import BaseModel

class registerStudent(BaseModel):
    name: str
    roll: int
    dob: int

class registerStudentRes(BaseModel):
    message: str

class getStudent(BaseModel):
    roll:int

class getStudentRes(BaseModel):
    name: str
    roll: int
    dob: int
    batch: str

class updateStudent(BaseModel):
    roll: int
    name: str | None = None
    new_roll: int | None = None
    dob: int | None = None

class updateStudentRes(BaseModel):
    message: str

class studentReportReq(BaseModel):
    roll: int

class subjectMarks(BaseModel):
    subject: str
    term: str
    marks: int

class studentReportRes(BaseModel):
    name: str
    batch: str
    results: list[subjectMarks]

class studentRankReq(BaseModel):
    roll: int
    batch: str

class studentRankRes(BaseModel):
    rank: int
    total_students: int
