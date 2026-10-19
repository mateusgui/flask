from sqlalchemy import select

from app.extensions import db
from app.models import Incidente, Bairro
from datetime import datetime, timezone

def listar():
    return db.session.scalars(select(Incidente).order_by(Incidente.aberto_em.desc())).all()

def buscar(incidente_id):
    return db.session.get(Incidente, incidente_id)

def criar(dados):
    incidente = Incidente(
        titulo = dados["titulo"],
        descricao = dados.get("descricao"),
        categoria = dados["categoria"],
        severidade = dados["severidade"],
        clientes_afetados = dados.get("clientes_afetados", 0),
        equipamento_id = dados.get("equipamento_id"),
        aberto_por_id = dados["aberto_por_id"]
    )
    ids = dados.get("bairros_ids", [])
    incidente.bairros = db.session.scalars(select(Bairro).where(Bairro.id.in_(ids))).all()

    db.session.add(incidente)
    db.session.commit()
    return incidente

def atualizar(incidente, dados):
    incidente.titulo = dados.get("titulo", incidente.titulo)
    incidente.descricao = dados.get("descricao", incidente.descricao)
    incidente.categoria = dados.get("categoria", incidente.categoria)
    incidente.severidade = dados.get("severidade", incidente.severidade)
    incidente.clientes_afetados = dados.get("clientes_afetados", incidente.clientes_afetados)
    incidente.equipamento_id = dados.get("equipamento_id", incidente.equipamento_id)
    incidente.responsavel_id = dados.get("responsavel_id", incidente.responsavel_id)
    db.session.commit()
    return incidente

def resolver(incidente, dados):
    incidente.status = "resolvido"
    incidente.resolvido_em = datetime.now(timezone.utc)
    incidente.causa_raiz = dados.get("causa_raiz")
    incidente.solucao = dados.get("solucao")
    db.session.commit()
    return incidente