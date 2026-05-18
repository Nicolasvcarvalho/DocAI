from app.models.candidatura import Candidatura

class CandidaturaRepository:

    @staticmethod
    def salvar_candidatura(db, candidatura):

        db.add(candidatura)
        db.commit()
        db.refresh(candidatura)

        return candidatura
    
    @staticmethod
    def buscar_por_candidato(db, candidato_id):

        return db.query(Candidatura).filter(Candidatura.candidato_id == candidato_id).first()
    