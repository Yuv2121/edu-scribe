import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_base_path():
    """Get the base directory, accounting for serverless environments"""
    # Check multiple possible locations
    possible_paths = [
        os.path.dirname(os.path.abspath(__file__)),
        os.getcwd(),
        "/tmp",
        os.path.expanduser("~"),
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    return os.path.dirname(os.path.abspath(__file__))

# --- Global State for RAG ---
corpus_text = []
corpus_path = os.path.join(get_base_path(), "corpus", "pedagogy.txt")

if os.path.exists(corpus_path):
    try:
        with open(corpus_path, "r", encoding="utf-8") as f:
            corpus_text = [line.strip() for line in f.readlines() if line.strip()]
    except Exception as e:
        print(f"Warning: Could not load corpus from {corpus_path}: {e}")
        corpus_text = []
else:
    print(f"Warning: Corpus file not found at {corpus_path}")
    corpus_text = []

# Initialize vectorizer only if we have corpus data
vectorizer = TfidfVectorizer()
tfidf_matrix = None

if corpus_text:
    try:
        tfidf_matrix = vectorizer.fit_transform(corpus_text)
    except Exception as e:
        print(f"Warning: Could not create TF-IDF matrix: {e}")
        tfidf_matrix = None

def dataset_loader(student_id: int) -> dict:
    """
    Retrieves a student's response from the local CSV dataset.
    
    Args:
        student_id (int): The row index of the student to analyze (e.g., 0 to 100).
    
    Returns:
        dict: Contains 'status' and 'response_text' or 'error'.
    """
    try:
        # Try multiple file paths
        possible_csv_paths = [
            "student_data.csv",
            os.path.join(get_base_path(), "student_data.csv"),
            os.path.join(get_base_path(), "..", "student_data.csv"),
        ]
        
        csv_path = None
        for path in possible_csv_paths:
            if os.path.exists(path):
                csv_path = path
                break
        
        if not csv_path:
            return {
                "status": "error",
                "message": f"student_data.csv not found in any of: {possible_csv_paths}"
            }
        
        df = pd.read_csv(csv_path)
        
        if student_id >= len(df):
            return {
                "status": "error",
                "message": f"Student ID {student_id} out of range. Dataset has {len(df)} records."
            }
        
        row = df.iloc[student_id]
        # Combine relevant columns into one text
        question_id = row.get('QuestionId', 'N/A')
        construct_name = row.get('ConstructName', 'N/A')
        question_text = row.get('QuestionText', 'N/A')
        
        text = f"Question ID: {question_id}\nConstruct: {construct_name}\nQuestion: {question_text}"
        
        return {
            "status": "success",
            "response_text": text,
            "student_id": student_id
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error loading student data: {str(e)}"
        }

def pedagogy_search(query: str) -> dict:
    """
    Searches the internal pedagogy knowledge base for relevant frameworks.
    
    Use this to find academic concepts (e.g., 'Bloom's Taxonomy') that explain a student's error.
    
    Args:
        query (str): The search topic (e.g., 'logical fallacy in algebra').
    
    Returns:
        dict: Contains search results or error message
    """
    if not corpus_text:
        return {
            "status": "error",
            "message": "Pedagogy corpus is empty or not loaded."
        }
    
    if tfidf_matrix is None:
        return {
            "status": "error",
            "message": "TF-IDF matrix could not be created."
        }
    
    try:
        query_vec = vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
        
        # Get top 1 result index
        best_idx = similarities.argmax()
        
        if similarities[best_idx] < 0.1:  # Threshold for relevance
            return {
                "status": "ambiguous",
                "message": "No relevant framework found.",
                "similarity_score": float(similarities[best_idx])
            }
        
        return {
            "status": "success",
            "framework_snippet": corpus_text[best_idx],
            "source": "pedagogy.txt",
            "similarity_score": float(similarities[best_idx])
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error during pedagogy search: {str(e)}"
        }
