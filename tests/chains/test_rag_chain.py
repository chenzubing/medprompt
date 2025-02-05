import pytest
from src.medprompt.chains.rag_chain import check_index, get_rag_tool

def test_check_index(patient_id):
    # Test with valid patient_id
    input_object = {
        "patient_id": patient_id,
        "input": "What is the erythrocyte count of patient " + patient_id + "?",
        "chat_history": [""]
    }
    result = check_index(input_object)
    print(result)
    assert result is not None


def test_get_rag_chain_not_mentioned(patient_id):
    input = {
        "patient_id": patient_id,
        "input": "What is the weight of patient " + patient_id + "?",
        "chat_history": [""]
    }
    output = get_rag_tool(input)
    print(output)
    assert "unknown" in output


def test_get_rag_chain_mentioned(patient_id):
    input = {
        "patient_id": patient_id,
        "input": "What is the last blood glucose of patient " + patient_id + "?",
        "chat_history": [""]
    }
    output = get_rag_tool(input)
    print(output)
    assert "glucose" in output