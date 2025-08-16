import os

class Settings:
    PROJECT_NAME: str = "RAG Backend"
    ALLOWED_ORIGINS = ["http://localhost:3000"]  # frontend dev
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")

settings = Settings()
