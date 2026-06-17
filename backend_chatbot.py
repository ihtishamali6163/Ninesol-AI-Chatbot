import os
from dotenv import load_dotenv

from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# ==================================================
# Environment Variables
# ==================================================

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")


# ==================================================
# Models & Database
# ==================================================

print("Loading Embedding Model...")

emb = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

print("Connecting to Chroma DB...")

store = Chroma(
    persist_directory="D:/NineSol_project/Company_rag/chroma_db",
    embedding_function=emb,
    collection_name="nine_sole_db",
)

print("Loading Language Model...")

llm = ChatGroq(
    api_key=api_key,
    temperature=0.4,
    model="openai/gpt-oss-120b",
)
retriever = store.as_retriever(search_kwargs={"k": 5})

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are NineSol Technologies' AI assistant.

            Rules:
            
            1. Greet the user only if it is their first message.
            2. If user says "Assalamu Alaikum", reply "Wa Alaikum Assalam".
            3. Reply in the same language used by the user.
            4. Remember information shared by the user during the conversation.
            5. Use ONLY the provided context to answer company-related questions.
            6. If the answer is not found in the context, use conversation memory only for personal information previously shared by the user.
            7. If the answer is unavailable, say:
               "I don't have enough information in the provided material."
            8. If the question is unrelated to NineSol Technologies, politely respond:
               "Please ask something related to NineSol Technologies."

Context:
{context}
            """,
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}"),
    ]
)
base_chain = (
    RunnablePassthrough.assign(
        context=lambda inputs: format_docs(retriever.invoke(inputs["question"]))
    )
    | prompt
    | llm
    | StrOutputParser()
)
session_memory_store = {}

def get_session_history(
    session_id: str,
) -> InMemoryChatMessageHistory:

    if session_id not in session_memory_store:

        session_memory_store[session_id] = InMemoryChatMessageHistory()

    return session_memory_store[session_id]


runnable_with_memory = RunnableWithMessageHistory(
    base_chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="chat_history",
)

def ask_question(
    question: str,
    session_id: str,
):

    response = runnable_with_memory.invoke(
        {"question": question},
        config={"configurable": {"session_id": session_id}},
    )

    return response


print("=" * 50)
print("NineSol Assistant Ready")
print("=" * 50)
