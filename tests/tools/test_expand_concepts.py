import pytest
from src.medprompt.tools.expand_concepts import ExpandConceptsTool


def test_ExpandConceptsTool():
    # Instantiate the class
    tool = ExpandConceptsTool()


    # Call the method under test
    result = tool._run(concepts=["tuberculosis", "rifampicin"])

    print(result)

    # Assert that the result is as expected
    assert result is not []

async def test_ExpandConceptsToolAsync():
    # Instantiate the class
    tool = ExpandConceptsTool()


    # Call the method under test
    result = await tool._arun(concepts=["tuberculosis", "rifampicin"])

    print(result)

    # Assert that the result is as expected
    assert result is not []