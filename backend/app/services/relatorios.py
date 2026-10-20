from sqlalchemy import select

from app.extensions import db
from app.models import Incidente


def mttr():
    # Só os incidentes já resolvidos têm resolvido_em e, por consequência, MTTR
    incidentes = db.session.scalars(
        select(Incidente)
        .where(Incidente.status == "resolvido")
        .order_by(Incidente.aberto_em.desc())
    ).all()

    total = 0
    soma_minutos = 0.0
    soma_por_severidade = {}
    quantidade_por_severidade = {}

    for incidente in incidentes:
        if incidente.mttr is None:
            continue

        minutos = incidente.mttr.total_seconds() / 60
        total += 1
        soma_minutos += minutos

        severidade = incidente.severidade
        soma_por_severidade[severidade] = soma_por_severidade.get(severidade, 0.0) + minutos
        quantidade_por_severidade[severidade] = quantidade_por_severidade.get(severidade, 0) + 1

    media_geral = round(soma_minutos / total, 1) if total else 0.0
    media_por_severidade = {
        severidade: round(soma / quantidade_por_severidade[severidade], 1)
        for severidade, soma in soma_por_severidade.items()
    }

    return {
        "incidentes": incidentes,
        "total": total,
        "media_geral": media_geral,
        "media_por_severidade": media_por_severidade,
        "quantidade_por_severidade": quantidade_por_severidade,
    }
