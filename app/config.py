from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"

class Setting:
    DATABASE_URL: str = DATABASE_URL
    # DATABASE_URL: str = os.getenv(DATABASE_URL)
    
settings = Setting()    