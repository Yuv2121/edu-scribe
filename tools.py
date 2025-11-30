import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# --- Global State for RAG ---
# We load this once when the agent starts
# Initialize safely to an empty list to avoid syntax/runtime issues
corpus_text = []
corpus_path = os.path.join(os.path.dirname(__file__), "corpus", "pedagogy.txt")
if os.path.exists(corpus_path):
    with open(corpus_path, "r", encoding="utf-8") as f:
        # Split by newlines to create "chunks"
        corpus_text = [line.strip() for line in f.readlines() if line.strip()]

vectorizer = TfidfVectorizer()
# Only fit if we have data
if corpus_text:
    tfidf_matrix = vectorizer.fit_transform(corpus_text)

def dataset_loader(student_id: int) -> dict:
    """
    Retrieves a student's response from the local CSV dataset.
    Args:
        student_id (int): The row index of the student to analyze (e.g., 0 to 100).
    Returns:
        dict: Contains 'status' and 'response_text' or 'error'.
    """
    try:
        df = pd.read_csv("student_data.csv")
        if student_id >= len(df):
            return {"status": "error", "message": "Student ID out of range."}
        
        # Assuming the CSV has a column 'QuestionText' and 'AnswerValue' - ADJUST THESE NAMES TO YOUR CSV
        # Open the CSV in Excel first to check column names!
        # For Eedi dataset, typically 'QuestionText' and 'ConstructName' are useful.
        row = df.iloc[student_id]
        # We combine relevant columns into one text
        text = f"Question: {row.get('QuestionId', 'N/A')} \nStudent Answer: {row.get('AnswerValue', 'N/A')}"
        
        return {"status": "success", "response_text": text}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def pedagogy_search(query: str) -> dict:
    """
    Searches the internal pedagogy knowledge base for relevant frameworks.
    Use this to find academic concepts (e.g., 'Bloom's Taxonomy') that explain a student's error.
    Args:
        query (str): The search topic (e.g., 'logical fallacy in algebra').
    """
    if not corpus_text:
        return {"status": "error", "message": "Corpus is empty."}
    
    try:
        query_vec = vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
        # Get top 1 result index
        best_idx = similarities.argmax()
        
        if similarities[best_idx] < 0.1: # Threshold for relevance
            return {"status": "ambiguous", "message": "No relevant framework found."}
            
        return {
            "status": "success", 
            "framework_snippet": corpus_text[best_idx],
            "source": "pedagogy.txt"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}