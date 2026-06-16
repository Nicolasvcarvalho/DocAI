from fastapi import HTTPException

class ArquivoVisualizacaoValidator:

    @staticmethod
    def validar(arquivo):

        if not arquivo.versao_documento:
            raise HTTPException(status_code=400, detail="Arquivo sem versão documental")
            
        documento = arquivo.versao_documento.documento

        if not documento:
            raise HTTPException(status_code=400, detail="Versão sem documento")            

        candidatura = documento.candidatura

        if not candidatura:
            raise HTTPException(status_code=400, detail=("Documento sem candidatura"))

        return candidatura