# Chat model class that talks to OpenAI (or an OpenAI-compatible API).
from langchain_openai import ChatOpenAI
# Loads key/value pairs from a local .env file into environment variables.
from dotenv import load_dotenv
# Builds a reusable text template with named placeholders such as {topic}.
from langchain_core.prompts import PromptTemplate
# Turns the model's message object into a plain Python string.
from langchain_core.output_parsers import StrOutputParser

# Read .env so OPENAI_API_KEY (and any other keys) are available to the model.
load_dotenv()

# Prompt that asks the model for five facts about whatever topic is supplied.
prompt = PromptTemplate(
    # Declares that this template expects a value named "topic".
    input_variables=["topic"],
    # {topic} is filled in later from the input dictionary.
    template="Generate 5 intersting facts about {topic}?"
)

# Model instance; temperature 0 keeps answers steady and less random.
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
# Parser so the chain returns text instead of a chat message object.
parser = StrOutputParser()
# Pipe the steps: fill the prompt, call the model, then extract the text.
chain = prompt | model | parser

# Start the chain with a topic and print the five facts.
print(chain.invoke({"topic": "Python"}))
