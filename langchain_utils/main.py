from langchain_utils.step_1 import initialize_llm
from langchain_utils.step_2 import get_intent
from langchain_utils.step_3 import get_product_documents
from langchain_utils.step_4 import create_ensemble_retriever
from langchain_utils.step_5 import process_relevant_docs
from langchain_utils.step_6 import generate_response

def pipeline(user_question):

    llm = initialize_llm()
    intent = get_intent(user_question, llm)
    documents = get_product_documents()
    ensemble_retriever = create_ensemble_retriever(documents)
    relevant_docs = ensemble_retriever.get_relevant_documents(intent)
    image_descriptions = process_relevant_docs(relevant_docs)
    result = generate_response(intent, relevant_docs, image_descriptions, llm)

    return result
