import os
import openai
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain_community.vectorstores import Milvus
from langchain.text_splitter import CharacterTextSplitter
from langchain.memory import ConversationBufferWindowMemory
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQAWithSourcesChain
import warnings
warnings.filterwarnings('ignore')

# Load environment variables from .env file
load_dotenv()
# IMPORTANT: Remember to create a .env variable containing: OPENAI_API_KEY=sk-xyz where xyz is your key

class ContractAdvisor:
    def __init__(self, file_path, milvus_host, milvus_port):
        self.file_path = file_path
        self.milvus_host = milvus_host
        self.milvus_port = milvus_port
        self.api_key = os.environ.get("OPENAI_API_KEY")
        openai.api_key = self.api_key
        self.loader = TextLoader(self.file_path, encoding="windows-1252")
        self.index = VectorstoreIndexCreator().from_loaders([self.loader])
        self.text_splitter = CharacterTextSplitter.from_tiktoken_encoder(chunk_size=1024, chunk_overlap=0)
        self.docs = self.text_splitter.split_documents(self.loader.load_and_split())
        self.embeddings = OpenAIEmbeddings()
        self.vector_db = Milvus.from_documents(self.docs, self.embeddings, collection_name="contract", connection_args={"host": self.milvus_host, "port": self.milvus_port, "database": "contract"})
        self.prompt_template = '''
        You are a contract advisor expert with immense knowledge and experience in the field.
        Answer my questions based on your knowledge and our older conversation. Do not make up answers.
        If you do not know the answer to a question, just say "I don't know".

        {context}

        Given the following conversation and a follow up question, answer the question.

        {chat_history}

        question: {question}
        '''
        self.PROMPT = PromptTemplate(template=self.prompt_template, input_variables=["context", "chat_history", "question"])
        self.memory = ConversationBufferWindowMemory(k=2, memory_key="chat_history", max_len=50, return_messages=True, output_key='answer')
        self.llm = ChatOpenAI(temperature=0)
        llm = ChatOpenAI(temperature=0)
        self.chain = RetrievalQAWithSourcesChain.from_chain_type(llm=llm, chain_type="map_rerank", retriever=self.vector_db.as_retriever(), memory=self.memory)

    def answer_question(self, question):
        return self.chain(self.PROMPT.format(question=question, chat_history=self.memory.chat_memory.messages, context=self.vector_db.similarity_search_with_score(question)))
