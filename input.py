import os
from query import QueryHandler
from read_files import FileHandler

class inputHandler():
	def __init__(self):
		super().__init__()

		self.state = None
		# Menu, Define API, Chat
		#Options: Chat, Reload files, change API?
		self.query = QueryHandler()
		self.files = FileHandler()
		self.setup()

	def setup(self):
		if not self.files.searchFiles():
			print("No files on /dataset")
			return False
		
		os.system('clear')
		print("File(s):")
		self.files.listFiles()

		print("Processing file(s)...")
		self.files.processFiles()

		print("Embedding file(s)...")
		self.query.embedContext(self.files.getContest())
		print("Context embedded.")
		os.system('clear')
		return True
	
	def show(self):
		print("Loaded Files: ")
		self.files.listFiles()

		print("\n		Enter 'exit'|'close'|'quit'|'end'  to end execution.\n")
		
	def read(self):
		text = input()

		if text.strip().upper() in  ["EXIT", "CLOSE", "QUIT", "END"]:
			return False
		
		self.showQuery(text)
		return True
	
	def showQuery(self, text):
		os.system('clear')
		print(f"Waiting response...")

		context = self.query.getRevelantContext(text)
		prompt = f"Given this context:\n{context}\n\n {text}"
		print(prompt)

		response = self.query.runQuery(prompt)

		os.system('clear')

		print(f"Question:{text}\n Answer: {response.content}")
