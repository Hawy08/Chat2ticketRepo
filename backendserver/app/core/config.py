from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    STRIPE_SECRET_KEY: str
    STRIPE_WEBHOOK_SECRET: str = ""
    
    # IBM Cloud / Watsonx.ai
    IBM_CLOUD_API_KEY: str
    IBM_CLOUD_URL: str = "https://us-south.ml.cloud.ibm.com"
    IBM_CLOUD_PROJECT_ID: str

    # Spotify
    SPOTIFY_CLIENT_ID: str
    SPOTIFY_CLIENT_SECRET: str

    # Google
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str = "https://0b44d62428f0.ngrok-free.app/auth/google/callback" # Add if needed for signature verification

    # SMTP (Email)
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    SMTP_FROM_EMAIL: str

    class Config:
        env_file = ".env"

settings = Settings()
