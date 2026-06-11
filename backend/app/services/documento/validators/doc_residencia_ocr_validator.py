from fastapi import HTTPException

class ComprovanteResidenciaOCRValidator:

    CAMPOS_OBRIGATORIOS = ["logradouro", "numero", "bairro", "cidade", "estado", "cep"]

    @classmethod
    def validar(cls, dados: dict):

        for campo in cls.CAMPOS_OBRIGATORIOS:

            if campo not in dados:
                raise HTTPException(status_code=400, detail=f"Campo obrigatório ausente: {campo}")