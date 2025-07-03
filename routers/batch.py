from fastapi import APIRouter,HTTPException,status
from database import db
from schemas.batch import registerBatch,registerBatchRes,getBatch,getBatchRes

router=APIRouter(prefix="/batch",tags=['Batches'])

@router.post("/register",response_model=registerBatchRes,status_code=status.HTTP_201_CREATED)
def register_batch(batch: registerBatch):
    
    batch_dict={
        "name":batch.name,
        "strength": batch.strength,
        "subjects":None
    }

    db["batches"].insert_one(batch_dict)
    
    return {
        "message": f"Batch '{batch.name}' registered successfully",
    }

@router.post("/search",response_model=getBatchRes,status_code=status.HTTP_200_OK)
def get_batch(batch:getBatch):
    bat=db["batches"].find_one({"name":batch.name})
    if not bat:
        raise HTTPException(status_code=404,detail="Batch not found")
    return{
        "name": bat["name"],
        "strength": bat["strength"],
        "subjects": bat["subjects"],
    }

@router.post("/get-all",response_model=list[getBatchRes],status_code=status.HTTP_200_OK)
def get_all_batches():
    batches=db["batches"].find()
    if not batches:
        raise HTTPException(status_code=404,detail="Batch not found")

    return[{
        "name": batch["name"],
        "strength": batch["strength"],
        "subjects": batch["subjects"],
    } for batch in batches
    ]