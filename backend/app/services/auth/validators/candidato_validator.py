from fastapi import HTTPException

import re

from datetime import date

class CandidatoValidator:

    @classmethod
    def validar(cls, dados):

        dados.nome = cls.validar_nome(dados.nome)
        dados.sobrenome = cls.validar_sobrenome(dados.sobrenome)
        cls.validar_data_nascimento(dados.data_nascimento)
        cls.validar_senha(dados.senha)
        dados.email = dados.email.strip().lower()

    @staticmethod
    def validar_nome(nome: str):

        nome = nome.strip()

        if not nome:
            raise HTTPException(status_code=400, detail="Nome é obrigatório")
        
        if len(nome) < 2:
            raise HTTPException(status_code=400, detail="Nome deve possuir pelo menos 2 caracteres")
        
        if not re.fullmatch(r"[A-Za-zÀ-ÖØ-öø-ÿ ]+", nome):
            raise HTTPException(status_code=400, detail="Nome contém caracteres inválidos")
        
        return nome
    
    @staticmethod
    def validar_sobrenome(sobrenome: str):

        sobrenome = sobrenome.strip()

        if not sobrenome:
            raise HTTPException(status_code=400, detail="Sobrenome é obrigatório")

        if len(sobrenome) < 2:
            raise HTTPException(status_code=400, detail="Sobrenome deve possuir pelo menos 2 caracteres")

        if not re.fullmatch(r"[A-Za-zÀ-ÖØ-öø-ÿ ]+", sobrenome):
            raise HTTPException(status_code=400, detail="Sobrenome contém caracteres inválidos")

        return sobrenome
    
    @staticmethod
    def validar_data_nascimento(data_nascimento: date):

        if data_nascimento > date.today():
            raise HTTPException(status_code=400, detail="Data de nascimento não pode estar no futuro")

        idade = date.today().year - data_nascimento.year

        if idade < 17:
            raise HTTPException(status_code=400, detail="Idade mínima permitida é 17 anos")
        
    @staticmethod
    def validar_senha(senha: str):

        if len(senha) < 8:
            raise HTTPException(status_code=400, detail="Senha deve possuir pelo menos 8 caracteres")

        if not re.search(r"[A-Za-z]", senha):
            raise HTTPException(status_code=400, detail="Senha deve possuir ao menos uma letra")

        if not re.search(r"\d", senha):
            raise HTTPException(status_code=400, detail="Senha deve possuir ao menos um número")