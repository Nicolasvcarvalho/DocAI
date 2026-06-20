from fastapi import FastAPI

from fastapi_utils.tasks import repeat_every

from app.jobs.lock_cleanup_job import liberar_locks_expirados

from app.api.routes.autenticacao_router import router as autenticacao_router
from app.api.routes.documento_router import router as documento_router
from app.api.routes.candidato_dashboard_router import router as candidato_dashboard_router
from app.api.routes.ocr_router import router as ocr_router
from app.api.routes.secretaria_router import router as secretaria_dashboard_router

app = FastAPI()

@app.on_event("startup")
@repeat_every(seconds=30)
def executar_limpeza_locks():

    liberar_locks_expirados()

app.include_router(autenticacao_router)
app.include_router(documento_router)
app.include_router(candidato_dashboard_router)
app.include_router(ocr_router)
app.include_router(secretaria_dashboard_router)