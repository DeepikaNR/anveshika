# anveshika
Bi-lingual web search engine

**Functionality:

1. flask_server.py : Extract the user query from the HTML form and fire a search session.
2. query_main.py : Detects the query language. Accordingly, carries out linguistic pre-processing of the query. Invokes a free text query search and returns the ranked URLs.
3. pipeline_processor.py : Tokenises, removes stop words and lemmatizes the input file. Returns stream of terms.
4. query_engine.py : Represents the query and matching documents as vectors. Calculates the cosine similarity measure for each pair of docuemnt and query. Ranks them in descending order.
5. indexer_main.py : Reads the harvest files from known location to convert them to stream of terms with the help of pipeline_processor.py. Writes the inverted index structure, idf, document map of tf to cassandra.

Indexing is done as a continuous background job(Step 4). When a user enters a query, only steps 1-4 are carried out.

(The HTML frontend and Kannada lemmatizer are not included. 
Refer for the web crawler code.)

