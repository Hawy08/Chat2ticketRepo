import json
from collections import OrderedDict

def fix_openapi():
    try:
        with open("openapi.json", "r") as f:
            data = json.load(f)
        
        # Create a new ordered dict to enforce order
        new_data = OrderedDict()
        new_data["openapi"] = data.get("openapi", "3.1.0")
        new_data["info"] = data.get("info", {})
        new_data["servers"] = [
            {
                "url": "https://0b44d62428f0.ngrok-free.app",
                "description": "Development Server"
            }
        ]
        # Add remaining keys
        for key, value in data.items():
            if key not in ["openapi", "info", "servers"]:
                new_data[key] = value
        
        with open("openapi.json", "w") as f:
            json.dump(new_data, f, indent=2)
        print("Fixed openapi.json and moved servers to top")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fix_openapi()
