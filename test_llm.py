from langchain_groq import ChatGroq
llm = ChatGroq(model="openai/gpt-oss-20b")
print(llm.invoke("Hello").content)
