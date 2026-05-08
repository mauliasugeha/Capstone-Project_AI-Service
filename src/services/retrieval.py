import faiss
import pickle
import numpy as np
import os
import pandas as pd
from src.services.embedding import get_embedding

INDEX_PATH = "index/faiss.index"
METADATA_PATH = "index/metadata.pkl"
DATA_PATH = "data/faq_epson.csv"

def create_index():
    print("Membuat index baru dari CSV...")
    if not os.path.exists("index"):
        os.makedirs("index")
    
    df = pd.read_csv(DATA_PATH)
    df.columns = df.columns.str.strip().str.lower()
    if "anwer" in df.columns:
        df.rename(columns={"anwer": "answer"}, inplace=True)
    
    questions = df["question"].astype(str).tolist()
    answers = df["answer"].astype(str).tolist()
    
    embeddings = get_embedding(questions)
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings).astype("float32"))
    
    faiss.write_index(index, INDEX_PATH)
    with open(METADATA_PATH, "wb") as f:
        pickle.dump({"questions": questions, "answers": answers}, f)
    print("Index berhasil dibuat!")
    return index, {"questions": questions, "answers": answers}

# Logika Load atau Create
if not os.path.exists(INDEX_PATH) or not os.path.exists(METADATA_PATH):
    index, metadata = create_index()
else:
    index = faiss.read_index(INDEX_PATH)
    with open(METADATA_PATH, "rb") as f:
        metadata = pickle.load(f)

answers = metadata["answers"]

def retrieve(query, top_k=1):
    query_vector = get_embedding([query])
    D, I = index.search(np.array(query_vector).astype("float32"), top_k)
    return answers[I[0][0]]
