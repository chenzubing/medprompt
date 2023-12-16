from kink import di
from os import getenv
from src.medprompt.utils import HapiFhirServer
from src.medprompt.tools import GetMedicalRecordTool

di["fhir_server"] = HapiFhirServer()
di["patient_id"] = getenv("PATIENT_ID", "592911")
di["get_medical_record_tool"] = GetMedicalRecordTool()