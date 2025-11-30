# Edu-Scribe: The "Cognitive Insight" Engine for Educators
### *Google AI Agents Intensive Capstone Project | Track: Agents for Good*

![Status](https://img.shields.io/badge/Status-Prototype-success)
![Tech](https://img.shields.io/badge/Built%20with-Google%20ADK-blue)
![Model](https://img.shields.io/badge/Powered%20by-Gemini%201.5%20Flash-orange)

**Edu-Scribe** is a multi-agent AI system designed not for students, but for *educators*. It solves the "Cognitive Black Box" problem in AI education: the inability of current tools to explain *how* a student is reasoning, not just *what* they got wrong.

Instead of a simple grade, Edu-Scribe ingests student responses, cross-references them with a library of pedagogical frameworks, and produces a deep **Cognitive Critique**—giving teachers the "X-Ray vision" they need to teach critical thinking.

---

## 🧠 The Problem: The "Cognitive Black Box"
Current AI tutors optimize for the correct answer. They can tell a teacher that a student scored 60%, but they cannot explain the cognitive root cause of the errors.
* Is it a calculation error?
* Is it a deep-seated misconception?
* Is it a failure of analogical reasoning?

Without this insight, educators are blind to the learning process. Edu-Scribe provides this missing layer of observability.

## 💡 The Solution: A Multi-Agent Pipeline
Edu-Scribe uses a team of specialized AI agents, orchestrated by the Google Agent Development Kit (ADK), to simulate an expert pedagogical review process.

### The Agent Team
| Agent | Role | Implementation |
| :--- | :--- | :--- |
| **IngestionAgent** | **The Librarian.** Fetches raw student data from the dataset. | Uses `dataset_loader` tool to read `student_data.csv`. |
| **CognitiveAnalysisAgent** | **The Brain.** Diagnoses the root cause of the error using academic theory. | Uses `pedagogy_search` (RAG) to find relevant frameworks (e.g., "Bloom's Taxonomy"). |
| **SynthesisAgent** | **The Writer.** Translates the technical diagnosis into a helpful critique. | Uses Gemini to write a constructive note for the teacher. |

---

## ⚙️ Technical Architecture
The project follows a **Sequential Workflow** pattern. Data flows in one direction to ensure the reasoning is traceable and hallucination is minimized.

1.  **Input:** User provides a `Student ID`.
2.  **Tool Call:** `IngestionAgent` calls `dataset_loader` to retrieve the specific question and the student's wrong answer.
3.  **RAG Lookup:** `CognitiveAnalysisAgent` analyzes the text and calls `pedagogy_search`. This performs a **TF-IDF similarity search** against a local corpus of pedagogical theory (`corpus/pedagogy.txt`).
4.  **Output:** `SynthesisAgent` combines the student data + the pedagogical theory to generate the final report.


---

## 🛠️ Setup & Installation

### Prerequisites
* Python 3.10+
* A Google Cloud Project with an API Key for Gemini.

### 1. Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/edu-scribe.git](https://github.com/YOUR_USERNAME/edu-scribe.git)
cd edu-scribe
2. Install Dependencies
Bash

pip install -r requirements.txt
3. Configure Secrets
Create a .env file in the root directory. Do not share this file.

Ini, TOML

GOOGLE_API_KEY="your_actual_api_key_here"
🚀 How to Run
You can run the agent team interactively in your terminal.

Bash

# Recommended runner (loads .env automatically)
python run_with_env.py
Sample Interaction:

Plaintext

You: 15
(Agent fetches student #15 from data...)
(Agent searches pedagogy corpus for "geometry misconceptions"...)
(Agent synthesizes response...)

EduScribeTeam: 
Diagnosis: Visual Spatial Error.
Theory: The Van Hiele Levels of Geometric Thought suggest this student is operating at Level 0 (Visualization), judging shapes by appearance rather than properties.
Critique: The student has correctly identified the shape but failed to calculate the area because they assumed... [Full critique follows]
📂 Project Structure
agent.py: The core ADK definitions. Defines the 3 sub-agents and the SequentialAgent pipeline.

tools.py: Custom Python tools.

dataset_loader: Pandas-based tool to read student_data.csv.

pedagogy_search: Scikit-learn based RAG tool using TF-IDF vectorization.

student_data.csv: A dataset of real student math responses (Sourced from Eedi/Kaggle).

corpus/: Directory containing text files for the RAG knowledge base.

run_terminal.py: A lightweight runner script for local testing.

🏆 Scoring & ADK Mastery
This project was built for the Google AI Agents Intensive Capstone. It demonstrates:

✅ Multi-Agent Orchestration: Using SequentialAgent to manage complex workflows.

✅ Custom Tools: Implementing Python functions (dataset_loader) as AI tools.

✅ RAG (Retrieval Augmented Generation): Building a custom vector search engine for pedagogical context.

✅ Context & State: Passing information (response_text, diagnosis) between agents via session state.




