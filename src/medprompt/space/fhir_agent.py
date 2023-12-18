from agency.agent import Agent, action
from ..agents import FhirAgent

class SpaceFhirAgent(Agent):

    @action
    def say(self, content: str, chat_history: list = []):
        """Search for a patient in the FHIR database."""
        #! TODO: Needs bootstrapping here.

        message = {
            "input": content,
            "chat_history": chat_history,
        }
        response_content = FhirAgent().get_agent().invoke(message)
        self.send({
          "to": self.current_message()['from'],
          "action": {
            "name": "say",
            "args": {
                "content": response_content["output"],
            }
          }
        })
        return True