from pathlib import Path
import shutil

class FileStorageService:
    
    STORAGE_ROOT = Path("storage")

    @staticmethod
    def salvar_arquivo(arquivo, caminho):

        caminho.parent.mkdir(parents=True, exist_ok=True)

        with open(caminho, "wb") as buffer:

            shutil.copyfileobj(arquivo.file, buffer)