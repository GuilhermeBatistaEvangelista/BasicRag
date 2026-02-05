import pandas as pd
import os


class FileHandler():
	def __init__(self):
		super().__init__()

		self.path = "dataset"
		self.csv_files = []
		self.context = None
	

	def searchFiles(self):
		self.csv_files = []
		for root, dirs, files in os.walk(self.path):
			for file in files:
				if file.endswith('.csv'):
					self.csv_files.append(os.path.join(root, file))
		if len(self.csv_files) > 0:
			return True
		return False

	
	def processFiles(self):
		documents = []
		for file in self.csv_files:
			df = pd.read_csv(file, sep=";", low_memory=False)
			#df = pd.read_csv(file)
			
			for i, row in df.iterrows():
				text = ", ".join([f"{col}: {str(val)}" for col, val in row.items()])
				documents.append(text)

		self.context = documents

	def getContest(self):
		return self.context

	def listFiles(self):
		for file in self.csv_files:
			print(file)
