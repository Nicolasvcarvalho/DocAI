from app.models.candidato import Usuario

class UsuarioRepository:

    @staticmethod
    def salvar_candidato(db, candidato):
        db.add(candidato)
        db.commit()
        db.refresh(candidato)

        return candidato
    
    @staticmethod
    def buscar_email(db, email: str):
        return db.query(Usuario).filter(Usuario.email==email).first()
    
    