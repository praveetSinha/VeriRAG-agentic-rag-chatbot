import logging
from fastapi import FastAPI
from backend.backend_src.api.chat import router as chat_router
from backend.backend_src.config.backend_settings import Settings
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

app = FastAPI()
app.include_router(chat_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

settings = Settings()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend_src.main:app",
        host="0.0.0.0",
        port=8000,
    )
