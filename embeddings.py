from os import environ
from dotenv import load_dotenv 
import openai 
import numpy as np

load_dotenv()
api_key = environ.get('OPENAI_KEY')

def get_embeddings(text):
    return np.array(openai.Embedding.create(input=text,
model="text-embedding-ada-002", api_key=api_key)["data"][0]["embedding"], dtype=np.float32)

def get_cosine_similarity(a, b):
    # Find the dot product of the embeddings
    dot_product = np.dot(a, b)

    # Find the L2 norm of the embeddings
    norm1 = np.linalg.norm(a)
    norm2 = np.linalg.norm(b)

    # Calculate the cosine similarity
    similarity = dot_product / (norm1 * norm2)
    return similarity