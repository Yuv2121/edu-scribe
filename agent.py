import os
from google.adk.agents import Agent, SequentialAgent
# google-adk may not expose `google.adk.model` in all versions; Model isn't used below
# so import it defensively to avoid hard import errors during module import.
try:
    from google.adk.model import Model
except Exception:
    Model = None
from tools import dataset_loader, pedagogy_search

# Load API Key
api_key = os.getenv("GOOGLE_API_KEY")
# Configure the Model: use a currently supported text-only Gemini Flash model
# (listed by the GenAI API). Using the 'models/...' canonical name avoids
# version mismatch errors like the NOT_FOUND seen with older model ids.
# ADK model registry typically expects the short model name (without the
# 'models/' prefix). Use the short form to match the ADK registry lookup.
model_config = "gemini-2.5-flash"

# --- Agent 1: The Ingestor ---
# Purpose: Get the raw data into the session state
ingestion_agent = Agent(
    name="IngestionAgent",
    model=model_config,
    tools=[dataset_loader],
    instruction="""
    You are a data retrieval specialist. 
    1. Your input will be a 'student_id' from the user.
    2. Call the 'dataset_loader' tool with this ID.
    3. If successful, SAVE the 'response_text' into the session context/memory for the next agent.
    4. Output a confirmation: "Data loaded for Student ID [X]."
    """
)

# --- Agent 2: The Analyst (The Brain) ---
# Purpose: Analyze the data using RAG and reasoning
analysis_agent = Agent(
    name="CognitiveAnalysisAgent",
    model=model_config, # Use a smarter model if possible, like Pro
    tools=[pedagogy_search], 
    instruction="""
    You are a Pedagogical Expert.
    1. Read the 'response_text' found in the conversation history.
    2. Analyze the student's error. Formulate a search query for a pedagogical framework (e.g. 'math misconception linear').
    3. Call the 'pedagogy_search' tool to find a relevant academic theory.
    4. Output a structured analysis: "Diagnosis: [Name of Error]. Theory: [Framework found]."
    """
)

# --- Agent 3: The Synthesizer (The Writer) ---
# Purpose: Format the output for the teacher
synthesis_agent = Agent(
    name="SynthesisAgent",
    model=model_config,
    instruction="""
    You are a Helpful Assistant for Teachers.
    1. Read the 'Diagnosis' and 'Theory' from the previous agent.
    2. Write a polite, constructive 'Cognitive Critique' for the teacher.
    3. Do not use jargon. Explain the student's thought process simply.
    """
)

# --- The Pipeline (Sequential Orchestration) ---
# This is the root agent that the user talks to
root_agent = SequentialAgent(
    name="EduScribeTeam",
    description="A team of agents that analyzes student work.",
    sub_agents=[ingestion_agent, analysis_agent, synthesis_agent]
)

# Setup for local running (Standard ADK boilerplate)
if __name__ == "__main__":
    from google.adk import run_agent
    run_agent(root_agent)