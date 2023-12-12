# import pytest
# from src.medprompt.chains.rag_chain import check_index, get_rag_tool

# def test_check_index():
#     # Test with valid patient_id
#     input_object = {
#         "patient_id": "41399401",
#         "input": "What is the erythrocyte count?",
#         "chat_history": [""]
#     }
#     result = check_index(input_object)
#     print(result)
#     assert result is not None


# def test_get_rag_chain_not_mentioned():
#     input = {
#         "patient_id": "41399401",
#         "input": "What is the patient's weight?",
#         "chat_history": [""]
#     }
#     output = get_rag_tool(input)
#     print(output)
#     assert "not mentioned" in output

# def test_get_rag_chain_not_mentioned():
#     input = {
#         "patient_id": "41399401",
#         "input": "What is the erythrocyte count of this patient?",
#         "chat_history": [""]
#     }
#     output = get_rag_tool(input)
#     print(output)
#     assert "4.12" in output