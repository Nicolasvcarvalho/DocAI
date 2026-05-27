from fastapi import HTTPException

from app.schemas.upload_documento_schema import DocumentoUploadInput

from app.models.tipo_documento import TipoDocumento

class LadoDocumentoValidator:

    @staticmethod
    def validar_lados_documento(tipo_documento: TipoDocumento, arquivos: DocumentoUploadInput):

        if tipo_documento.exige_frente_verso:

            if arquivos.frente is None or arquivos.verso is None:
                raise HTTPException(status_code=400, detail="Documento exige frente e verso")
            
        else:

            if arquivos.arquivo is None:
                raise HTTPException(status_code=400, detail="Documento exige arquivo único")