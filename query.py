import os

os.environ["CHROMA_TELEMETRY_ENABLED"] = "false"

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

import requests
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

class CustomEmbeddings(Embeddings):
    def __init__(self, embed_url, embed_name, api_key=None):
        self.embed_url = embed_url
        self.embed_name = embed_name
        self.api_key = api_key

    def embed_documents(self, texts):
        response = requests.post(
            f"{self.embed_url}embeddings",
            json={"input": texts, "model": self.embed_name},
            headers={"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
        )
        data = response.json()
        return [d["embedding"] for d in data["data"]]

    def embed_query(self, text):
        return self.embed_documents([text])[0]


import time
class QueryHandler():
	def __init__(self):
		super().__init__()

		self.key = None
		self.prompt = None
		self.llm = None
		
		self.embeddings_model = None
		self.vector_store = None
		self.setup()

	def setup(self):
		self.key = os.getenv('API_KEY')
		self.url = os.getenv("MODEL_URL")
		self.model = os.getenv("MODEL") or "local-model"

		self.llm = ChatOpenAI(
			model=self.model,
			api_key=self.key,
			base_url=self.url
		)

		self.embed_url = os.getenv("EMBEDDING_URL")
		self.embed_name = os.getenv("EMBEDDING_MODEL") or "text-embedding-nomic-embed-text-v1.5"

		embed_openai = (os.getenv("EMBED_WITH_OPENAI") or "").strip().upper() == "TRUE"
		if embed_openai:
			self.embeddings_model = OpenAIEmbeddings( model=self.embed_name, api_key=self.key, base_url=self.embed_url )
		else:
			self.embeddings_model = CustomEmbeddings(embed_url=self.embed_url, embed_name=self.embed_name, api_key=self.key)

		self.vector_store = Chroma(collection_name="rag_collection", embedding_function=self.embeddings_model)

		print("using: ", self.key, ", ", self.url)
	
	def getEmbed(self, texts):
		response = requests.post(
			f"{self.embed_url}embeddings",
			json={"input": texts, "model": self.embed_name},
			headers={"Authorization": f"Bearer {self.key}"} if self.key else {}
		)
		data = response.json()
		return [d["embedding"] for d in data["data"]]

	def embedContext(self, context):
		context = context[0:50]
		try:
			docs = [Document(page_content=text) for text in context]
			self.vector_store.add_documents(docs)
		except Exception as e:
			return print(f"Embedding error: {e}")

	def getRevelantContext(self, query, k=10):
		try:
			docs = self.vector_store.similarity_search(query, k=k)
			return [doc.page_content for doc in docs]
		except Exception as e:
			return f"Retrieval error: {e}"

	def runQuery(self, prompt):
		try:
			return self.llm.invoke(prompt)
		except Exception as e:
			return f"Query Error: {e}"
	
