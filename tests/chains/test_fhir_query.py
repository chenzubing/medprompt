import pytest
import json
from src.medprompt.chains.fhir_query import get_fhir_query_tool

def test_fhir_query():
    input = {
        "question": "What is the last erythrocyte count of patient John Doe?",
    }
    output = json.loads(get_fhir_query_tool(input))
    print(output["fhir_query"])
    assert "Observation" in output["fhir_query"]['query']