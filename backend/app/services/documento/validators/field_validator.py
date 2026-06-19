import re

from datetime import date
from datetime import datetime

from fastapi import HTTPException


class FieldValidator:

    UF_VALIDAS = {
        "AC","AL","AP","AM","BA",
        "CE","DF","ES","GO","MA",
        "MT","MS","MG","PA","PB",
        "PR","PE","PI","RJ","RN",
        "RS","RO","RR","SC","SP",
        "SE","TO"
    }

    @staticmethod
    def limpar_numeros(valor: str):

        return re.sub(r"\D", "", valor)
    
    @classmethod
    def validar_cpf(cls, cpf: str):

        cpf = cls.limpar_numeros(cpf)

        if not cpf.isdigit():
            raise HTTPException(status_code=400, detail="CPF deve conter apenas números")

        if len(cpf) != 11:
            raise HTTPException(status_code=400, detail="CPF deve possuir 11 dígitos")

        cls._validar_digitos_cpf(cpf)

        return cpf
    
    @staticmethod
    def _validar_digitos_cpf(cpf: str):

        if cpf == cpf[0] * 11:
            raise HTTPException(status_code=400, detail="CPF inválido")

        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))

        resto = (soma * 10) % 11

        primeiro = 0 if resto == 10 else resto

        if primeiro != int(cpf[9]):
            raise HTTPException(status_code=400, detail="CPF inválido")

        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))

        resto = (soma * 10) % 11

        segundo = 0 if resto == 10 else resto

        if segundo != int(cpf[10]):
            raise HTTPException(status_code=400, detail="CPF inválido")
        
    @classmethod
    def validar_rg(cls, rg: str):

        rg = rg.strip()

        if not (5 <= len(rg) <= 14):
            raise HTTPException(status_code=400, detail="RG deve possuir entre 5 e 14 caracteres")

        return rg
    
    @staticmethod
    def validar_data_nascimento(data_str: str):

        try:
            data = datetime.strptime(data_str, "%Y-%m-%d").date()

        except ValueError:
            raise HTTPException(status_code=400, detail="Formato de data inválido")

        if data > date.today():
            raise HTTPException(status_code=400, detail="Data de nascimento não pode estar no futuro")

        return data.isoformat()
    
    @classmethod
    def validar_cep(cls, cep: str):

        cep = cls.limpar_numeros(cep)

        if len(cep) != 8:
            raise HTTPException(status_code=400, detail="CEP deve possuir 8 dígitos")

        return cep
    
    @classmethod
    def validar_uf(cls, uf: str):

        uf = uf.strip().upper()

        if uf not in cls.UF_VALIDAS:
            raise HTTPException(status_code=400, detail="UF inválida")

        return uf
    
