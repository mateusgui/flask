from flask import Blueprint, abort, redirect, render_template, request, url_for

from app.services import bairros as service

bp = Blueprint("bairros", __name__, url_prefix="/bairros")


@bp.get("")
def listar():
    # Lista todos os bairros
    return render_template("bairros/lista.html", bairros=service.listar())


@bp.get("/novo")
def novo_form():
    # Mostra o formulário vazio de cadastro
    return render_template(
        "bairros/form.html",
        titulo="Novo bairro",
        acao=url_for("bairros.criar"),
        valores={"nome": "", "regiao": ""},
    )


@bp.post("/novo")
def criar():
    # Recebe o formulário de cadastro e salva
    valores = {
        "nome": request.form.get("nome", "").strip(),
        "regiao": request.form.get("regiao", "").strip(),
    }

    if not valores["nome"] or not valores["regiao"]:
        # Devolve o mesmo formulário com o erro e o que já foi digitado
        return render_template(
            "bairros/form.html",
            titulo="Novo bairro",
            acao=url_for("bairros.criar"),
            valores=valores,
            erro="Nome e região são obrigatórios.",
        )

    service.criar(valores)
    return redirect(url_for("bairros.listar"))


@bp.get("/<int:bairro_id>/editar")
def editar_form(bairro_id):
    # Mostra o formulário preenchido com os dados atuais do bairro
    bairro = service.buscar(bairro_id)
    if bairro is None:
        abort(404)

    return render_template(
        "bairros/form.html",
        titulo="Editar bairro",
        acao=url_for("bairros.editar", bairro_id=bairro.id),
        valores={"nome": bairro.nome, "regiao": bairro.regiao or ""},
    )


@bp.post("/<int:bairro_id>/editar")
def editar(bairro_id):
    # Recebe o formulário de edição e salva
    bairro = service.buscar(bairro_id)
    if bairro is None:
        abort(404)

    valores = {
        "nome": request.form.get("nome", "").strip(),
        "regiao": request.form.get("regiao", "").strip(),
    }

    if not valores["nome"] or not valores["regiao"]:
        return render_template(
            "bairros/form.html",
            titulo="Editar bairro",
            acao=url_for("bairros.editar", bairro_id=bairro.id),
            valores=valores,
            erro="Nome e região são obrigatórios.",
        )

    service.atualizar(bairro, valores)
    return redirect(url_for("bairros.listar"))
