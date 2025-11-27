import os
from google.genai.client import Client

# Load .env
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

print('Using GOOGLE_API_KEY from environment:', bool(os.getenv('GOOGLE_API_KEY')))

c = Client()
try:
    models = c.models.list()
    print(f'Found {len(models)} models:')
    for m in models:
        # model object may have id or name attribute
        print('-', getattr(m, 'name', getattr(m, 'model_id', repr(m))))
except Exception as e:
    print('Error listing models:', e)
    raise
