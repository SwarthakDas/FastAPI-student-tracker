from fastapi import APIRouter, HTTPException, status
from database import db
from schemas.exam import addExam, addExamRes, compareReq, compareRes, getExam, getExamRes, topperReq, topperRes, updateMarksReq, updateMarksRes
from models.exam import Exam

router = APIRouter(prefix="/exam", tags=["Exams"])

@router.post("/add", response_model=addExamRes, status_code=status.HTTP_201_CREATED)
def add_exam(exam: addExam, subject_code: str):
    subject = db["subjects"].find_one({"code": subject_code})
    if not subject:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subject not found")

    existing_exam = db["exams"].find_one({"code": subject_code, "term": exam.term})
    if existing_exam:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Exam with this term already exists for this subject")

    exam_obj = Exam(
        code=subject_code,
        term=exam.term,
        marks={}
    )
    result = db["exams"].insert_one(exam_obj.model_dump())

    db["subjects"].update_one(
        {"code": subject_code},
        {"$push": {"exams": result.inserted_id}}
    )

    return {
        "message": f"Exam '{exam.term}' added to subject '{subject_code}'"
    }

@router.post("/search", response_model=getExamRes, status_code=status.HTTP_200_OK)
def get_exam(exam: getExam):
    ex = db["exams"].find_one({"code": exam.code, "term": exam.term})
    if not ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exam not found")

    student_marks = {}
    for roll, marks in ex.get("marks", {}).items():
        student = db["students"].find_one({"roll": roll})
        name = student["name"] if student else f"Roll {roll}"
        student_marks[name] = marks

    return {
        "code": ex["code"],
        "term": ex["term"],
        "marks": student_marks
    }

@router.post("/get-all", response_model=list[getExamRes], status_code=status.HTTP_200_OK)
def get_all_exams(subject_code: str):
    exams = list(db["exams"].find({"code": subject_code}))
    if not exams:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No exams found for this subject")

    response = []
    for ex in exams:
        student_marks = {}
        for roll, marks in ex.get("marks", {}).items():
            student = db["students"].find_one({"roll": roll})
            name = student["name"] if student else f"Roll {roll}"
            student_marks[name] = marks

        response.append({
            "code": ex["code"],
            "term": ex["term"],
            "marks": student_marks
        })

    return response

@router.patch("/update-marks", response_model=updateMarksRes, status_code=status.HTTP_200_OK)
def update_marks(req: updateMarksReq):
    ex = db["exams"].find_one({"code": req.code, "term": req.term})
    if not ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exam not found")

    db["exams"].update_one(
        {"_id": ex["_id"]},
        {"$set": {f"marks.{req.roll}": req.marks}}
    )
    return {"message": "Marks updated"}


@router.post("/students-marks", response_model=getExamRes, status_code=status.HTTP_200_OK)
def students_marks(req: getExam):
    return get_exam(req)


@router.post("/topper", response_model=topperRes, status_code=status.HTTP_200_OK)
def exam_topper(req: topperReq):
    ex = db["exams"].find_one({"code": req.code, "term": req.term})
    if not ex or not ex.get("marks"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exam not found or no marks")

    roll, marks = max(ex["marks"].items(), key=lambda x: x[1])
    roll_int = int(roll)
    student = db["students"].find_one({"roll": roll_int})
    name = student["name"] if student else f"Roll {roll_int}"

    return {"name": name, "roll": roll_int, "marks": marks}

@router.post("/compare", response_model=compareRes, status_code=status.HTTP_200_OK)
def compare_exams(req: compareReq):
    ex1 = db["exams"].find_one({"code": req.code, "term": req.term1})
    ex2 = db["exams"].find_one({"code": req.code, "term": req.term2})

    total1 = sum(ex1["marks"].values()) if ex1 and ex1.get("marks") else None
    total2 = sum(ex2["marks"].values()) if ex2 and ex2.get("marks") else None

    diff = total2 - total1 if (total1 is not None and total2 is not None) else None
    return {"term1_total": total1, "term2_total": total2, "diff": diff}

