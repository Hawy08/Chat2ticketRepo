import httpx
import base64
from app.core.config import settings

async def get_spotify_track(query: str):
    token = await get_spotify_token()
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.spotify.com/v1/search",
            headers=headers,
            params={
                "q": query,
                "type": "track",
                "limit": 1
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"DEBUG: Spotify Query: {query}")
            print(f"DEBUG: Spotify Response: {data}")
            tracks = data.get("tracks", {}).get("items", [])
            if tracks:
                track = tracks[0]
                if not track:
                    return None
                return {
                    "name": track.get("name"),
                    "artist": track.get("artists", [{}])[0].get("name"),
                    "url": track.get("external_urls", {}).get("spotify"),
                    "image": track.get("album", {}).get("images", [{}])[0].get("url") if track.get("album", {}).get("images") else None
                }
    return None

async def get_spotify_token():
    # Client Credentials Flow
    auth_str = f"{settings.SPOTIFY_CLIENT_ID}:{settings.SPOTIFY_CLIENT_SECRET}"
    b64_auth = base64.b64encode(auth_str.encode()).decode()
    
    headers = {
        "Authorization": f"Basic {b64_auth}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {"grant_type": "client_credentials"}
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://accounts.spotify.com/api/token",
            headers=headers,
            data=data
        )
        response.raise_for_status()
        return response.json()["access_token"]
