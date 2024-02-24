from langchain.memory import ConversationBufferWindowMemory
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQAWithSourcesChain
from load import vector_db

memory = ConversationBufferWindowMemory(
                                    k=2,
                                    memory_key="chat_history",
                                    max_len=50,
                                    return_messages=True,
                                    output_key='answer'
                                )

llm = ChatOpenAI(temperature=0)
chain = RetrievalQAWithSourcesChain.from_chain_type(
                        llm,
                        chain_type="map_rerank",
                        retriever=vector_db.as_retriever(),
                        memory=memory,
                    )
