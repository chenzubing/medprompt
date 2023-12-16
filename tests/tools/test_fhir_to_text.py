import pytest
import pytest
from src.medprompt.tools.create_embedding import CreateEmbeddingFromFhirBundle
from src.medprompt.chains.rag_chain import get_rag_tool
import os
import requests
import json
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from src.medprompt.tools.fhir_to_text import ConvertFhirToTextTool
from src.medprompt.tools.get_medical_record import GetMedicalRecordTool
from src.medprompt.utils.hapi_server import HapiFhirServer

class _GetMedicalRecordTool(GetMedicalRecordTool, HapiFhirServer):
    pass

class _ConvertFhirToTextTool(ConvertFhirToTextTool, _GetMedicalRecordTool):
    pass

def test_ConvertFhirToTextTool(patient_id):
    # Instantiate the class
    tool = _ConvertFhirToTextTool()


    # Call the method under test
    result = tool._run(patient_id=patient_id)

    print(result)

    # Assert that the result is as expected
    assert result is not None