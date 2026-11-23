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

# First prompt: ask the model to write a full report on a topic.
prompt1 = PromptTemplate(
    # {topic} is filled in from the dictionary passed to chain.invoke.
    template="Generate a detailed report on the following topic: {topic}.",
    # This template only needs the topic string.
    input_variables=["topic"]
)

# Second prompt: ask the model to shorten whatever report it just wrote.
prompt2 = PromptTemplate(
    # {report} is filled by the string coming out of the first prompt-model-parser run.
    template="Summarize the following report: {report}.",
    # This template expects the previous step's text under the name "report".
    input_variables=["report"]
)

# One model instance, reused for both the report and the summary.
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
# Parser used after each model call so the next step receives plain text.
parser = StrOutputParser()
# Run in order: topic -> report -> text, then that text -> summary -> text.
chain = prompt1 | model | parser | prompt2 | model | parser

# Start with a topic; the chain writes a report, summarizes it, and prints the summary.
print(chain.invoke({"topic": "Artificial Intelligence"}))
