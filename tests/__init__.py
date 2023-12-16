from kink import di
from os import getenv
from src.medprompt.utils.hapi_server import HapiFhirServer
from src.medprompt.tools.get_medical_record import GetMedicalRecordTool

di["fhir_server"] = HapiFhirServer()
di["patient_id"] = getenv("PATIENT_ID", "592911")
di["get_medical_record_tool"] = GetMedicalRecordTool()