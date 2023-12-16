import pytest
from unittest.mock import patch, Mock
from src.medprompt.tools.get_medical_record import GetMedicalRecordTool, SearchInput
from src.medprompt.utils.hapi_server import HapiFhirServer


class _GetMedicalRecordTool(GetMedicalRecordTool, HapiFhirServer):
    pass

@patch('httpx.get')
def test_run_method(mock_get):
    # Arrange
    tool = _GetMedicalRecordTool()
    mock_get.return_value = Mock(status_code=200)
    mock_get.return_value.raise_for_status = Mock()
    mock_get.return_value.text = '{"total": 1}'

    # Act
    result = tool._run(patient_id='123')

    # Assert
    assert result == {"total": 1}
    mock_get.assert_called_once()

@patch('httpx.AsyncClient.get')
@pytest.mark.asyncio
async def test_arun_method(mock_get):
    # Arrange
    tool = _GetMedicalRecordTool()
    mock_get.return_value = Mock(status_code=200)
    mock_get.return_value.raise_for_status = Mock()
    mock_get.return_value.text = '{"total": 1}'

    # Act
    result = await tool._arun(patient_id='123')

    # Assert
    assert result == {"total": 1}
    mock_get.assert_called_once()

def test_format_query():
    # Arrange
    tool = _GetMedicalRecordTool()

    # Act
    result = tool._format_query(patient_id='123')

    # Assert
    expected_query = "/Patient?_id=123&_revinclude=Observation:subject&_revinclude=Condition:subject&_revinclude=Procedure:subject&_revinclude=MedicationRequest:subject"
    assert result == expected_query


def test_integration_run(patient_id):
    # Arrange
    tool = _GetMedicalRecordTool()

    # Act
    result = tool.run(patient_id)

    # Assert
    assert result is not None