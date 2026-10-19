from sqlalchemy import select

from app.extensions import db
from app.models import Usuario


def listar():
    return db.session.scalars(select(Usuario).order_by(Usuario.nome)).all()


def buscar(usuario_id):
    return db.session.get(Usuario, usuario_id)


def criar(dados):
    usuario = Usuario(
        nome=dados["nome"],
        email=dados["email"],
        perfil=dados.get("perfil", "operador"),
    )
    usuario.definir_senha(dados["senha"])
    db.session.add(usuario)
    db.session.commit()
    return usuario


def atualizar(usuario, dados):
    usuario.nome = dados.get("nome", usuario.nome)
    usuario.email = dados.get("email", usuario.email)
    usuario.perfil = dados.get("perfil", usuario.perfil)
    if "senha" in dados:
        usuario.definir_senha(dados["senha"])
    db.session.commit()
    return usuario


def desativar(usuario):
    usuario.ativo = False
    db.session.commit()