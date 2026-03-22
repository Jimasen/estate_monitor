#!/usr/bin/env python3
import os
import re

# Root folder containing your models
MODELS_DIR = "./app/models"

# Regex to detect class definitions using Base
CLASS_REGEX = re.compile(r"^(class\s+\w+\(Base\):)", re.MULTILINE)

# Loop through all .py files in the models folder
for root, dirs, files in os.walk(MODELS_DIR):
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            with open(path, "r") as f:
                content = f.read()

            # Skip if __table_args__ already exists
            if "__table_args__" in content:
                continue

            # Find class definitions using Base
            matches = CLASS_REGEX.findall(content)
            if matches:
                new_content = content
                for match in matches:
                    # Insert __table_args__ line after class definition
                    new_content = new_content.replace(
                        match,
                        f"{match}\n    __table_args__ = {{'extend_existing': True}}"
                    )
                with open(path, "w") as f:
                    f.write(new_content)
                print(f"[PATCHED] {path}")

