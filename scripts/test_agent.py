import os
import asyncio
import traceback

# Load .env into environment (if present)
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
if os.path.exists(env_path):
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' not in line:
                continue
            k, v = line.split('=', 1)
            os.environ.setdefault(k.strip(), v.strip())

print('GOOGLE_API_KEY present:', bool(os.getenv('GOOGLE_API_KEY')))

try:
    # Ensure project root is on sys.path so we can import agent.py
    import sys
    project_root = os.path.dirname(os.path.dirname(__file__))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    from agent import root_agent
    from google.adk.runners import InMemoryRunner

    runner = InMemoryRunner(agent=root_agent)

    async def run_test():
        try:
            print('Running run_debug with message: "Hello from automated test"')
            events = await runner.run_debug('Hello from automated test')
            print(f'Run complete. {len(events)} events returned')
            for i, ev in enumerate(events, 1):
                author = getattr(ev, 'author', None)
                invocation_id = getattr(ev, 'invocation_id', None)
                content = getattr(ev, 'content', None)
                print(f'Event {i}: author={author}, invocation_id={invocation_id}, content={content}')
        finally:
            try:
                await runner.close()
            except Exception:
                pass

    asyncio.run(run_test())

except Exception:
    traceback.print_exc()
    raise
