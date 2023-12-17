from kink import di
from os import getenv
from src.medprompt.utils import HapiFhirServer
from src.medprompt.tools import GetMedicalRecordTool

di["fhir_server"] = HapiFhirServer()
di["patient_id"] = getenv("PATIENT_ID", "592911")
di["get_medical_record_tool"] = GetMedicalRecordTool()
di["rag_chain_main_llm"] = getenv("RAG_CHAIN_MAIN_LLM", "gpt4all-orca-mini-3b.txt")
di["rag_chain_clinical_llm"] = getenv("RAG_CHAIN_CLINICAL_LLM", "gpt4all-orca-mini-3b.txt")
# di["rag_chain_main_llm"] = getenv("RAG_CHAIN_MAIN_LLM", "text_bison_001_model_v1.txt")
# di["rag_chain_clinical_llm"] = getenv("RAG_CHAIN_CLINICAL_LLM", "text_bison_001_model_v1.txt")