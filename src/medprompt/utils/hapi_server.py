import httpx
import json
import logging
import os

from .fhir_server import FhirServer
_logger = logging.getLogger(__name__)

class HapiFhirServer(FhirServer):
    """
    A class for calling the FHIR server.
    Inherit from this class and override the call_fhir_server and async_call_fhir_server methods.
    """

    def call_fhir_server(self, url, params=None):
        """
        Calls the FHIR server with the provided URL and parameters.

        Args:
            url (str): The URL of the FHIR server to call.
            params (dict): The parameters to include in the call.

        Returns:
            response (requests.Response): The response from the FHIR server.
        """
        base_url = 'http://hapi.fhir.org/baseR4'
        try:
            response = httpx.get(base_url + url, params=params)
            response.raise_for_status()
            _response = json.loads(response.text)
        except:
            # raise ValueError("FHIR server not responding")
            return "Sorry I cannot find the answer as the FHIR server is not responding."
        return _response

    async def async_call_fhir_server(self, url, params=None):
        """
        Asynchronously calls the FHIR server with the provided URL and parameters.

        Args:
            url (str): The URL of the FHIR server to call.
            params (dict): The parameters to include in the call.

        Returns:
            _response (dict): The response from the FHIR server as a dictionary.
        """
        base_url = 'http://hapi.fhir.org/baseR4'
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(base_url + url, params=params)

            response.raise_for_status()
            _response = json.loads(response.text)
        except:
            _logger.error("FHIR server not responding")
            return "Sorry I cannot find the answer as the FHIR server is not responding."
        return _response