class CandidaturaRepository:

    @staticmethod
    def salvar_candidatura(db, candidatura):

        db.add(candidatura)
        db.commit()
        db.refresh(candidatura)

        return candidatura