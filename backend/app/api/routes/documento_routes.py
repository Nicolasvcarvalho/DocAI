from fastapi import APIRouter, Depends, File, Form, UploadFile, HTTPException

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.dependencies.auth import get_usuario_logado

from app.repositories.tipo_documento_repository import TipoDocumentoRepository
from app.repositories.candidatura_repository import CandidaturaRepository

from app.schemas.upload_documento_schema import DocumentoUploadInput
from app.schemas.documento_schema import DocumentoResponse
from app.schemas.base import HTTPErrorResponse

from app.services.documento.documento_service import DocumentoService 

router = APIRouter(prefix="/documentos", tags=["Documentos"])

@router.post(
    "/documentos/upload",
    response_model=DocumentoResponse,
    summary="Upload documental",
    description="""
Realiza o upload de arquivos para um documento específico.

**Regras de Envio:**
- **Documento Identificação:** Enviar campos `frente` e `verso`.
- **Comprovantes/Outros:** Enviar apenas o campo `arquivo`.

**Sistema de Versão:**
Esta rota não deleta documentos antigos. Ela cria uma nova **Versão** e atualiza o ponteiro `versao_atual_id` no Documento.
""",
    responses={
        200: {"model": DocumentoResponse, "description": "Upload processado com sucesso."},
        401: {
            "model": HTTPErrorResponse,
            "description": "Usuário não autenticado.",
            "content": {"application/json": {"example": {"detail": "Not authenticated"}}}
        },
        404: {
            "model": HTTPErrorResponse,
            "description": "Recurso não encontrado.",
            "content": {
                "application/json": {
                    "examples": {
                        "Candidatura": {"value": {"detail": "Candidatura não encontrada"}},
                        "Tipo Documental": {"value": {"detail": "Tipo documental não encontrado"}}
                    }
                }
            }
        },
        400: {
            "model": HTTPErrorResponse,
            "description": "Erro na lógica de arquivos (ex: enviou 'arquivo' para RG).",
        }
    }
)
def upload_documentos(
    tipo_documento_id: int = Form(...),
    frente: UploadFile | None = File(None),
    verso: UploadFile | None = File(None),
    arquivo: UploadFile | None = File(None),
    db: Session = Depends(get_db),
    candidato = Depends(get_usuario_logado)
):
    candidatura = CandidaturaRepository.buscar_por_candidato(db, candidato_id=candidato.id)
    
    if not candidatura:
        raise HTTPException(status_code=404, detail="Candidatura não encontrada")
    
    tipo_documento = TipoDocumentoRepository.buscar_por_id(db, tipo_documento_id)

    if not tipo_documento:
        raise HTTPException(status_code=404, detail="Tipo documental não encontrado")
    
    upload_input = DocumentoUploadInput(frente=frente, verso=verso, arquivo=arquivo)

    return DocumentoService.upload_documento(
        db=db,
        candidatura_id=candidatura.id,
        tipo_documento=tipo_documento,
        arquivos=upload_input 
    )