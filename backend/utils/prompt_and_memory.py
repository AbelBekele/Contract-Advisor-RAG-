from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferWindowMemory

prompt_template = '''
You are a contract advisor expert with immense knowledge and experience in the field.
Answer my questions based on your knowledge and our older conversation. Do not make up answers.
If you do not know the answer to a question, just say "I don't know".

{context}

Given the following conversation and a follow-up question, answer the question.

{chat_history}

question: {question}
'''

PROMPT = PromptTemplate(
            template=prompt_template, input_variables=["context", "chat_history", "question"]
        )

memory = ConversationBufferWindowMemory(
                                    k=2,
                                    memory_key="chat_history",
                                    max_len=50,
                                    return_messages=True,
                                    output_key='answer'
                                )
