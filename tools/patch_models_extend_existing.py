import os
import re

MODELS_DIR = "app/models"

for filename in os.listdir(MODELS_DIR):
    if not filename.endswith(".py"):
        continue
    if filename == "__init__.py":
        continue

    path = os.path.join(MODELS_DIR, filename)

    with open(path, "r") as f:
        content = f.read()

    # Skip if already patched
    if "__table_args__" in content:
        continue

    # Insert after __tablename__
    pattern = r'(__tablename__\s*=\s*["\'].*?["\'])'
    replacement = r'\1\n    __table_args__ = {"extend_existing": True}'

    new_content, count = re.subn(pattern, replacement, content, count=1)

    if count > 0:
        with open(path, "w") as f:
            f.write(new_content)
        print(f"✅ Patched {filename}")
    else:
        print(f"⚠️  Skipped {filename} (no __tablename__)")

print("🎉 Done. Restart Uvicorn.")
