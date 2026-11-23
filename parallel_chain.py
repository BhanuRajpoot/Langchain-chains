# Chat model class that talks to OpenAI (or an OpenAI-compatible API).
from langchain_openai import ChatOpenAI
# Loads key/value pairs from a local .env file into environment variables.
from dotenv import load_dotenv
# Builds a reusable text template with named placeholders such as {topic}.
from langchain_core.prompts import PromptTemplate
# Turns the model's message object into a plain Python string.
from langchain_core.output_parsers import StrOutputParser
# Runs several chains at the same time and returns a dict of their results.
from langchain.schema.runnable import RunnableParallel

# Read .env so OPENAI_API_KEY (and any other keys) are available to the model.
load_dotenv()

# Prompt that asks the model to turn a topic into short study notes.
prompt1 = PromptTemplate(
    # {topic} is filled in later from the input dictionary.
    template="Generate simple and sort notes from the following topic: {topic}.",
    # Declares which placeholders this template expects.
    input_variables=["topic"]
)

# Prompt that asks the model to turn the same topic into a quiz.
prompt2 = PromptTemplate(
    # Same placeholder name as prompt1 so both branches can share one input.
    template="Generate a quiz from the following topic: {topic}.",
    # This template only needs the topic string.
    input_variables=["topic"]
)

# Prompt that combines the two parallel outputs into one final answer.
prompt3 = PromptTemplate(
    # {notes} and {quiz} must match the keys produced by the parallel chain.
    template="Merge the following notes and quiz: {notes} and {quiz}.",
    # Both pieces of text are required before this prompt can run.
    input_variables=["notes", "quiz"]
)

# First model instance; temperature 0 keeps answers steady and less random.
model1 = ChatOpenAI(model="gpt-4o-mini", temperature=0)
# Second model instance so the quiz branch can call the API on its own.
model2 = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Shared parser: each branch and the merge step return text, not a message object.
parser = StrOutputParser()

# Fan-out step: both branches receive the same {"topic": ...} input together.
parallel_chain = RunnableParallel({
    # Notes branch: fill prompt1, call model1, then extract the text.
    "notes": prompt1 | model1 | parser,
    # Quiz branch: fill prompt2, call model2, then extract the text.
    "quiz": prompt2 | model2 | parser
})

# Fan-in step: takes the dict {"notes": ..., "quiz": ...} and writes one merged reply.
merge_chain = prompt3 | model1 | parser

# Full pipeline: run both branches in parallel, then pass their results into the merge.
chain = parallel_chain | merge_chain

# Start the pipeline with a topic and print the merged notes-plus-quiz string.
print(chain.invoke({"topic": "Artificial Intelligence"}))
