from fastapi import FastAPI

from app.api.routes.auth_routes import router as auth_router
from app.api.routes.documento_routes import router as doc_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(doc_router)