from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

prompt = PromptTemplate(
    input_variables=["topic"],
    template="Generate 5 intersting facts about {topic}?"
)

model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
parser = StrOutputParser()
chain = prompt | model | parser

print(chain.invoke({"topic": "Python"}))
