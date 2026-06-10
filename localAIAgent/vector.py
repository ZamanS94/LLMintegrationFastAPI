from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os
import pandas as pd

df = pd.read_csv("realistic_restaurant_reviews.csv")
embeddings = OllamaEmbeddings(model="mxbai-embed-large")

db_location = "./chrome_langchain_db"
is_documents = not os.path.exists(db_location)

if is_documents:
    documents = []
    ids = []
    
    for i, row in df.iterrows():
        document = Document(
            page_content=row["Title"] + " " + row["Review"], #the important searchable info we want to look at
            metadata={"rating": row["Rating"], "date": row["Date"]}, #additional data
            id=str(i)
        )
        ids.append(str(i))
        documents.append(document)

#initialize or load Chroma vector database      
vector_store = Chroma(
    collection_name="restaurant_reviews",
    persist_directory=db_location, #not to create vector db repeatedly
    embedding_function=embeddings
)

#add documents only on first run
if vector_store._collection.count() == 0:
    vector_store.add_documents(documents)
    
retriever = vector_store.as_retriever(
    search_kwargs={"k": 5} #how many relevant info we want to consider
)