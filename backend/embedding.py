import json
import os
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi
from sklearn.metrics.pairwise import cosine_similarity
import heapq
import nltk

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for the app

# Initialize sentence transformer model
model = SentenceTransformer('paraphrase-MiniLM-L12-v2')

# Load all embeddings from the JSONL file
def load_embeddings(file_path):
    embeddings = []
    with open(file_path, "r") as infile:
        for line in infile:
            data = json.loads(line)
            embeddings.append({
                "file_index": data["file_index"],
                "desc_index": data["desc_index"],
                "work_description": data["work_description"],
                "embedding": np.array(data["embedding"])  # Convert list back to NumPy array
            })
    return embeddings

# Load BM25 corpus (text descriptions)
def load_bm25_corpus(embeddings_data):
    corpus = []
    for entry in embeddings_data:
        tokens = nltk.word_tokenize(entry['work_description'].lower())
        corpus.append(tokens)
    return corpus

# BM25 search function
def bm25_search(bm25, query, corpus, top_n=100):
    query_tokens = nltk.word_tokenize(query.lower())
    scores = bm25.get_scores(query_tokens)
    top_indices = np.argsort(scores)[-top_n:][::-1]  # Get top N indices (descending)
    return [(corpus[i], scores[i], i) for i in top_indices]

# Cosine similarity search function
def cosine_similarity_search(user_query_embedding, embeddings_data, top_n=100):
    similarities = []
    
    for i, entry in enumerate(embeddings_data):
        similarity = cosine_similarity(
            user_query_embedding.reshape(1, -1), 
            entry["embedding"].reshape(1, -1)
        )[0][0]  # Flatten similarity value
        similarities.append((similarity, entry))
    
    # Find top N results with the highest cosine similarity
    top_results = heapq.nlargest(top_n, similarities, key=lambda x: x[0])
    
    return top_results

# Function to normalize scores between 0 and 1
def normalize(scores):
    min_val = min(scores)
    max_val = max(scores)
    return [(score - min_val) / (max_val - min_val) for score in scores]

def hybrid_search(user_query, embeddings_data, corpus, bm25, top_n=100, bm25_weight=0.4, cosine_weight=0.6):
    # Generate embedding for user query
    query_embedding = model.encode(user_query)
    
    # Perform BM25 search
    bm25_results = bm25_search(bm25, user_query, corpus, top_n)
    bm25_scores = [score for _, score, _ in bm25_results]
    normalized_bm25_scores = normalize(bm25_scores)
    
    # Perform cosine similarity search
    cosine_results = cosine_similarity_search(query_embedding, embeddings_data, top_n)
    cosine_scores = [similarity for similarity, _ in cosine_results]
    normalized_cosine_scores = normalize(cosine_scores)
    
    # Combine BM25 and Cosine Similarity scores
    combined_results = []
    for i in range(top_n):
        bm25_score = normalized_bm25_scores[i]
        cosine_score = normalized_cosine_scores[i]
        combined_score = bm25_weight * bm25_score + cosine_weight * cosine_score
        
        # Find the corresponding entry in embeddings_data using the index from BM25 results
        entry = embeddings_data[bm25_results[i][2]]  # Use index from BM25 results
        combined_results.append((combined_score, cosine_scores[i], entry))  # Store combined score and original cosine score

    # Sort combined results by cosine similarity score (second item in tuple) in descending order
    combined_results.sort(key=lambda x: x[1], reverse=True)

    # Return user ID and top results
    return combined_results

# Load embeddings data and prepare BM25 corpus
embeddings_file = "embeddings.jsonl"
embeddings_data = load_embeddings(embeddings_file)
corpus = load_bm25_corpus(embeddings_data)

# Initialize BM25 with the corpus
bm25 = BM25Okapi(corpus)

# Define the API endpoint
@app.route('/search', methods=['POST'])
def search():
    user_query = request.json.get('query')  # Get the query from the request
    if not user_query:
        return jsonify({"error": "Query not provided"}), 400
    
    # Perform hybrid search
    hybrid_results = hybrid_search(user_query, embeddings_data, corpus, bm25, top_n=100)
    
    # Extract user IDs from the results
    results_with_ids = [{"user_id": entry['file_index'], "description": entry['work_description']} for _, _, entry in hybrid_results]

    return jsonify(results_with_ids)  # Return the results as JSON

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
