import pytest
from src.medprompt.chains.clinical_summary import get_summary_tool

document = """
A 40-year old male patient presented to the out patient department of our institute with complaints of painful oral ulceration.
History revealed that complaints started 3 to 4 days back.
Initially to start with, there was redness in the oral cavity and over lips.
Soon bleeding ulcers and bullae appeared at these sites. Bullae ruptured to form encrustations over lips.
Odynophagia and dysarthria was present. No history of febrile episode was present.
There was no history of drug intake before the onset of these lesions. No other mucosal surface involvement history was present.
Only positive history was that patient was a chronic alcoholic and had drinking episode in which he had mixed different brands of alcohol, a day before start of his complaints.
On clinical examination, dark brown encrustations were present on lips. Lips were edematous and erythema was present around encrustations.
Bleeding ulcers were present on dorsum of tongue, hard palate, buccal mucosa, and gingivae.
Few hyperemic papules and macules were also present. Pharyngeal and laryngeal examination was normal.
No neck nodes were palpable. A diagnostically significant finding was the presence of two target lesions on the palmar surface of left hand.
Other systemic examination was normal.
"""

def test_clinical_summary():
    input = {
        "clinical_document": document,
        "word_count": "50",
    }
    output = get_summary_tool(input)
    print(output)
    assert "oral" in output