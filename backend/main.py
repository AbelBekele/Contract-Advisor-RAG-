import nest_asyncio
import os
from fastapi import FastAPI
from utils.main import ContractAdvisor
import asyncio
asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/answer")
def read_item(question: str):
    advisor = ContractAdvisor(file_path="../data/Robinson_Advisory.txt", milvus_host="192.168.137.236", milvus_port="19530")
    answer = advisor.answer_question(question)
    return {"answer": answer['answer']}
