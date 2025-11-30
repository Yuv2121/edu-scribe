import os
import zipfile

root = os.path.dirname(os.path.dirname(__file__))
zip_path = os.path.join(os.path.dirname(root), 'edu-scribe_pyzip.zip')
exclude_names = {'.env', '.git'}

with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
    for dirpath, dirnames, filenames in os.walk(root):
        # Skip .git directories anywhere
        if '.git' in dirpath.split(os.sep):
            continue
        rel_dir = os.path.relpath(dirpath, root)
        for f in filenames:
            if f == '.env':
                continue
            full = os.path.join(dirpath, f)
            arcname = os.path.normpath(os.path.join(rel_dir, f)) if rel_dir != '.' else f
            z.write(full, arcname)

print('Created zip:', zip_path)
