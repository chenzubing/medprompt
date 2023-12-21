"""
 Copyright 2023 Bell Eapen

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""


from typing import List
from kink import di
from langchain.prompts.prompt import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableMap, RunnablePassthrough
from langchain.tools import tool
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.output_parsers import GuardrailsOutputParser
from ..tools import ExpandConceptsTool

from .. import MedPrompter
med_prompter = MedPrompter()
import logging
_logger = logging.getLogger(__name__)
class ClinicalConceptOutput(BaseModel):
    clinical_concepts: List[str] = Field()

class ClinicalConceptInput(BaseModel):
    clinical_document: str = Field()
    word_count: str = Field()

CLINICAL_CONCEPT_INPUT_TEMPLATE = """
Given the following clinical document, extract the clinical concepts and return them as a list.
The clinical concepts include the following:
- Problem
- Medication
- Procedure
- Lab
- Vital
- Medication

Clinical Document: ${clinical_document}
${gr.complete_json_suffix_v2}
"""

clinical_concepts_output_parser = GuardrailsOutputParser.from_pydantic(output_class=ClinicalConceptOutput, prompt=CLINICAL_CONCEPT_INPUT_TEMPLATE)

CLINICAL_CONCEPT_INPUT_PROMPT = PromptTemplate(
    template=clinical_concepts_output_parser.guard.prompt.escape(),
    input_variables=["clinical_document"],
)

CLINICAL_CONCEPT_SUMMARY_TEMPLATE = """
Given the following clinical concepts, summarize them into a single paragraph of ${input.word_count} words.
Include comments on these ${input.clinical_concepts}.

Clinical Document: ${input.clinical_document}
"""

CLINICAL_CONCEPT_SUMMARY_PROMPT = PromptTemplate(
    template=CLINICAL_CONCEPT_SUMMARY_TEMPLATE,
    input_variables=["input"],
)

main_llm = di["rag_chain_main_llm"]
clinical_llm = di["rag_chain_clinical_llm"]

def get_runnable(**kwargs):
    """Get the runnable chain."""
    list_of_concepts = RunnablePassthrough.assign(
        clinical_document=lambda x: x["clinical_document"],
    ) | CLINICAL_CONCEPT_INPUT_PROMPT | clinical_llm | clinical_concepts_output_parser | ExpandConceptsTool().with_types(input_type=ClinicalConceptOutput)
    input = RunnablePassthrough.assign(
        clinical_document=lambda x: x["clinical_document"],
        word_count=lambda x: x["word_count"],
    )
    _inputs = RunnableMap(
        clinical_concepts=list_of_concepts,
        input=input,
    )
    _chain = _inputs | CLINICAL_CONCEPT_SUMMARY_PROMPT | main_llm | StrOutputParser()
    chain = _chain.with_types(input_type=ClinicalConceptInput)
    return chain

@tool("clinical summary", args_schema=ClinicalConceptInput)
def get_summary_tool(**kwargs):
    """
    Summarize the clinical document to a given word count.

    Args:
        clinical_document (str): The clinical document to summarize.
        word_count (str): The number of words to summarize to.
    """
    return get_runnable().invoke(kwargs)
