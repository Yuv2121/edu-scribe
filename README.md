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

## 💡 Our Solution: A Multi-Agent Pipeline
Edu-Scribe uses a team of specialized AI agents, orchestrated by the Google Agent Development Kit (ADK), to simulate an expert pedagogical review process.

Edu-Scribe is an "insight engine" that provides this missing "why." It uses a multi-agent team  to run 
an observable analysis pipeline, giving educators a concrete, actionable critique of a student's 
reasoning process.    
Example Flow: 
1. Educator: "Analyze student response #42." 
2. Edu-Scribe: 
• Ingests student response #42: "I think the answer is 60 because 6x10 is 60, just like 
5x10 is 50." 
• Analyzes this response against its pedagogical knowledge base. 
• Synthesizes a critique. 
3. Final Output (Cognitive Critique): "The student's answer is correct, but the reasoning 
exhibits a Faulty Analogical Leap. While the 5x10 analogy is correct arithmetically, the 
student is applying a surface-level pattern without confirming the underlying mathematical 
rule. Recommend a follow-up question to probe their understanding of this rule." 

---

## ⚙️ System Architecture
The project is built as a hierarchical multi-agent system using Google's Agent Development Kit 
(ADK). A "Coordinator" LlmAgent delegates to a "Sequential Pipeline" SequentialAgent  to ensure the 
reasoning process is robust, repeatable, and observable. 

### The Agent Team
| Agent | Role | Implementation |
| :--- | :--- | :--- |
| **IngestionAgent** | **The Librarian.** Fetches raw student data from the dataset. | Uses `dataset_loader` tool to read `student_data.csv`. |
| **CognitiveAnalysisAgent** | **The Brain.** Diagnoses the root cause of the error using academic theory. | Uses `pedagogy_search` (RAG) to find relevant frameworks (e.g., "Bloom's Taxonomy"). |
| **SynthesisAgent** | **The Writer.** Translates the technical diagnosis into a helpful critique. | Uses Gemini to write a constructive note for the teacher. |



1.  **Input:** User provides a `Student ID`.
2.  **Tool Call:** `IngestionAgent` calls `dataset_loader` to retrieve the specific question and the student's wrong answer.
3.  **RAG Lookup:** `CognitiveAnalysisAgent` analyzes the text and calls `pedagogy_search`. This performs a **TF-IDF similarity search** against a local corpus of pedagogical theory (`corpus/pedagogy.txt`).
4.  **Output:** `SynthesisAgent` combines the student data + the pedagogical theory to generate the final report.


---

## 🏆 ADK Concepts & Scoring Compliance

This project was built to demonstrate mastery of the ADK ecosystem. We explicitly implemented the following concepts to meet the Kaggle Capstone criteria:

| Requirement | Status | Implementation Details |
| :--- | :---: | :--- |
| **Track: Agents for Good** | ✅ | Project provides pedagogical insights for educators. |
| **Core Concept 1: Multi-agent system** | ✅ | A 4-agent team (Orchestrator, Ingestion, CognitiveAnalysis, Synthesis) using a `SequentialAgent` workflow. |
| **Core Concept 2: Custom Tools** | ✅ | `DatasetLoader` to load student data and `PedagogyVectorstore` (RAG) to search our internal academic corpus. |
| **Core Concept 3: Built-in Tools** | ✅ | `Google Search` is used by the `CognitiveAnalysisAgent` for dynamic, real-time knowledge retrieval. |
| **Core Concept 4: Sessions & Memory** | ✅ | `InMemorySessionService` is used to pass state (e.g., `student_response`, `retrieved_framework`) between agents. |
| **Core Concept 5: Agent Evaluation** | ✅ | We built a "Golden Set" of 15 test cases. The project was formally evaluated using `adk web` and `adk eval`. |
| **Core Concept 6: Observability** | ✅ | Our sequential, state-passing architecture makes the agent's reasoning fully traceable in the `adk web` UI. |
| **Bonus 1: Use of Gemini** | ✅ | The core `CognitiveAnalysisAgent` is powered by the latest **Gemini model** for maximum reasoning quality. |
| **Bonus 2: Agent Deployment** | ✅ | The entire system is deployed as a public endpoint on Google Cloud Run using `adk deploy cloud_run`. |
| **Bonus 3: YouTube Video** | ✅ | A 3-minute demo video is linked in the submission. |

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



