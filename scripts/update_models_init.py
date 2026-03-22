import os

MODELS_DIR = "app/models"
INIT_FILE = os.path.join(MODELS_DIR, "__init__.py")

# Map files to actual class names when they don't match filename
SPECIAL_CLASSES = {
    "payment": "RentPayment",
    "tenant": "TenantProfile",
    "estate": "Estate",
    "property": "Property",
    "user": "User",
    "audit": "AuditLog",
    "utility": "UtilityBill", 
# Add more here as needed
}

lines = []
for file in os.listdir(MODELS_DIR):
    if file.endswith(".py") and file != "__init__.py":
        module = file.replace(".py", "")
        class_name = SPECIAL_CLASSES.get(module)
        if not class_name:
            # Default: capitalize words from filename
            class_name = "".join(word.capitalize() for word in module.split("_"))
        lines.append(f"from app.models.{module} import {class_name}")

with open(INIT_FILE, "w") as f:
    f.write("\n".join(sorted(lines)))

print("✅ app/models/__init__.py updated")
