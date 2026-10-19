from flask import Blueprint, abort, redirect, render_template, request, url_for

from app.models import PERFIS
from app.services import usuarios as service

bp = Blueprint("usuarios", __name__, url_prefix="/usuarios")


@bp.get("")
def listar():
    # Lista todos os usuários
    return render_template("usuarios/lista.html", usuarios=service.listar())


@bp.get("/novo")
def novo_form():
    # Mostra o formulário vazio de cadastro
    valores = {"nome": "", "email": "", "perfil": "operador"}
    return render_template(
        "usuarios/form.html",
        titulo="Novo usuário",
        acao=url_for("usuarios.criar"),
        valores=valores,
        perfis=PERFIS,
        usuario=None,
    )


@bp.post("/novo")
def criar():
    # Recebe o formulário de cadastro e salva
    valores = {
        "nome": request.form.get("nome", "").strip(),
        "email": request.form.get("email", "").strip(),
        "perfil": request.form.get("perfil", "operador"),
    }
    senha = request.form.get("senha", "")

    if not valores["nome"] or not valores["email"] or not senha:
        # Devolve o mesmo formulário com o erro e o que já foi digitado
        return render_template(
            "usuarios/form.html",
            titulo="Novo usuário",
            acao=url_for("usuarios.criar"),
            valores=valores,
            perfis=PERFIS,
            usuario=None,
            erro="Nome, e-mail e senha são obrigatórios.",
        )

    service.criar({**valores, "senha": senha})
    return redirect(url_for("usuarios.listar"))


@bp.get("/<int:usuario_id>/editar")
def editar_form(usuario_id):
    # Mostra o formulário preenchido com os dados atuais do usuário
    usuario = service.buscar(usuario_id)
    if usuario is None:
        abort(404)

    valores = {"nome": usuario.nome, "email": usuario.email, "perfil": usuario.perfil}
    return render_template(
        "usuarios/form.html",
        titulo="Editar usuário",
        acao=url_for("usuarios.editar", usuario_id=usuario.id),
        valores=valores,
        perfis=PERFIS,
        usuario=usuario,
    )


@bp.post("/<int:usuario_id>/editar")
def editar(usuario_id):
    # Recebe o formulário de edição e salva
    usuario = service.buscar(usuario_id)
    if usuario is None:
        abort(404)

    valores = {
        "nome": request.form.get("nome", "").strip(),
        "email": request.form.get("email", "").strip(),
        "perfil": request.form.get("perfil", usuario.perfil),
    }

    if not valores["nome"] or not valores["email"]:
        return render_template(
            "usuarios/form.html",
            titulo="Editar usuário",
            acao=url_for("usuarios.editar", usuario_id=usuario.id),
            valores=valores,
            perfis=PERFIS,
            usuario=usuario,
            erro="Nome e e-mail são obrigatórios.",
        )

    dados = dict(valores)
    senha = request.form.get("senha", "")
    # Senha vazia significa "manter a atual", então a chave nem entra no dicionário
    if senha:
        dados["senha"] = senha

    service.atualizar(usuario, dados)
    return redirect(url_for("usuarios.listar"))


@bp.post("/<int:usuario_id>/desativar")
def desativar(usuario_id):
    # Marca o usuário como inativo
    usuario = service.buscar(usuario_id)
    if usuario is None:
        abort(404)

    service.desativar(usuario)
    return redirect(url_for("usuarios.listar"))
