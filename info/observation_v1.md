# FHIR Observation to free text mapper template

* This template is for converting an Observation resource into text form.
* The effectiveDaeTime time stamp is converted into a form that is suitable for LLMs to assess temporality. Example: *2 months ago*
* The code.text, interpretation and the valueQuantity are converted into text.