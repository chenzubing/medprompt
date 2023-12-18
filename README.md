# MEDPrompt
## *Prompts, tools, chains and agents* for healthcare using *LLMs & FHIR*.  ✍️
![Libraries.io SourceRank](https://img.shields.io/librariesio/sourcerank/pypi/medprompt)
[![PyPI download total](https://img.shields.io/pypi/dm/medprompt.svg)](https://pypi.python.org/pypi/medprompt/)
![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/dermatologist/medprompt)

## About
**MEDPrompt** is a collection of prompts, tools, chains  and agents for medical applications using [LangChain](https://www.langchain.com/) and *space* using [Agency](https://github.com/operand/agency). **MEDPrompt also includes a collection of templates for using FHIR in LLM prompts (see below).** The aim of MEDPrompt is to provide a conceptual framework and a set of tools for building healthcare applications using LLMs. [Please read my Blog post](https://nuchange.ca/2023/12/medprompt-how-to-architect-llm-solutions-for-healthcare.html). User contributions are highly appreciated!

## Terminology
* **Prompts** are inputs or queries to LLMs that users can provide to elicit specific responses from a Large Language Model (LLM). Example: [*You are an AI assistant. Summarize this clinical document in 250 words*](src/medprompt/templates/summary_v1.jinja)
* **Tools** are functions used by *agents* for getting things done. Example: [To find patient ID from name.](src/medprompt/tools/find_patient.py)
* **Chains** are tools that use LLM calls to get things done. Example: [Answer a clinical question based on patient health record using RAG](src/medprompt/chains/rag_chain.py)
* **Agents** uses an LLM to orchestrate Chains and Tools to acheive the overarching goal. Example: [Answer a doctors question related to a patient. Find patient, get health record, generate embedding and generate answer](src/medprompt/agents/fhir_agent.py)
* **Space** is an [Agency](https://github.com/operand/agency) based abstraction for an environment for agents to communicate according to the [actor model](https://en.wikipedia.org/wiki/Actor_model). Example: [FHIR space](examples/example_space_gradio.py)

### Architecture *(Names correspond to the files in the repository)*
[![Agent](https://github.com/dermatologist/medprompt/blob/develop/notes/agent.drawio.svg)](https://github.com/dermatologist/medprompt/blob/develop/notes/agent.drawio.svg)

### Design principles (WIP)
* **Decoupled** - Each component is independent of the other with [dependencies injected](src/medprompt/bootstrap.py).
* **LLM agnostic** - Each component can use any LLM. LLMS are [injected into chains and agents](src/medprompt/bootstrap.py).
* **No Permanent vector storage** - No permanent storage of vectors. Vectors are generated on the fly.
* **Fail silently** - Each component should fail silently and log errors.
* **Returns** - Each component should return a LLM friendly message.
* **Modular** - Each component is a separate module that can be used independently.
* **Extensible** - New tools, chains and agents can be added easily.
* **Reusable** - Tools, chains and agents can be reused in different contexts.
* **Testable** - Each component can be tested independently.
* **Documented** - Each component is documented with examples.
* **Open** - Open source and open to contributions.

#### Disclaimer:
*This repository is not associated with the [Medprompt method of prompting](https://arxiv.org/pdf/2311.16452.pdf). In this generic repository, [I](https://nuchange.ca) will be trying to implement the method using langchain abstractions. Get in touch to share your thoughts via [GitHub discussions](https://github.com/dermatologist/medprompt/discussions). Please submit a PR with a link to the official implementation if any.*

### FHIR2Text -> Convert FHIR resources to plain text
This repository includes templates for converting **FHIR resources into a text representation** that can be injected into an LLM prompt. Only relevant information is extracted from the resource with simple transformations using helper functions. 🚒[**See this example usage**](/tests/test_fhir_observation_v1.py).

### FHIR2Calculator -> Calculate clinical scores from a FHIR Bundle (*Work in progress*)
Clinical calculators are tools that help healthcare professionals make medical decisions by providing them with quick and easy access to various medical formulas, scores, and algorithms. Calculations performed by LLMs are not reliable. FHIR2Calculator performs calculations on data fields extracted from a FHIR bundle and outputs the results as plain text that can be injected into LLM prompts.

Documentation is in progress. Any help will be highly appreciated.
## [Documentation & List of Templates](https://dermatologist.github.io/medprompt/)

## Usage

## See [Examples folder](/examples)
1. [Observation](/examples/fhirToText.ipynb)
2. [FHIR Bundle](/examples/fhirBundle.ipynb)
More documentation and examples to follow..

### Install
* *medprompt* for the core package
* *embedding* for using RAG with HuggingFace transformers

```
pip install medprompt
pip install medprompt[embedding]
```

### Install Develop branch

```
pip install git+https://github.com/dermatologist/medprompt.git

OR
after cloning the repository
pip install -e .[embedding]
```

### Using templates
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

### Using Tools and chains in an agent

[FHIR Server base class](src/medprompt/utils/fhir_server.py)
[Example Fhir Agent](src/medprompt/agents/fhir_agent.py)

```
from medprompt.tools import FhirPatientSearchTool, CreateEmbeddingFromFhirBundle, ConvertFhirToTextTool, GetMedicalRecordTool
from medprompt.chains import get_rag_tool
from src.medprompt.utils import HapiFhirServer
from os import getenv

# Dependency injection
from kink import di
di["fhir_server"] = HapiFhirServer()
di["patient_id"] = getenv("PATIENT_ID", "592911")
di["get_medical_record_tool"] = GetMedicalRecordTool()

tools = [FhirPatientSearchTool(), CreateEmbeddingFromFhirBundle(), ConvertFhirToTextTool(), get_rag_tool]
```

### Using agents in LangServe
```
from medprompt.agents import FhirAgent
agent = FhirAgent()
add_routes(
    app,
    FhirAgent.get_agent(),
    path="/agent",
)
```

### [Using Space](examples/example_space_gradio.py)

### [Hosting with LangServe](/t_install.py)

## Give us a star ⭐️
If you find this project useful, give us a star. It helps others discover the project.

## Contributing
* PR welcome
* Add templates in [this folder](src/medprompt/templates/) as [jinja2](https://jinja.palletsprojects.com/en/3.1.x/) or JSON.
* Follow the naming conventions in the folder.
* Add tools, chains and agents in the [appropriately named folders.](src/medprompt/)
* Add documentations [here](info/) as a markdown file with the same name.
* Add a link in the [index.md file](info/index.md).
* Please see [CONTRIBUTING.md](/CONTRIBUTING.md)

## Contributers
* [Bell Eapen](https://nuchange.ca) | [![Twitter Follow](https://img.shields.io/twitter/follow/beapen?style=social)](https://twitter.com/beapen)
* [My Blog post](https://nuchange.ca/2023/12/medprompt-how-to-architect-llm-solutions-for-healthcare.html)