from sqlalchemy import select

from app.extensions import db
from app.models import Equipamento


def listar():
    return db.session.scalars(select(Equipamento).order_by(Equipamento.nome)).all()


def buscar(equipamento_id):
    return db.session.get(Equipamento, equipamento_id)


def criar(dados):
    equipamento = Equipamento(
        nome=dados["nome"],
        tipo=dados["tipo"],
        ip=dados["ip"],
        bairro_id=dados.get("bairro_id"),
    )
    db.session.add(equipamento)
    db.session.commit()
    return equipamento


def atualizar(equipamento, dados):
    equipamento.nome = dados.get("nome", equipamento.nome)
    equipamento.tipo = dados.get("tipo", equipamento.tipo)
    equipamento.ip = dados.get("ip", equipamento.ip)
    equipamento.bairro_id = dados.get("bairro_id", equipamento.bairro_id)
    db.session.commit()
    return equipamento


def desativar(equipamento):
    equipamento.ativo = False
    db.session.commit()
