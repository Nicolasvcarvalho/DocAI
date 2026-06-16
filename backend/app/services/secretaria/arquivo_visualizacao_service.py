from pathlib import Path

from fastapi import HTTPException
from fastapi.responses import Response


class ArquivoVisualizacaoService:

    @staticmethod
    def visualizar(arquivo):

        caminho = Path(arquivo.file_path)

        if not caminho.exists():
            raise HTTPException(status_code=404, detail="Arquivo físico não encontrado")

        with open(caminho, "rb") as f:
            conteudo = f.read()

        return Response(content=conteudo, media_type=arquivo.mime_type)