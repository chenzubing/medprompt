import pytest
from src.medprompt.tools.fhir_to_text import ConvertFhirToTextTool


def test_ConvertFhirToTextTool(patient_id):
    # Instantiate the class
    tool = ConvertFhirToTextTool()


    # Call the method under test
    result = tool._run(patient_id=patient_id)

    print(result)

    # Assert that the result is as expected
    assert result is not None