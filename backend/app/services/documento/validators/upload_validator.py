from pathlib import Path

from fastapi import HTTPException, UploadFile

from app.schemas.upload_documento_schema import DocumentoUploadInput

class UploadValidator:

    MB = 1024 * 1024
    MAX_FILE_SIZE = 10 * MB

    ALLOWED_EXTENSIONS = {
        ".jpg",
        ".png",
        ".jpeg"
    }

    ALLOWED_CONTENT_TYPES = {
        "image/png",
        "image/jpeg"
    }

    MAGIC_NUMBERS = {
    ".png": [b"\x89PNG\r\n\x1a\n"],
    ".jpg": [b"\xff\xd8\xff"],
    ".jpeg": [b"\xff\xd8\xff"]
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
            raise HTTPException(status_code=400, detail="Quantidade de arquivos inválida")
        
    @staticmethod 
    async def _validar_arquivo(arquivo: UploadFile):

        UploadValidator._validar_extensao(arquivo)
        
        UploadValidator._validar_content_type(arquivo)

        await UploadValidator._validar_tamanho(arquivo)

        await UploadValidator._validar_magic_number(arquivo)

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

    @staticmethod
    async def _validar_magic_number(arquivo: UploadFile):

        extensao = Path(arquivo.filename).suffix.lower()

        assinaturas_esperadas = UploadValidator.MAGIC_NUMBERS.get(extensao)

        if not assinaturas_esperadas:
            return
        
        cabecalho = await arquivo.read(16)

        if not any(cabecalho.startswith(assinatura) for assinatura in assinaturas_esperadas):
            raise HTTPException(status_code=400, detail="Assinatura do arquivo inválida")
        
        await arquivo.seek(0)