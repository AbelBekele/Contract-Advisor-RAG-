import sys
from langchain.prompts import PromptTemplate
from typing import List
from langchain.chat_models import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader
from pydantic import BaseModel, Field
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema import StrOutputParser
from pymilvus import Milvus, DataType
from datetime import date
from dotenv import load_dotenv
import json
import os

load_dotenv()

TOKEN = os.getenv("Milvus_token")
CLUSTER_ENDPOINT = os.getenv("Milvus_HOST")

class ScienceDirectDocument(BaseModel):
    paper_title: str
    abstract: str
    date: date
    keywords: List[str]
    doi: str
    topics: List[str] = Field(default_factory=list, description="Topics covered by the document. Examples include Services, Time Tracking, No Conflicts, Term, Termination, Compensation, etc.")

def process_and_classify_document(filename):
    loader = PyPDFLoader(filename)
    pages = loader.load_and_split()

    ids = [str(i) for i in range(1, len(pages) + 1)]

    embeddings = OpenAIEmbeddings()
    vectors = embeddings.generate_embeddings(pages)  # Generate embeddings from pages

    # Replace uri and token with your own
    client = Milvus(
        uri=CLUSTER_ENDPOINT,  # Cluster endpoint obtained from the console
        token=TOKEN  # API key or a colon-separated cluster username and password
    )

    # Create a collection
    client.create_collection(
        collection_name="contract_advisor",
        dimension=768
    )
    
    client.insert(collection_name, vectors, ids)
    retriever = client.search(collection_name, vectors, params={"metric_type": "L2", "params": {"nprobe": 10}}, limit=10)

    schema = ScienceDirectDocument.schema()

    template = """Use the following pieces of context to accurately classify the documents based on the schema passed. Output should follow the pattern defined in schema.
    No verbose should be present. Output should follow the pattern defined in schema and the output should be in json format only so that it can be directly used with json.loads():
    {context}
    schema: {schema}
    """
    rag_prompt_custom = PromptTemplate.from_template(template)
    llm = ChatOpenAI(model_name="gpt-4", temperature=0)

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {"context": retriever | format_docs, "schema": RunnablePassthrough()}
        | rag_prompt_custom
        | llm
        | StrOutputParser()
    )
    output = json.loads(rag_chain.invoke(str(schema)))
    client.drop_collection(collection_name)  # Delete the collection after use
    return output

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python your_script_name.py <pdf_filename>")
        sys.exit(1)

    filename = sys.argv[1]  # Get the filename from the command-line argument
    json_output = process_and_classify_document(filename=filename)
    print(json.dumps(json_output, indent=4))  # Print the output in a pretty format
