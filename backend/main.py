from fastapi import FastAPI

from app.api.routes.autenticacao_router import router as autenticacao_router
from app.api.routes.documento_router import router as documento_router
from app.api.routes.candidato_dashboard_router import router as candidato_dashboard_router
from app.api.routes.ocr_router import router as ocr_router
from app.api.routes.secretaria_router import router as secretaria_dashboard_router

app = FastAPI()

app.include_router(autenticacao_router)
app.include_router(documento_router)
app.include_router(candidato_dashboard_router)
app.include_router(ocr_router)
app.include_router(secretaria_dashboard_router)