# Chat model class that talks to OpenAI (or an OpenAI-compatible API).
from langchain_openai import ChatOpenAI
# Loads key/value pairs from a local .env file into environment variables.
from dotenv import load_dotenv
# Builds a reusable text template with named placeholders such as {feedback}.
from langchain_core.prompts import PromptTemplate
# Turns the model's message object into a plain Python string.
from langchain_core.output_parsers import StrOutputParser
# Parses model text into a Pydantic object using the format instructions below.
from langchain_core.output_parsers import PydanticOutputParser
# BaseModel defines a schema; Field adds a description the model can follow.
from pydantic import BaseModel, Field
# Literal restricts a value to an exact set of allowed strings.
from typing import Literal
# RunnableBranch picks one path; RunnableLambda wraps a plain Python function.
# RunnableParallel is imported here but this file does not use it.
from langchain.schema.runnable import RunnableParallel, RunnableBranch, RunnableLambda

# Read .env so OPENAI_API_KEY (and any other keys) are available to the model.
load_dotenv()

# One model instance, reused by the classifier and by whichever reply branch runs.
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
# String parser used after the model so each step returns plain text.
parser = StrOutputParser()

# Schema the classifier is meant to fill: only "positive" or "negative".
class feedback_classifier(BaseModel):
    # sentiment must be one of those two words; the description tells the model what to put there.
    sentiment: Literal["positive", "negative"] = Field(description="The sentiment of the feedback")

# Parser that knows how to turn model output into a feedback_classifier instance.
pydantic_parser = PydanticOutputParser(pydantic_object=feedback_classifier)

# Prompt that asks the model to label the feedback as positive or negative.
prompt = PromptTemplate(
    # {feedback} is the user's text; {format_instructions} tells the model the required shape.
    template="Classify the snetiment of following feedback into positive and negative \n: {feedback} \n {format_instructions}.",
    # Only feedback is supplied at invoke time.
    input_variables=["feedback"],
    # format_instructions is filled now, from the Pydantic parser, so the caller does not pass it.
    partial_variables={"format_instructions": pydantic_parser.get_format_instructions()}
)

# Classify step: fill the prompt, call the model, then return the reply as a string.
classifier_chain = prompt | model | parser

# Prompt used only when the feedback was labeled positive.
prompt2 = PromptTemplate(
    # {feedback} is the text this branch expects to answer warmly.
    template="Generate a positive response to the following feedback: {feedback}.",
    # This template needs a value named "feedback".
    input_variables=["feedback"]
)

# Prompt used only when the feedback was labeled negative.
prompt3 = PromptTemplate(
    # {feedback} is the text this branch expects to answer carefully.
    template="Generate a negative response to the following feedback: {feedback}.",
    # This template needs a value named "feedback".
    input_variables=["feedback"]
)

# Chooses one runnable based on the sentiment value from the previous step.
branch_chain = RunnableBranch({
    # If sentiment is positive, write the upbeat reply and return its text.
    (lambda x: x["sentiment"] == "positive", prompt2 | model | parser),
    # If sentiment is negative, write the careful reply and return its text.
    (lambda x: x["sentiment"] == "negative", prompt3 | model | parser),
    # Fallback when neither check matches.
    RunnableLambda(lambda x: 'Sentiment not found')
})

# Full pipeline: classify the feedback first, then run the matching reply branch.
chain = classifier_chain | branch_chain

# Start with this feedback string and print whichever branch's reply comes back.
print(chain.invoke({"feedback": "The product is great! I love it!"}))
