import faiss
import os
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.llms import OpenAI

class VectorStore:
    def __init__(self):
        self.index = None
        self.embeddings = OpenAIEmbeddings()
        self.text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        self.vector_db_path = "local_vector_db"
        
        # Load existing vector database if available
        if os.path.exists(self.vector_db_path):
            self.index = FAISS.load_local(self.vector_db_path, self.embeddings)
        else:
            self.index = None

    def store_file(self, file_content, file_name):
        # Split the file into chunks
        text_chunks = self.text_splitter.split_text(file_content.decode('utf-8'))
        
        # Generate embeddings for the text chunks
        doc_embeddings = self.embeddings.embed_documents(text_chunks)
        
        # Create a new FAISS index if it doesn't exist
        if self.index is None:
            self.index = FAISS(doc_embeddings)
        else:
            self.index.add_documents(doc_embeddings)
        
        # Save the FAISS index
        self.index.save_local(self.vector_db_path)

    def query(self, user_query):
        if self.index is None:
            return "No files uploaded yet."
        
        # Generate the query embedding
        query_embedding = self.embeddings.embed_query(user_query)
        
        # Find similar documents
        result = self.index.similarity_search_with_score(query_embedding)
        
        # Return the most relevant chunk
        if result:
            return result[0][0].page_content
        return "No relevant information found."
