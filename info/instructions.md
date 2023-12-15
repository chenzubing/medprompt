# Instructions

## Using templates
```
from medprompt import MedPrompter
prompt = MedPrompter()
prompt.set_template(
    template_name="fhir_search_oai_chat_v1.json")

print(prompt.get_template_variables())

messages = prompt.generate_prompt(
    {"question": "Find Conditions for patient with first name John?"})

print(messages)
```

## Using Tools and chains in an agent
```
from medprompt.tools import FhirPatientSearchTool
tools = [FhirPatientSearchTool()]
```

## Using agents in LangServe
```
from medprompt.agents import FhirAgent
agent = FhirAgent()
add_routes(
    app,
    FhirAgent.get_agent(),
    path="/agent",
)
```

## Using Space
```
from src.medprompt.space.fhir_agent import SpaceFhirAgent

# Create the space instance
with LocalSpace() as space:

    # Add a host agent to the space, exposing access to the host system
    space.add(SpaceFhirAgent, "SpaceFhirAgent")
```