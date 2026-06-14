import importlib, traceback

try:
    m = importlib.import_module('app.modules.auth.models')
    print('OK', hasattr(m, 'User'))
    if hasattr(m, 'User'):
        print(m.User)
except Exception:
    traceback.print_exc()
