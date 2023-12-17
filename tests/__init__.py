from kink import di
from os import getenv
import os
from src.medprompt.utils import HapiFhirServer
from src.medprompt.tools import GetMedicalRecordTool
from langchain.llms import VertexAI, GPT4All
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

di["fhir_server"] = HapiFhirServer()
di["patient_id"] = getenv("PATIENT_ID", "592911")
di["get_medical_record_tool"] = GetMedicalRecordTool()

di["model_name"] = getenv("MODEL_NAME", "text-bison@001")
di["n"] = int(getenv("N", "1"))
di["stop"] = getenv("STOP", None)
di["max_output_tokens"] = int(getenv("MAX_OUTPUT_TOKENS", "1024"))
di["temperature"] = float(getenv("TEMPERATURE", "0.1"))
di["top_p"] = float(getenv("TOP_P", "0.8"))
di["top_k"] = int(getenv("TOP_K", "40"))
di["verbose"] = True

di["vertex_ai"] = lambda di: VertexAI(
    model_name=di["model_name"],
    n=di["n"],
    stop=di["stop"],
    max_output_tokens=di["max_output_tokens"],
    temperature=di["temperature"],
    top_p=di["top_p"],
    top_k=di["top_k"],
    verbose=di["verbose"],
)

di["gpt4all_model_path"] = getenv("GPT4ALL_MODEL_PATH", os.getcwd() + "/models/orca-mini-3b-gguf2-q4_0.gguf")

di["gpt4al"] = lambda di: GPT4All(
    model=di["gpt4all_model_path"],
    backend="gptj",
    callbacks=[StreamingStdOutCallbackHandler()],
    verbose=True
)

di["rag_chain_main_llm"] = di["gpt4al"]
di["rag_chain_clinical_llm"] = di["gpt4al"]
di["fhir_agent_llm"] = di["gpt4al"]