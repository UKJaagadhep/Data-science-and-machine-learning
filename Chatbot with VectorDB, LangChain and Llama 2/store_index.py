from src.helper import load_pdf, text_split, download_hugging_face_embeddings
from langchain.vectorstores import Pinecone
from langchain_pinecone import PineconeVectorStore
from pinecone.grpc import PineconeGRPC
from pinecone import ServerlessSpec
import pinecone
from dotenv import load_dotenv
import os

load_dotenv()

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')

extracted_data = load_pdf("data/")
text_chunks = text_split(extracted_data)
embeddings = download_hugging_face_embeddings()

pc = PineconeGRPC()

index_name="medical-bot"

if index_name not in pc.list_indexes().names():
    pc.create_index(
        name = index_name,
        dimension = 384,
        metric = "cosine",
        spec = ServerlessSpec(
            cloud = 'aws',
            region = 'us-east-1'
        )
    )

index = pc.Index(index_name) #Accessing pinecone index

docsearch = PineconeVectorStore.from_documents(
    documents = text_chunks,
    index_name = index_name,
    embedding = embeddings,
    namespace = "medical"
)
