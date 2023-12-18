from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import LLMChain
from langchain.llms import GPT4All
from langchain.prompts import PromptTemplate

from langchain.load import loads, dumps


template = """Question: {question}

Answer: Let's think step by step."""

prompt = PromptTemplate(template=template, input_variables=["question"])

local_path = (
    "models/orca-mini-3b-gguf2-q4_0.gguf"  # replace with your desired local file path
)

# Callbacks support token-wise streaming
callbacks = [StreamingStdOutCallbackHandler()]

# Verbose is required to pass to the callback manager
llm = GPT4All(model=local_path, callbacks=callbacks, verbose=True)

# If you want to use a custom model add the backend parameter
# Check https://docs.gpt4all.io/gpt4all_python.html for supported backends
llm = GPT4All(model=local_path, backend="gptj", callbacks=callbacks, verbose=True)

print(dumps(llm))

llm_def = """
{"lc": 1, "type": "constructor", "id": ["langchain", "llms", "gpt4all", "GPT4All"], "kwargs": {"model": "/home/beapen/repos/medprompt/models/orca-mini-3b-gguf2-q4_0.gguf", "backend":"gptj", "stop": null, "top_p": 0.8, "top_k": 40, "verbose": true}}
"""

_llm = loads(llm_def)

llm_chain = LLMChain(prompt=prompt, llm=llm)

question = "What NFL team won the Super Bowl in the year Justin Bieber was born?"

llm_chain.run(question)