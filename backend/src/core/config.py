from pydantic_settings import BaseSettings

class Setting(BaseSettings):
    
    GROQ_API_KEY:str
    CHROMA_PATH:str="./chroma_store"
    UPLOAD_DIR:str="./uploads"
    
    class config:
        env_file=".env"

settings = Setting()
    
    