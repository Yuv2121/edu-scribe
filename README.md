# Edu-Scribe

A small multi-agent educational analysis toolkit. This repo contains a simple orchestration of three agents (Ingestor, Analyst, Synthesizer) built on top of the Google ADK and a small local RAG toolset for pedagogical lookups.

This repository is prepared for sharing with reviewers. It intentionally excludes secrets — please do not commit your `.env` file.

## What’s included
- `agent.py` - the agent definitions and pipeline (root_agent).
- `run_terminal.py` - interactive terminal runner (falls back to an in-memory runner if needed).
- `run_with_env.py` - helper that loads `.env` then runs `run_terminal.py`.
- `tools.py` - helper tools: `dataset_loader` and `pedagogy_search`.
- `scripts/test_agent.py` - non-interactive test that sends a short message and prints events.
- `scripts/list_models.py` - lists available GenAI models for your account.
- `corpus/pedagogy.txt` - local pedagogy snippets used by the RAG tool.
- `.env.example` - environment example (place your real API key into local `.env`, do NOT commit it).
- `.gitignore` - ignores `.env`, caches and common artifacts.

## Quick start (for reviewers)
These steps assume Python 3.11+ is installed.

1. Clone the repository or download & unzip the submitted artifact.
2. Create a local `.env` file (do not commit it) with your Google API key:

```text
GOOGLE_API_KEY=your_real_api_key_here
```

3. Install dependencies (recommended in a venv):

```powershell
python -m pip install -r requirements.txt
```

4. Run the non-interactive test (prints a short exchange):

```powershell
python .\scripts\test_agent.py
```

5. Or run interactively (the helper loads `.env` for you):

```powershell
python .\run_with_env.py
# then type messages (or 'exit' to quit)
```

Notes for reviewers:
- If you do not want to make real API calls, remove/rename `.env` and the scripts will show friendly messages.
- The pipeline uses `dataset_loader` which expects a `student_data.csv` file in the repo root. If this CSV has different column names, update `tools.dataset_loader` accordingly.

## Security
- `.env` is excluded via `.gitignore`. If a secret was accidentally committed, rotate the key immediately and contact the repository owner to rewrite history.

## Hybrid retrieval & strict mode

The `CognitiveAnalysisAgent` implements hybrid retrieval: it always consults the local pedagogy vectorstore (the `pedagogy_search` tool in `tools.py`) and will optionally use the ADK `GoogleSearch` tool when available to broaden results.

- By default the import of `GoogleSearch` is conditional so the project runs even when the optional dependency or credentials are missing.
- To enforce that `GoogleSearch` must be present at runtime (for strict evaluation or CI), set the environment variable `EDUSCRIBE_STRICT_GOOGLESEARCH=1`. When strict mode is enabled the runner will exit with a clear message if `GoogleSearch` is not available.

How to enable strict mode locally (PowerShell):

```powershell
$env:EDUSCRIBE_STRICT_GOOGLESEARCH = "1"
python .\run_with_env.py
```

How to enable strict mode in GitHub Actions (example snippet):

```yaml
env:
	EDUSCRIBE_STRICT_GOOGLESEARCH: '1'
	GOOGLE_API_KEY: ${{ secrets.GOOGLE_API_KEY }}
```

Quick checks:
- Use the helper to verify availability: `python .\scripts\check_tools.py` (it prints the status of `GoogleSearch` and respects the strict-mode env var).
- If you don't want external calls during review, unset `GOOGLE_API_KEY` or leave `EDUSCRIBE_STRICT_GOOGLESEARCH` unset/`0`. The agent will still run using the local pedagogy RAG.

## What I verified before sharing
- Syntax & imports: `python -m compileall .` passed.
- Dependencies: `pip install -r requirements.txt` completed on my environment.
- Basic E2E: `scripts/test_agent.py` runs and completes (requires a valid `GOOGLE_API_KEY` in `.env`).
 - Hybrid retrieval: `scripts/check_tools.py` was used to validate the conditional `GoogleSearch` import and the `EDUSCRIBE_STRICT_GOOGLESEARCH` enforcement locally.

## How to provide the GitHub link
1. Create a repository on GitHub (public or private per competition rules).
2. Upload the project files (via `git push` or GitHub web upload).
3. Ensure `.env` is not included in the repo (check the file list for `.env`).
4. Copy the repository URL and paste it into your competition form.

If you want, I can generate a ZIP of the repository prepared for upload (it will exclude `.env`). Tell me and I'll produce it for you to download.

---
If anything is unclear or you want me to generate the ZIP/patch now, I can create it and give you the download path. Good luck with the competition!
