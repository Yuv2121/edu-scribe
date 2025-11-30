import os
import importlib

# Load .env if present
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
if os.path.exists(env_path):
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' not in line:
                continue
            k,v = line.split('=',1)
            os.environ.setdefault(k.strip(), v.strip())

print('Checking for optional tools...')
try:
    agent = importlib.import_module('agent')
    gs = getattr(agent, 'GoogleSearch', None)
    # Optionally allow a local stub for offline testing/demos
    use_local = os.getenv('EDUSCRIBE_USE_LOCAL_GOOGLESEARCH','').strip() in ('1','true','True')
    if use_local and not gs:
        try:
            from .google_search_stub import GoogleSearch as LocalGoogleSearch
        except Exception:
            # fallback: try relative import for direct script execution
            from scripts.google_search_stub import GoogleSearch as LocalGoogleSearch
        # attach the local stub into the agent module so checks and downstream
        # logic detect it as present
        setattr(agent, 'GoogleSearch', LocalGoogleSearch)
        gs = LocalGoogleSearch
        print('Using local GoogleSearch stub for offline testing.')
    print('GoogleSearch available:', bool(gs))
except Exception as e:
    print('Could not import agent module to check tools:', e)
    raise

strict = os.getenv('EDUSCRIBE_STRICT_GOOGLESEARCH','').strip() in ('1','true','True')
if strict and not gs:
    print('\nStrict mode enabled and GoogleSearch missing. Exiting with non-zero status.')
    raise SystemExit(2)
else:
    print('\nTool check complete.')
