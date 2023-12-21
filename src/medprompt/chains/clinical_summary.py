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
import json
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

main_llm = di["rag_chain_main_llm"]
clinical_llm = di["rag_chain_clinical_llm"]

rail_spec = """
<rail version="0.1">
<output>
    <object name="response" format="length: 1">
        <string
            name="concepts"
            description="The list of concepts extracted from the clinical document."
            format="list"
            on-fail-length="reask"
        />
    </object>
</output>


<prompt>

Given the following clinical document, extract all the clinical concepts and return them as a list.
If concepts are repeated, return them only once.
If concepts have two words, return them as a single word joined by an underscore.
The clinical concepts include the following:
- Problem
- Medication
- Procedure
- Lab
- Vital
- Medication

Clinical Document: ${clinical_document}
${gr.complete_json_suffix_v2}

</prompt>
</rail>

"""


class ClinicalConceptInput(BaseModel):
    clinical_document: str = Field()
    word_count: str = Field()



clinical_concepts_output_parser = GuardrailsOutputParser.from_rail_string(rail_spec, api=main_llm)

CLINICAL_CONCEPT_INPUT_PROMPT = PromptTemplate(
    template=clinical_concepts_output_parser.guard.prompt.escape(),
    input_variables=["clinical_document"],
)

# CLINICAL_CONCEPT_SUMMARY_TEMPLATE = """
# Given the following clinical concepts, summarize them into a single paragraph of ${input.word_count} words.
# Include comments on these ${input.clinical_concepts}.

# Clinical Document: ${input.clinical_document}
# """

# CLINICAL_CONCEPT_SUMMARY_PROMPT = PromptTemplate(
#     template=CLINICAL_CONCEPT_SUMMARY_TEMPLATE,
#     input_variables=["input"],
# )


def extract_concepts(guardrails_output):
    """Extract the concepts from the clinical document."""
    _gr = json.loads(guardrails_output)
    return _gr["response"]
    # concepts = _gr["response"]["concepts"]
    # return concepts


def get_runnable(**kwargs):
    """Get the runnable chain."""
    list_of_concepts = RunnablePassthrough.assign(
        clinical_document=lambda x: x["clinical_document"],
    ) | CLINICAL_CONCEPT_INPUT_PROMPT | main_llm | StrOutputParser() | extract_concepts |  ExpandConceptsTool().run
    # input = RunnablePassthrough.assign(
    #     clinical_document=lambda x: x["clinical_document"],
    #     word_count=lambda x: x["word_count"],
    # )
    # _inputs = RunnableMap(
    #     clinical_concepts=list_of_concepts,
    #     input=input,
    # )
    # _chain = _inputs | CLINICAL_CONCEPT_SUMMARY_PROMPT | main_llm | StrOutputParser()
    # chain = _chain.with_types(input_type=ClinicalConceptInput)
    chain = list_of_concepts
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
