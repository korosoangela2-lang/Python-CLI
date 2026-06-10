import importlib
import inspect
import tempfile
from pathlib import Path
import traceback

modules = ["tests.test_app", "tests.test_services"]

results = []

for mod_name in modules:
    try:
        mod = importlib.import_module(mod_name)
    except Exception as e:
        print(f"ERROR importing {mod_name}: {e}")
        traceback.print_exc()
        results.append((mod_name, 'import-error', str(e)))
        continue

    for name, obj in inspect.getmembers(mod, inspect.isfunction):
        if not name.startswith('test_'):
            continue
        print(f"Running {mod_name}.{name}...", flush=True)
        sig = inspect.signature(obj)
        try:
            if len(sig.parameters) == 0:
                obj()
            elif len(sig.parameters) == 1:
                with tempfile.TemporaryDirectory() as td:
                    tmp = Path(td)
                    obj(tmp)
            else:
                # For unexpected signatures, skip
                print(f"  SKIP: {name} (unexpected parameters)")
                results.append((f"{mod_name}.{name}", 'skip', 'unexpected parameters'))
                continue
            print(f"  PASS: {name}")
            results.append((f"{mod_name}.{name}", 'pass', None))
        except AssertionError as ae:
            print(f"  FAIL: {name} -> {ae}")
            traceback.print_exc()
            results.append((f"{mod_name}.{name}", 'fail', str(ae)))
        except Exception as e:
            print(f"  ERROR: {name} -> {e}")
            traceback.print_exc()
            results.append((f"{mod_name}.{name}", 'error', str(e)))

print('\nSummary:')
passes = [r for r in results if r[1]=='pass']
fails = [r for r in results if r[1]=='fail']
errors = [r for r in results if r[1] in ('error','import-error')]
print(f"  Passed: {len(passes)}")
print(f"  Failed: {len(fails)}")
print(f"  Errors: {len(errors)}")

if fails or errors:
    raise SystemExit(1)
else:
    print('All tests passed')
