import importlib
import google.adk as adk

print('adk dir:', [n for n in dir(adk) if not n.startswith('_')])
try:
    runners = importlib.import_module('google.adk.runners')
    print('runners dir:', [n for n in dir(runners) if not n.startswith('_')])
except Exception as e:
    print('runners import failed:', e)
