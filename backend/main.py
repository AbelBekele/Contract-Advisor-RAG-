from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from utils.main import ContractAdvisor
import asyncio
asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set this to the origin(s) you want to allow
    allow_credentials=True,
    allow_methods=["*"],  # Set this to the method(s) you want to allow
    allow_headers=["*"],  # Set this to the header(s) you want to allow
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

class Question(BaseModel):
    question: str

@app.post("/answer")
async def get_answer(request: Request, question: Question):
    advisor = ContractAdvisor(file_path="../data/Robinson_Advisory.txt", milvus_host="192.168.137.236", milvus_port="19530")
    answer = advisor.answer_question(question.question)
    return JSONResponse(content={"answer": answer['answer']})

