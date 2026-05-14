from app.models.candidato import Candidato
from app.models.candidatura import Candidatura
from app.enums.status_candidatura import StatusCandidatura
from app.core.security import gerar_hash
from app.repositories.usuario_repository import UsuarioRepository
from app.repositories.candidatura_repository import CandidaturaRepository

class AuthService:

    @staticmethod
    def criar_candidato(db, dados):

        if UsuarioRepository.buscar_email(db, dados.email):
            raise Exception("Email já cadastrado")

        senha_hash = gerar_hash(dados.senha)

        candidato = Candidato(
            nome=dados.nome,
            sobrenome=dados.sobrenome,
            data_nascimento=dados.data_nascimento,
            sexo=dados.sexo,
            email=dados.email,
            senha_hash=senha_hash,
            
        )

        UsuarioRepository.salvar_candidato(db, candidato)

        candidatura = Candidatura(
            status=StatusCandidatura.PENDENTE_ENVIO,
            candidato_id=candidato.id
            )
        
        CandidaturaRepository.salvar_candidatura(db, candidatura)

        """
    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(Enum(StatusCandidatura), nullable=False)
    candidato_id = Column(ForeignKey("usuarios.id"), nullable=False)
    locked_by_id = Column(ForeignKey("usuarios.id"), nullable=True)
    locked_at = Column(DateTime, nullable=True)
    lock_expires_at = Column(DateTime, nullable=True)
        """