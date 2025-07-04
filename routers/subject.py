from fastapi import APIRouter, HTTPException, status
from database import db
from schemas.exam import getExamRes
from schemas.subject import addSubject, addSubjectRes, getSubject, getSubjectRes, subjectAverageReq, subjectAverageRes, updateSubject, updateSubjectRes
from models.subject import Subject

router = APIRouter(prefix="/subject", tags=['Subjects'])

@router.post("/add", response_model=addSubjectRes, status_code=status.HTTP_201_CREATED)
def add_subject(subject: addSubject, batch_name: str):
    batch = db["batches"].find_one({"name": batch_name})
    if not batch:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Batch not found")
    
    existing = db["subjects"].find_one({"code": subject.code})
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Subject with this code already exists")
    
    subject_obj = Subject(
        code=subject.code,
        name=subject.name,
        marks=subject.marks,
        exams=[]
    )
    db["subjects"].insert_one(subject_obj.model_dump())

    db["batches"].update_one(
        {"_id": batch["_id"]},
        {"$push": {"subjects": subject.code}}
    )

    return {
        "message": f"Subject '{subject.name}' added successfully",
    }

@router.post("/search", response_model=getSubjectRes, status_code=status.HTTP_200_OK)
def get_subject(subject: getSubject):
    sub = db["subjects"].find_one({"code": subject.code})
    if not sub:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subject not found")
    
    return {
        "code": sub["code"],
        "name": sub["name"],
        "marks": sub["marks"],
        "exams": sub.get("exams", [])
    }

@router.post("/get-all", response_model=list[getSubjectRes], status_code=status.HTTP_200_OK)
def get_all_subjects(batch_name: str):
    batch = db["batches"].find_one({"name": batch_name})
    if not batch:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Batch not found")

    subject_ids = batch.get("subjects", [])
    if not subject_ids:
        return []

    subjects = list(db["subjects"].find({"_id": {"$in": subject_ids}}))

    return [
        {
            "code": sub["code"],
            "name": sub["name"],
            "marks": sub["marks"],
            "exams": sub.get("exams", [])
        }
        for sub in subjects
    ]

@router.patch("/update", response_model=updateSubjectRes, status_code=status.HTTP_200_OK)
def update_subject(payload: updateSubject):
    sub = db["subjects"].find_one({"code": payload.code})
    if not sub:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subject not found")

    update_fields = {}
    if payload.name:
        update_fields["name"] = payload.name
    if payload.marks is not None:
        update_fields["marks"] = payload.marks

    if update_fields:
        db["subjects"].update_one({"_id": sub["_id"]}, {"$set": update_fields})

    return {"message": "Subject updated successfully"}


@router.post("/exams", response_model=list[getExamRes], status_code=status.HTTP_200_OK)
def subject_exams(req: getSubject):
    return router.dependency_overrides.get

@router.post("/average", response_model=subjectAverageRes, status_code=status.HTTP_200_OK)
def subject_average(req: subjectAverageReq):
    exams = list(db["exams"].find({"code": req.code}))
    if not exams:
        return {"average": None}

    total, count = 0, 0
    for ex in exams:
        total += sum(ex["marks"].values())
        count += len(ex["marks"])

    avg = round(total / count, 2) if count else None
    return {"average": avg}
