import httpx
from app.core.config import settings
import json

async def analyze_event_for_music(name: str, description: str):
    """
    Analyzes the event name and description using IBM Granite model to determine
    if it's music-related and extract genres/moods.
    """
    if not description:
        return {"is_music": False}

    prompt = f"""
    Analyze the following event and determine if it is related to music.
    If it is, extract the likely genres, moods, artists, and a good search query for a Spotify track (song) that matches the vibe.
    
    Event Name: {name}
    Event Description: {description}
    
    Output valid JSON only in the following format:
    {{
        "is_music": true/false,
        "genres": ["genre1", "genre2"],
        "moods": ["mood1", "mood2"],
        "search_query": "string to search on spotify"
    }}
    """

    url = f"{settings.IBM_CLOUD_URL}/ml/v1/text/generation?version=2023-05-29"
    
    headers = {
        "Authorization": f"Bearer {await get_ibm_token()}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
#music suggestion
    body = {
        "input": f"<|user|>\n{prompt}\n<|assistant|>\n",
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 200,
            "min_new_tokens": 0,
            "stop_sequences": [],
            "repetition_penalty": 1
        },
        #use IBM granite-3-8b-instruct model
        "model_id": "ibm/granite-3-8b-instruct",
        "project_id": settings.IBM_CLOUD_PROJECT_ID
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, json=body, timeout=30.0)
            response.raise_for_status()
            result = response.json()
            generated_text = result['results'][0]['generated_text']
            
            # Clean up potential markdown code blocks
            generated_text = generated_text.replace("```json", "").replace("```", "").strip()
            print(f"DEBUG: Generated text: {generated_text}")
            
            # Robust JSON extraction
            try:
                start_index = generated_text.find('{')
                end_index = generated_text.rfind('}')
                if start_index != -1 and end_index != -1:
                    json_str = generated_text[start_index : end_index + 1]
                    return json.loads(json_str)
                else:
                    raise ValueError("No JSON object found")
            except json.JSONDecodeError:
                 # Try to be lenient if it's a list or something else, though prompt asks for object
                 return json.loads(generated_text)
        except httpx.HTTPStatusError as e:
            print(f"AI Analysis failed: {e}")
            print(f"Response body: {e.response.text}")
            return {"is_music": False, "error": str(e)}
        except Exception as e:
            print(f"AI Analysis failed: {e}")
            return {"is_music": False, "error": str(e)}

async def get_ibm_token():
    # Exchange API Key for IAM Token
    # This is a simplified version. In production, cache the token.
    url = "https://iam.cloud.ibm.com/identity/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": settings.IBM_CLOUD_API_KEY
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, data=data)
        response.raise_for_status()
        return response.json()["access_token"]
