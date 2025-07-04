from fastapi import APIRouter,HTTPException,status
from database import db
from schemas.batch import registerBatch,registerBatchRes,getBatch,getBatchRes,BatchExamsReq,BatchExamsRes
from models.batch import Batch

router=APIRouter(prefix="/batch",tags=['Batches'])

@router.post("/register",response_model=registerBatchRes,status_code=status.HTTP_201_CREATED)
def register_batch(batch: registerBatch):
    existing = db["batches"].find_one({"name": batch.name})
    if existing:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Batch with this name already exists")
    batch_obj=Batch(
        name=batch.name,
        strength=0,
        subjects=[]
    )

    db["batches"].insert_one(batch_obj.model_dump())
    
    return {
        "message": f"Batch '{batch.name}' registered successfully",
    }

@router.post("/search",response_model=getBatchRes,status_code=status.HTTP_200_OK)
def get_batch(batch:getBatch):
    bat=db["batches"].find_one({"name":batch.name})
    if not bat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Batch not found")
    return{
        "name": bat["name"],
        "strength": bat["strength"],
        "subjects": bat["subjects"],
    }

@router.post("/get-all",response_model=list[getBatchRes],status_code=status.HTTP_200_OK)
def get_all_batches():
    batches=list(db["batches"].find())
    return[{
        "name": batch["name"],
        "strength": batch["strength"],
        "subjects": batch["subjects"],
    } for batch in batches
    ]

@router.post("/exams", response_model=BatchExamsRes, status_code=status.HTTP_200_OK)
def list_batch_exams(req: BatchExamsReq):
    batch = db["batches"].find_one({"name": req.name})
    if not batch:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Batch not found")

    subject_ids = batch.get("subjects", [])
    if not subject_ids:
        return {"exams": []}

    subjects = db["subjects"].find({"_id": {"$in": subject_ids}})
    exam_ids = []
    for sub in subjects:
        exam_ids.extend(sub.get("exams", []))

    exams = db["exams"].find({"_id": {"$in": exam_ids}})
    exam_strings = [f"{ex['code']} | {ex['term']}" for ex in exams]

    return {"exams": exam_strings}
