import pytest
from src.medprompt.chains.fhir_query import get_fhir_query_tool

def test_fhir_query():
    input = {
        "question": "What is the last erythrocyte count of patient John Doe?",
    }
    output = get_fhir_query_tool(input)
    print(output)
    assert "Therefore, the answer is" in output