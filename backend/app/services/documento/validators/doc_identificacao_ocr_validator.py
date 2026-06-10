from fastapi import HTTPException

class DocumentoIdentificacaoOCRValidator:

    CAMPOS_OBRIGATORIOS = ["nome", "cpf", "data_nascimento", "nome_pai", "nome_mae"]

    @classmethod
    def validar(cls, dados: dict):
        
        for campo in cls.CAMPOS_OBRIGATORIOS:
            
            if campo not in dados:
                raise HTTPException(status_code=400, detail=f"Campo obrigatório ausente: {campo}")
            