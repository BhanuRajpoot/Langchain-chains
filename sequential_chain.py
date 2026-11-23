from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

prompt1 = PromptTemplate(
    template="Generate a detailed report on the following topic: {topic}.",
    input_variables=["topic"]
)

prompt2 = PromptTemplate(
    template="Summarize the following report: {report}.",
    input_variables=["report"]
)

model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
parser = StrOutputParser()
chain = prompt1 | model | parser | prompt2 | model | parser

print(chain.invoke({"topic": "Artificial Intelligence"}))
