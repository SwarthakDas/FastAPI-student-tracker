from fastapi import APIRouter,HTTPException,status
from database import db
from schemas.student import registerStudentRes,registerStudent,getStudentRes,getStudent, studentRankReq, studentRankRes, studentReportReq, studentReportRes, subjectMarks, updateStudent, updateStudentRes
from models.student import Student

router=APIRouter(prefix="/student",tags=['Students'])

@router.post("/register",response_model=registerStudentRes,status_code=status.HTTP_201_CREATED)
def register_student(student: registerStudent, batch_name: str):
    batch=db["batches"].find_one({"name":batch_name})
    if not batch:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Batch not found")
    
    existing = db["students"].find_one({"roll": student.roll})
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Student with this roll already exists")
    
    student_obj = Student(
        name=student.name,
        roll=student.roll,
        dob=student.dob,
        batch=batch["name"]
    )
    db["students"].insert_one(student_obj.model_dump())

    db["batches"].update_one(
        {"_id": batch["_id"]},
        {"$inc": {"strength": 1}}
    )
    
    return {
        "message": f"Student '{student.name}' registered successfully",
    }

@router.post("/search",response_model=getStudentRes,status_code=status.HTTP_200_OK)
def get_student(student:getStudent):
    stu=db["students"].find_one({"roll":student.roll})
    if not stu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Student not found")
    return{
        "name": stu["name"],
        "roll": stu["roll"],
        "dob": stu["dob"],
        "batch": stu["batch"]
    }

@router.post("/get-all",response_model=list[getStudentRes],status_code=status.HTTP_200_OK)
def get_all_students(batch_name: str):
    batch=db["batches"].find_one({"name":batch_name})
    if not batch:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Batch not found")
    
    students=list(db["students"].find({"batch":batch["name"]}))

    return[{
        "name": stu["name"],
        "roll": stu["roll"],
        "dob": stu["dob"],
        "batch": batch_name
    } for stu in students
    ]

@router.patch("/update", response_model=updateStudentRes, status_code=status.HTTP_200_OK)
def update_student(req: updateStudent):
    stu = db["students"].find_one({"roll": req.roll})
    if not stu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    update_fields = {}
    if req.name:
        update_fields["name"] = req.name
    if req.new_roll:
        if db["students"].find_one({"roll": req.new_roll}):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Roll already exists")
        update_fields["roll"] = req.new_roll
    if req.dob:
        update_fields["dob"] = req.dob

    if update_fields:
        db["students"].update_one({"_id": stu["_id"]}, {"$set": update_fields})

    return {"message": "Student updated successfully"}


@router.post("/report", response_model=studentReportRes, status_code=status.HTTP_200_OK)
def student_report(req: studentReportReq):
    stu = db["students"].find_one({"roll": req.roll})
    if not stu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    results: list[subjectMarks] = []
    exams = db["exams"].find({"marks."+str(req.roll): {"$exists": True}})
    for ex in exams:
        mark = ex["marks"][str(req.roll)]
        results.append(subjectMarks(subject=ex["code"], term=ex["term"], marks=mark))

    return {
        "name": stu["name"],
        "batch": stu["batch"],
        "results": results
    }


@router.post("/rank", response_model=studentRankRes, status_code=status.HTTP_200_OK)
def student_rank(req: studentRankReq):
    students = list(db["students"].find({"batch": req.batch}))
    if not students:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Batch not found")

    totals: dict[int, int] = {s["roll"]: 0 for s in students}
    exams = db["exams"].find({"marks": {"$ne": {}}})
    for ex in exams:
        for roll, mark in ex["marks"].items():
            if roll in totals:
                totals[roll] += mark

    sorted_totals = sorted(totals.items(), key=lambda x: x[1], reverse=True)
    rank = next((idx + 1 for idx, (r, _) in enumerate(sorted_totals) if r == req.roll), None)
    if rank is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student has no marks")

    return {"rank": rank, "total_students": len(students)}
