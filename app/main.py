from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from fastapi.testclient import TestClient

from app.api.api_v1.api import api_router
from app.core.config import settings
import os

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)
test_client = TestClient(app)

# Set all CORS enabled origins
# if settings.BACKEND_CORS_ORIGINS:
#     app.add_middleware(
#         CORSMiddleware,
#         allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
#         allow_credentials=True,
#         allow_methods=["*"],
#         allow_headers=["*"],
#     )

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

Assets_DIR = os.path.join(settings.home_dir, "assets")
if not os.path.exists(Assets_DIR):
    os.makedirs(Assets_DIR)

if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
