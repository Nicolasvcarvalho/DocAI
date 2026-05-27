from pathlib import Path

from fastapi import HTTPException, UploadFile

from app.schemas.upload_documento_schema import DocumentoUploadInput

class UploadValidator:

    MAX_FILE_SIZE = 10 * 24 * 1024

    ALLOWED_EXTENSIONS = {
        ".png",
        ".jpeg"
    }

    ALLOWED_CONTENT_TYPES = {
        "image/png",
        "image/jpeg"
    }

    @staticmethod
    async def validar_upload(arquivos: DocumentoUploadInput):

        arquivos_recebidos = []

        opcoes_arquivos = [arquivos.frente, arquivos.verso, arquivos.arquivo]

        for arquivo in opcoes_arquivos:

            if arquivo is not None:
                arquivos_recebidos.append(arquivo)

        UploadValidator._validar_quantidade_arquivos(arquivos_recebidos)

        for arquivo in arquivos_recebidos:

            await UploadValidator._validar_arquivo(arquivo)

    @staticmethod
    def _validar_quantidade_arquivos(arquivos: list[UploadFile]):
        
        if len(arquivos) == 0:
            raise HTTPException(status_code=400, detail="Nenhum arquivo enviado")
        
        if len(arquivos) > 2:
            raise HTTPException(status_code=400, detail="Quantidade de arquivos inválidos")
        
    @staticmethod 
    async def _validar_arquivo(arquivo: UploadFile):

        UploadValidator._validar_extensao(arquivo)
        UploadValidator._validar_content_type(arquivo)

        await UploadValidator._validar_tamanho(arquivo)

    @staticmethod
    def _validar_extensao(arquivo: UploadFile):

        extensao = Path(arquivo.filename).suffix.lower()

        if extensao not in UploadValidator.ALLOWED_EXTENSIONS:
            raise HTTPException(status_code=400, detail=f"Extensão inválida: {extensao}")
        
    @staticmethod
    def _validar_content_type(arquivo: UploadFile):

        if arquivo.content_type not in UploadValidator.ALLOWED_CONTENT_TYPES:
            raise HTTPException(status_code=400, detail="Tipo de arquivo inválido")
        
    @staticmethod
    async def _validar_tamanho(arquivo: UploadFile):

        conteudo = await arquivo.read()

        tamanho = len(conteudo)

        if tamanho == 0:
            raise HTTPException(status_code=400, detail="Arquivo vazio")
        
        if tamanho > UploadValidator.MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="Arquivo excede o tamanho máximo")
        
        await arquivo.seek(0)    
    