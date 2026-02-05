## What is it?
This project implements a basic Retrieval-Augmented Generation (RAG) pipeline, using a simple CLI loop for interactive Q&A.
1. Load structured data (CSV) from the /dataset folder.
2. Convert to text.
3. Embed and store in vector DB.
4. Get user query.
5. Retrieve relevant context.
6. Query an LLM with that context.
## Documentation

### Requirements

This project has the following dependencies, as shown in `requirements.txt`:
- [pandas](https://pandas.pydata.org/)
- [numpy](https://numpy.org/)
- [python-dotenv](https://github.com/theskumar/python-dotenv)
- [langchain](https://www.langchain.com/)
- [chromadb](https://github.com/chroma-core/chroma)
### Quick Start

To get started, create and configure the variables in the `.env` file as per example in `example.env`. The context data must be added to a `dataset` folder in the directory.

The project can be set up either by installing the dependencies with a package manager and running `main.py`, or by using [Docker](https://www.docker.com/) to run it in an interactive shell.
