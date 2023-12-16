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


from typing import List, Tuple

from langchain.agents import AgentType, initialize_agent
from langchain.load import loads
from medprompt.tools.get_medical_record import GetMedicalRecordTool
from medprompt.utils.hapi_server import HapiFhirServer
from pydantic import BaseModel, Field

from .. import MedPrompter
from ..chains import get_rag_tool
from ..tools import (ConvertFhirToTextTool, CreateEmbeddingFromFhirBundle,
                     FhirPatientSearchTool)


class SearchInput(BaseModel):
    """Chat history with the bot."""
    chat_history: List[str] = Field()
    input: str

class _FhirPatientSearchTool(FhirPatientSearchTool, HapiFhirServer):
    pass

class _GetMedicalRecordTool(GetMedicalRecordTool, HapiFhirServer):
    pass

class _ConvertFhirToTextTool(ConvertFhirToTextTool, _GetMedicalRecordTool):
    pass

class _CreateEmbeddingFromFhirBundle(CreateEmbeddingFromFhirBundle, _GetMedicalRecordTool):
    pass
class FhirAgent:
    def __init__(
            self,
            template_path =None,
            llm_model="text_bison_model_v1.txt",
            prefix="fhir_agent_prefix_v1.jinja",
            suffix="fhir_agent_suffix_v1.jinja",
            tools: List = [_FhirPatientSearchTool(), _CreateEmbeddingFromFhirBundle(), _ConvertFhirToTextTool(), get_rag_tool],
        ):
        self.med_prompter = MedPrompter()
        if ".txt" not in llm_model:
            llm_model = llm_model + ".txt"
        self.med_prompter.set_template(template_path=template_path, template_name=llm_model)
        self.llm_str = self.med_prompter.generate_prompt()
        self.llm = loads(self.llm_str)
        if ".jinja" not in prefix:
            prefix = prefix + ".jinja"
        if ".jinja" not in suffix:
            suffix = suffix + ".jinja"
        self.med_prompter.set_template(template_path=template_path, template_name=prefix)
        self.prefix = self.med_prompter.generate_prompt()
        self.med_prompter.set_template(template_path=template_path, template_name=suffix)
        self.suffix = self.med_prompter.generate_prompt()
        self.tools = tools
        self.agent_kwargs = {
            "prefix": self.prefix,
            "suffix": self.suffix,
            "input_variables": ["input", "chat_history", "agent_scratchpad"],
        }

    def get_agent(self):
        return initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            stop=["\nObservation:"],
            max_iterations=len(self.tools),
            handle_parsing_errors=True,
            agent_kwargs=self.agent_kwargs,
            verbose=True).with_types(input_type=SearchInput)


