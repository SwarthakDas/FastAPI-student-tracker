from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import student,batch,exam,subject

origins=[]
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(batch.router)
app.include_router(student.router)
app.include_router(subject.router)
app.include_router(exam.router)