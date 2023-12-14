import time
from agency.spaces.local_space import LocalSpace
from .gradio_user import GradioUser
from src.medprompt.space.fhir_agent import SpaceFhirAgent

# Create the space instance
with LocalSpace() as space:

    # Add a host agent to the space, exposing access to the host system
    space.add(SpaceFhirAgent, "SpaceFhirAgent")

    # Connect the Gradio app user to the space
    gradio_user: GradioUser = space.add_foreground(GradioUser, "User")

    # Launch the gradio app
    gradio_user.demo().launch(
        server_name="0.0.0.0",
        server_port=8080,
        prevent_thread_lock=True,
        quiet=True,
    )

    try:
        # block here until Ctrl-C
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass