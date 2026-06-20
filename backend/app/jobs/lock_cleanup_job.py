from datetime import datetime

from app.core.database import SessionLocal

from app.models.candidatura import Candidatura

from app.services.documento.workflow.candidatura_workflow import CandidaturaWorkflowService

from app.repositories.candidatura_repository import CandidaturaRepository

def liberar_locks_expirados():

    db = SessionLocal()

    try:

        agora = datetime.utcnow()

        candidaturas = db.query(Candidatura).filter(Candidatura.lock_expires_at.is_not(None), Candidatura.lock_expires_at <= agora).all()

        for candidatura in candidaturas:

            CandidaturaRepository.liberar_lock(candidatura)

            candidatura.status = CandidaturaWorkflowService.recalcular_status_candidatura(candidatura)
        
        db.commit()

    finally:

        db.close()