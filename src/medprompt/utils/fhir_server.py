class FhirServer:

    @staticmethod
    def call_fhir_server(url, params=None):
        """
        Calls the FHIR server with the provided URL and parameters.

        Args:
            url (str): The URL of the FHIR server to call.
            params (dict): The parameters to include in the call.

        Returns:
            response (requests.Response): The response from the FHIR server.
        """
        pass

    @staticmethod
    async def async_call_fhir_server(url, params=None):
        """
        Asynchronously calls the FHIR server with the provided URL and parameters.

        Args:
            url (str): The URL of the FHIR server to call.
            params (dict): The parameters to include in the call.

        Returns:
            _response (dict): The response from the FHIR server as a dictionary.
        """
        pass