import pytest
from src.medprompt.agents.fhir_agent import FhirAgent


def test_fhir_agent(patient_id):
    input = {
        "input": "What is the erythrocyte count of  patient " + patient_id + "?",
        "chat_history": [""]
    }
    output = FhirAgent().get_agent().invoke(input)
    print(output)
    assert output is not None