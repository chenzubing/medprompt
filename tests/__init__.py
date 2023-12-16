from kink import di
from os import getenv
from src.medprompt.utils.hapi_server import HapiFhirServer

di["fhir_server"] = HapiFhirServer()
