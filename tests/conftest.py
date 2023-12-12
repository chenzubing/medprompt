"""
    Dummy conftest.py for medprompt.

    If you don't know what this is for, just leave it empty.
    Read more about conftest.py under:
    - https://docs.pytest.org/en/stable/fixture.html
    - https://docs.pytest.org/en/stable/writing_plugins.html
"""

import pytest
import os
import requests
import json

@pytest.fixture
def f():
    from src.medprompt import MedPrompter
    _m = MedPrompter()
    return _m

@pytest.fixture(scope="session")
def patient_id():
    url = os.environ.get("FHIR_SERVER_URL", 'http://hapi.fhir.org/baseR4')
    _patient = requests.get(url + "/Patient?_pretty=true")
    patient = json.loads(_patient.text)
    patient_id = patient["entry"][0]["resource"]["id"]
    for root, dirs, files in os.walk("tests/data"):
        for file in files:
            if file.endswith(".json"):
                fhir_json = open(os.path.join(root, file)).read()
                resource = json.loads(fhir_json)
                resource["subject"]["reference"] = "Patient/"+patient_id
                headers = {'Content-Type': 'application/json'}
                _post_url = url + "/" + resource["resourceType"]
                response = requests.post(_post_url, data=json.dumps(resource), headers=headers)
    return patient_id