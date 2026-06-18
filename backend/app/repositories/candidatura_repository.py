from app.models.candidatura import Candidatura
from datetime import datetime, UTC, timedelta

class CandidaturaRepository:

    @staticmethod
    def buscar_por_id(db, candidatura_id):
        
        return db.query(Candidatura).filter(Candidatura.id == candidatura_id).first()

    @staticmethod
    def salvar_candidatura(db, candidatura):

        db.add(candidatura)
        db.commit()
        db.refresh(candidatura)

        return candidatura
    
    @staticmethod
    def buscar_por_candidato(db, candidato_id):

        return db.query(Candidatura).filter(Candidatura.candidato_id == candidato_id).first()
    
    @staticmethod
    def listar_disponiveis_para_analise(db):

        candidaturas = db.query(Candidatura).all()

        resultado = []

        for candidatura in candidaturas:

            if candidatura.esta_disponivel:
                
                resultado.append(candidatura)

        return resultado
    
    @staticmethod
    def liberar_lock(candidatura):

        candidatura.locked_by_id = None
        candidatura.locked_at = None
        candidatura.lock_expires_at = None

        return candidatura

    @staticmethod
    def assumir(candidatura, secretaria_id):

        agora = datetime.utcnow()

        candidatura.locked_by_id = secretaria_id
        candidatura.locked_at = agora
        candidatura.lock_expires_at = agora + timedelta(minutes=30)

        return candidatura