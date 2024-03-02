from llama_index.vector_stores import VectorStoreIndex, MilvusVectorStore
from llama_index.storage.storage_context import StorageContext

vector_store = MilvusVectorStore(dim=1536, overwrite=True)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)
