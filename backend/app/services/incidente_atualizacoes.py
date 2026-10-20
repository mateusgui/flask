from app.extensions import db
from app.models import IncidenteAtualizacao


def criar(incidente, dados):
    atualizacao = IncidenteAtualizacao(
        incidente_id=incidente.id,
        usuario_id=dados["usuario_id"],
        mensagem=dados["mensagem"],
        status_novo=dados.get("status_novo"),
    )
    db.session.add(atualizacao)

    # Mesmo commit: a nota do histórico e o novo status do incidente andam juntos
    if dados.get("status_novo"):
        incidente.status = dados["status_novo"]

    db.session.commit()
    return atualizacao
