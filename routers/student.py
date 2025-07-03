from fastapi import APIRouter,HTTPException,status
from database import db
from schemas.student import registerStudentRes,registerStudent,getStudentRes,getStudent

router=APIRouter(prefix="/student",tags=['Students'])

@router.post("/register",response_model=registerStudentRes,status_code=status.HTTP_201_CREATED)
def register_student(student: registerStudent, batch_name: str):
    batch=db["batches"].find_one({"name":batch_name})
    if not batch:
        raise HTTPException(status_code=404,detail="Batch not found")
    
    student_dict={
        "name":student.name,
        "roll": student.roll,
        "dob":student.dob,
        "batch":batch["_id"]
    }

    db["students"].insert_one(student_dict)
    
    return {
        "message": f"Student '{student.name}' registered successfully",
    }
# batch needs to be updated

@router.post("/search",response_model=getStudentRes,status_code=status.HTTP_200_OK)
def get_student(student:getStudent):
    stu=db["students"].find_one({"roll":student.roll})
    if not stu:
        raise HTTPException(status_code=404,detail="Student not found")
    batch=db["batches"].find_one({"_id":stu["batch"]})
    return{
        "name": stu["name"],
        "roll": stu["roll"],
        "dob": stu["dob"],
        "batch": batch["name"]
    }

@router.post("/get-all",response_model=list[getStudentRes],status_code=status.HTTP_200_OK)
def get_student(batch_name: str):
    batch=db["batches"].find_one({"name":batch_name})
    if not batch:
        raise HTTPException(status_code=404,detail="Batch not found")
    
    students=list(db["students"].find({"batch":batch["_id"]}))

    return[{
        "name": stu["name"],
        "roll": stu["roll"],
        "dob": stu["dob"],
        "batch": batch["name"]
    } for stu in students
    ]