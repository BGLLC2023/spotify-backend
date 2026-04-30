from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    debug: bool = False
   
   
   

    class Config():
        env_file = ".env"




settings = Settings()