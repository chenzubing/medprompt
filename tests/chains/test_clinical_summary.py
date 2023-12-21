import pytest
from src.medprompt.chains.clinical_summary import get_summary_tool

def test_clinical_summary():
    input = {
        "clinical_document": "Patient had a CBC done. The erythrocyte count is 4.5 million cells per microliter. The hemoglobin is 12.5 grams per deciliter. The hematocrit is 40%. The platelet count is 200,000 per microliter. The white blood cell count is 5,000 per microliter.",
        "word_count": "50"
    }
    output = get_summary_tool(input)
    print(output)
    assert "Therefore, the answer is" in output