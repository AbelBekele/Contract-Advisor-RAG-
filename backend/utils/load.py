import os
from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Milvus

loader = TextLoader("../data/Robinson_Advisory.txt", encoding="windows-1252")
index = VectorstoreIndexCreator().from_loaders([loader])

text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=1024, chunk_overlap=0
)
documents = loader.load_and_split()
docs = text_splitter.split_documents(documents)
embeddings = OpenAIEmbeddings()

vector_db = Milvus.from_documents(
    docs,
    embeddings,
    collection_name="contract",
    connection_args={"host": "192.168.137.236", "port": "19530", "database": "contract"},
)
