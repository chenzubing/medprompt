import pytest
from src.medprompt.chains.clinical_summary import get_summary_tool

document = """
A 40-year old male patient presented to the out patient department of our institute with complaints of painful oral ulceration.
History revealed that complaints started 3 to 4 days back.
Initially to start with, there was redness in the oral cavity and over lips.
Soon bleeding ulcers and bullae appeared at these sites. Bullae ruptured to form encrustations over lips.
"""

def test_clinical_summary():
    input = {
        "clinical_document": document,
        "word_count": "10",
    }
    output = get_summary_tool(input)
    print(output)
    assert "oral" in output