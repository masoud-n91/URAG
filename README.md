# Chatter: Your Friendly Chatbot Assistant

Chatter is a Python-based chatbot assistant designed to help you build and manage a chatbot with ease. It leverages powerful machine learning models for natural language processing and offers a variety of utilities to handle documents and web data.

## Features

- **Standalone Query Creation**: Automatically reformulates user queries to be standalone, improving the clarity and context for the chatbot.
- **Final Response Generation**: Generates comprehensive responses based on user queries, chat history, and top responses.
- **Document Handling**: Reads and processes `.docx` files to extract and preprocess text.
- **Web Scraping**: Extracts URLs and scrapes web content to include in documents.
- **Vector Database**: Creates and manages a vector database for efficient document retrieval using Annoy index.
- **Memory Management**: Keeps track of chat history and recent interactions to maintain context in conversations.

## Installation

To use Chatter, you need to have the following dependencies installed:

```bash
pip install -r requirements.txt
```

## Usage
### Initializing Chatter
Create an instance of the Chatter class with your API key and optional parameters. You also need to specify a folder in which you have information (in docx format) that chatbot can use to asnwer the queries accordingly. 

```python
from chatter_rag import Chatter, Memory

data_path = "path/to/your/docx/files.docx"
api_key = "your_groq_api_key"
chatter = Chatter(api_key = api_key, file_path = data_path)

memory = Memory()
```

### Updating vector database
First you always need to create or update your database according to the docx file in you data folder. This part of code can be run only once. If documents are changed you need to run this part again.
```python
_, document_embeddings = chatter.find_documents(data_path)
_ = chatter.create_vector_database(document_embeddings, path = model_path)
```

### Creating Standalone Queries
To have separated chat for each user, you need to specify a unique session_id to each chat. Generate a standalone query from a user query and chat history:

```python
# choose on of the following as your memory
str_mem = memory.get_last_mem(session_id)   # only use the last query and response of the chat
str_mem5 = memory.get_5_mem(session_id)     # use the last 5 sets of queries and responses
standalone_query = chatter.create_standalone_query("user query", str_mem)
```

### Embed the standalone query
To be able to seach the database using the standalone query, you also need to embed it.

```python
query_embedding = chatter.model.encode(chatter.preprocess_text(standalone_query))
```

### Find and load the ann file
The vector database is mustbe loaded first.

```python
ann_file = chatter.find_ann_files(model_path)
dimention, _ = ann_file.split('.')

ann_dir = model_path + ann_file
index = chatter.load_index(ann_dir, int(dimention))
```

### Find indices of similar documents to the standalone query
Some parts of the document are more related to the query. This part will hep you find those. Hete top 10 responses (top_k=10) is the default.
```python
similar_docs_indices, _ = chatter.get_similar_documents(query_embedding, index, top_k=10)
```

### Fetch all the documents
Now that you have the indices, you need to load the document to find that which part of the document is more related to the query:

```python
documents, _ = chatter.find_documents(data_path)
top_responses = [documents[i] for i in similar_docs_indices]
```

### Generate final response
The top responses and the query along with the last 5 sets of queries and responses must be passed to chatter to produce the final response.
```python
final_response = chatter.generate_final_response(top_responses, user_query, str_mem5)
```

### Update chat history
At the end, the memory must be updated with the query and the final response in the correct session_id.
```python
memory.update_chat(session_id, user_query, final_response)
```

### Memory clearance
If needed, you can clear the memory.
```python
memory.remove_mem(session_id)
```

### To sum up
```python
from chatter import Chatter, Memory

data_path = "path/to/your/docx/files.docx"
api_key = "your_groq_api_key"
chatter = Chatter(api_key = api_key, file_path = data_path)

memory = Memory()

# choose on of the following as your memory
str_mem = memory.get_last_mem(session_id)   # only use the last query and response of the chat
str_mem5 = memory.get_5_mem(session_id)     # use the last 5 sets of queries and responses
standalone_query = chatter.create_standalone_query(user_query, str_mem)

query_embedding = chatter.model.encode(chatter.preprocess_text(standalone_query))

ann_file = chatter.find_ann_files(model_path)
dimention, _ = ann_file.split('.')

ann_dir = model_path + ann_file
index = chatter.load_index(ann_dir, int(dimention))

similar_docs_indices, _ = chatter.get_similar_documents(query_embedding, index, top_k=10)

documents, _ = chatter.find_documents(data_path)
top_responses = [documents[i] for i in similar_docs_indices]

final_response = chatter.generate_final_response(top_responses, user_query, str_mem5)

memory.update_chat(session_id, user_query, final_response)
```


