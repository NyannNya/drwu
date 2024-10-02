from langchain_community.vectorstores import FAISS
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from langchain_openai import OpenAIEmbeddings
from . import openai_api_key
import json

def create_ensemble_retriever(documents):
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    vector_store = FAISS.from_documents(documents, embeddings)
    faiss_retriever = vector_store.as_retriever()
    bm25_retriever = BM25Retriever.from_documents(documents)
    ensemble_retriever = EnsembleRetriever(retrievers=[bm25_retriever, faiss_retriever])
    return ensemble_retriever

