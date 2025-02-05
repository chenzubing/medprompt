import pytest
from src.medprompt.tools.create_embedding import CreateEmbeddingFromFhirBundle
from src.medprompt.chains.rag_chain import get_rag_tool


@pytest.mark.order(1)
def test_create_embedding_from_fhir_bundle(patient_id):
    # Initialize the class
    create_embedding = CreateEmbeddingFromFhirBundle()

    # Test the _run method
    result = create_embedding._run(patient_id=patient_id)
    print(result)
    assert result is not None


# @pytest.mark.order(2)
# def test_created_embedding(patient_id):
#     EMBED_MODEL = os.getenv("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
#     embedding = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
#     vectorstore = Chroma(collection_name=patient_id, persist_directory=os.getenv("CHROMA_DIR", "/tmp/chroma"), embedding_function=embedding)
#     retriever = vectorstore.as_retriever()
#     result = vectorstore.similarity_search("Erythrocytes", k=10)
#     assert result is not None
#     retreived = retriever.get_relevant_documents("Erythrocytes", k=10)
#     print(retreived)
#     assert retreived is not None


@pytest.mark.order(2)
def test_created_embedding(patient_id):
    input = {
        "chat_history": [""],
        "input": "Erythrocytes [#/volume] in Blood by Automated count?",
        "patient_id": "592911"
    }

    x = get_rag_tool(input)
    print(x)