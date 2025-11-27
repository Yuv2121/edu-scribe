import os
import sys

# 1. Force the script to see your current folder
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 2. Import your agent (Assuming your agent file is named 'agent.py' and the agent variable is 'root_agent')
try:
    from agent import root_agent
except ImportError:
    print("❌ ERROR: Could not find 'root_agent' in 'agent.py'.")
    print("Check: Is your file named agent.py? Did you name the variable 'root_agent'?")
    sys.exit(1)

# 3. Run it interactively in the terminal
if __name__ == "__main__":
    print("\n" + "="*40)
    print(" 🤖 EDU-SCRIBE AGENT (TERMINAL MODE)")
    print("="*40 + "\n")
    print("Type your request below (or 'exit' to quit).")
    # Check for API key early to provide a friendly message instead of a long traceback
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key or api_key.strip() == "YOUR_GOOGLE_API_KEY_HERE":
        print("\n⚠️  GOOGLE_API_KEY is not set. The ADK needs an API key to call the model.")
        print("Add your key to a local `.env` (or set the environment variable) and restart.")
        print("If you want to run the agent without network/model calls, set up mocks or a local test runner.")
        sys.exit(1)

    # Try to import a convenience `run_agent` helper if the installed ADK exposes it.
    try:
        from google.adk import run_agent  # some ADK releases expose this
    except Exception:
        # Otherwise fall back to an interactive loop using InMemoryRunner from runners
        try:
            from google.adk.runners import InMemoryRunner
        except Exception as e:
            print("❌ ERROR: Could not find a runner in google.adk.\nDetails:", e)
            sys.exit(1)

        import asyncio

        runner = InMemoryRunner(agent=root_agent)

        try:
            while True:
                user_input = input("You: ")
                if user_input.strip().lower() in ("exit", "quit"):
                    break
                # run_debug will print events by default and also return them
                asyncio.run(runner.run_debug(user_input))
        finally:
            # Close runner cleanly
            try:
                asyncio.run(runner.close())
            except Exception:
                pass