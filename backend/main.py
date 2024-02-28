from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from utils.main import ContractAdvisor
import asyncio
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Question(BaseModel):
    question: str

@app.post("/answer")
async def get_answer(request: Request, question: Question):
    advisor = ContractAdvisor(file_path="../data/Robinson_Advisory.txt", milvus_host="192.168.137.236", milvus_port="19530")
    answer = advisor.answer_question(question.question)
    return answer['answer']

@app.post("/response")
async def response_endpoint(request: Request, question: Question):
    answer_response = await get_answer(request, question)
    return JSONResponse(content={"response": answer_response})

@app.post("/uploadfile")
async def create_upload_file(file: UploadFile = File(...)):
    with open(f"../data/{file.filename}", "wb") as buffer:
        buffer.write(await file.read())
    return {"filename": file.filename}