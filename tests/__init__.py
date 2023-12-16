from kink import di
from os import getenv
from src.medprompt.utils.hapi_server import HapiFhirServer

di["fhir_server"] = HapiFhirServer()
di["patient_id"] = getenv("PATIENT_ID", "592911")