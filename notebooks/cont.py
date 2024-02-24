import openai
import numpy as np
import pandas as pd
import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA, ConversationalRetrievalChain,RetrievalQAWithSourcesChain
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.chains.question_answering import load_qa_chain
from langchain.document_loaders import UnstructuredFileLoader
from langchain.prompts import PromptTemplate

from langchain.document_loaders import UnstructuredExcelLoader
loader = UnstructuredFileLoader("../Test.pdf", mode="elements")
documents = loader.load()


from langchain.docstore.document import Document
import json
 
# Opening JSON file
with open('Customer_profile.json', 'r') as openfile:
# Reading from json file
    json_object = json.load(openfile)
 
cName=json_object['Customer_Name']
cState=json_object['Customer_State']
cGen=json_object['Customer_Gender']

cProfile = "Customer's Name is "+cName+"\nCustomer's Resident State is "+cState+"\nCustomer's Gender is "+cGen
print(cProfile)
# cProfileDoc =  Document(page_content=cProfile, metadata={"source": "customerProfile.json"})
# documents.insert(0, cProfileDoc)

prompt_template = """You are a Chat customer support agent.
        Address the customer as Dear Mr. or Miss. depending on customer's gender followed by Customer's First Name.
        Use the following customer related information (delimited by <cp></cp>) context (delimited by <ctx></ctx>) and the chat history (delimited by <hs></hs>) to answer the question at the end:
        If you don't know the answer, just say that you don't know, don't try to make up an answer.
        Below are the details of the customer:\n 
        <cp>
        Customer's Name: {Customer_Name}
        Customer's Resident State: {Customer_State}
        Customer's Gender: {Customer_Gender}
        </cp>
        <ctx>
        {context}
        </ctx>
        <hs>
        {history}
        </hs>
        Question: {query}
        Answer: """

#print(prompt_template.format(cProfile))

PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["history","context", "query","Customer_Name","Customer_State","Customer_Gender"]
)


text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)
#embeddings = OpenAIEmbeddings()
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
vectorDB = Chroma.from_documents(texts,embeddings)

from langchain.memory import ConversationBufferMemory
memory = ConversationBufferMemory(memory_key="history",input_key="query" ,output_key='answer',return_messages=True)


qa = RetrievalQA.from_chain_type(
    llm=OpenAI(),
    chain_type='stuff',
    retriever=vectorDB.as_retriever(),
    verbose=True,
    chain_type_kwargs={
        "verbose": True,
        "prompt": PROMPT,
        "memory": memory
    }
)

qa({"query": "who's the client's friend?","Customer_Gender":"Male","Customer_State":"New York","Customer_Name":"Aaron"})