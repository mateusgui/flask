from sqlalchemy import select

from app.extensions import db
from app.models import Bairro

def listar():
    return db.session.scalars(select(Bairro).order_by(Bairro.nome)).all()

def buscar(bairro_id):
    return db.session.get(Bairro, bairro_id)

def criar(dados):
    bairro = Bairro(
        nome = dados["nome"],
        regiao = dados["regiao"]
    )
    db.session.add(bairro)
    db.session.commit()
    return bairro

def atualizar(bairro, dados):
    bairro.nome = dados.get("nome", bairro.nome)
    bairro.regiao = dados.get("regiao", bairro.regiao)
    db.session.commit()
    return bairro