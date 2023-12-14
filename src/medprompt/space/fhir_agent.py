from agency.agent import Agent, action
from ..agents import FhirAgent

class SpaceFhirAgent(Agent):

    @action
    def say(self, message: str):
        """Search for a patient in the FHIR database."""
        response_content = FhirAgent().get_agent().invoke(message)
        self.send({
          "to": self.current_message['from'],
          "action": {
            "name": "say",
            "args": {
                "content": response_content,
            }
          }
        })