import logging
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Basic logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

# Create app
app = FastAPI()

# include_router imported lazily inside a function to avoid heavy import at module load
def include_routers():
    try:
        from backend_src.api.chat import router as chat_router
        app.include_router(chat_router)
    except Exception as e:
        logging.exception("Failed to include routers at startup (will retry later): %s", e)

include_routers()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# No uvicorn.run block here — Render will run uvicorn itself.
# But for local dev we keep a safe entry using env PORT.
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("backend_src.main:app", host="0.0.0.0", port=port)
