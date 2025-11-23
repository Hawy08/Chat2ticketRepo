import asyncio
import sys
import os

# Add the current directory to sys.path so we can import app modules
sys.path.append(os.getcwd())

from app.services.ai_generator import analyze_event_for_music

async def main():
    print("Testing AI Generator...")
    
    # Test Case 1: Music Event
    print("\n--- Test Case 1: Music Event ---")
    name = "Summer Jazz Festival"
    description = "A relaxing evening of smooth jazz featuring top artists from around the world. Come enjoy the saxophone melodies."
    print(f"Input: {name} - {description}")
    try:
        result = await analyze_event_for_music(name, description)
        print("Result:", result)
    except Exception as e:
        print(f"Error: {e}")

    # Test Case 2: Non-Music Event
    print("\n--- Test Case 2: Non-Music Event ---")
    name = "Python Coding Workshop"
    description = "Learn how to build APIs with FastAPI and Python. Bring your laptop!"
    print(f"Input: {name} - {description}")
    try:
        result = await analyze_event_for_music(name, description)
        print("Result:", result)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
