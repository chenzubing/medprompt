from kink import di
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.tools import tool
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from langchain.prompts.prompt import PromptTemplate
from langchain.output_parsers import GuardrailsOutputParser

from .. import MedPrompter
med_prompter = MedPrompter()
med_prompter.set_template(template_name='fhir_rails_v1.xml')

rail_spec = med_prompter.generate_prompt()
fhir_query_llm = di["fhir_query_llm"]
output_parser = GuardrailsOutputParser.from_rail_string(rail_spec, api=fhir_query_llm)

FHIR_QUERY_PROMPT = PromptTemplate(
    template=output_parser.guard.prompt.escape(),
    input_variables=output_parser.guard.prompt.variable_names,
)

class FhirQueryPrompt(BaseModel):
    question: str = Field()

def get_runnable(**kwargs):
    """Get the runnable chain."""
    _cot = RunnablePassthrough.assign(
        question = lambda x: x["question"],
        ) | FHIR_QUERY_PROMPT | fhir_query_llm | StrOutputParser()
    chain = _cot.with_types(input_type=FhirQueryPrompt)
    return chain

@tool("fhir query string", args_schema=FhirQueryPrompt)
def get_fhir_query_tool(**kwargs):
    """
    Returns the FHIR query string for the given question.

    Args:
        question (str): The question asked to the model.
    """
    return get_runnable().invoke(kwargs)