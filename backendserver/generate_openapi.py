import json
import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

from app.main import app

def generate_openapi():
    openapi_schema = app.openapi()
    # Explicitly add the servers block
    openapi_schema["servers"] = [
        {
            "url": "https://0b44d62428f0.ngrok-free.app",
            "description": "Development Server"
        }
    ]
    with open("openapi.json", "w") as f:
        json.dump(openapi_schema, f, indent=2)
    print("openapi.json generated successfully with servers block.")

if __name__ == "__main__":
    generate_openapi()
