from dotenv import load_dotenv
from pathlib import Path
dotenv_path = Path('config.env')
load_dotenv(dotenv_path=dotenv_path)

from logging.config import dictConfig
from config import LOGGING_CONFIG
dictConfig(LOGGING_CONFIG)
import uvicorn
from fastapi import FastAPI
from db.models import Base
from db.session import engine
from resources.v1 import threat

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(threat.router)

@app.get("/")
async def index():
    return {"message": "Hello World!"}

if __name__ == "__main__":
   uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
