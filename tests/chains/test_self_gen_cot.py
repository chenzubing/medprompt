import pytest
from src.medprompt.chains.self_gen_cot import get_sgc_tool

def test_self_gen_cot():
    input = {
        "question": "What is the erythrocyte count?",
        "answer": "The erythrocyte count is 4.5 million cells per microliter."
    }
    output = get_sgc_tool(input)
    print(output)
    assert "Therefore, the answer is" in output