from fastapi import HTTPException

class OCRValidator:

    CAMPOS_OBRIGATORIOS = []

    @classmethod
    def validar(cls, dados: dict):

        for campo in cls.CAMPOS_OBRIGATORIOS:

            if campo not in dados:
                raise HTTPException(status_code=400, detail=f"Campo obrigatório ausente: {campo}")
        
            valor = dados.get(campo)
            if isinstance(valor, str) and not valor.strip():
                raise HTTPException(status_code=400, detail=f"Campo obrigatório vazio: {campo}")