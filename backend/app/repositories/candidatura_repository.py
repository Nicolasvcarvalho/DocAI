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
    
    @staticmethod
    def listar_disponiveis_para_analise(db):

        candidaturas = db.query(Candidatura).all()

        resultado = []

        for candidatura in candidaturas:
            
            print(
                f"id={candidatura.id}",
                f"status_banco={candidatura.status}",
                f"possui_analista={candidatura.possui_analista}",
                f"esta_disponivel={candidatura.esta_disponivel}"
                )

            if candidatura.esta_disponivel:
                
                resultado.append(candidatura)

        return resultado
