import ipaddress

from flask import Blueprint, abort, redirect, render_template, request, url_for

from app.models import TIPOS_EQUIPAMENTO
from app.services import bairros as bairros_service
from app.services import equipamentos as service

bp = Blueprint("equipamentos", __name__, url_prefix="/equipamentos")


def opcoes():
    # Listas usadas pelos selects do formulário
    return {"tipos": TIPOS_EQUIPAMENTO, "bairros": bairros_service.listar()}


def validar(valores):
    # Devolve a mensagem de erro, ou None se estiver tudo certo
    if not valores["nome"] or not valores["tipo"] or not valores["ip"]:
        return "Nome, tipo e IP são obrigatórios."

    try:
        ipaddress.ip_address(valores["ip"])
    except ValueError:
        # Sem isso o banco recusaria o INET e a página quebraria com erro 500
        return "IP inválido"

    return None


@bp.get("")
def listar():
    # Lista todos os equipamentos
    return render_template("equipamentos/lista.html", equipamentos=service.listar())


@bp.get("/novo")
def novo_form():
    # Mostra o formulário vazio de cadastro
    valores = {"nome": "", "tipo": TIPOS_EQUIPAMENTO[0], "ip": "", "bairro_id": None}
    return render_template(
        "equipamentos/form.html",
        titulo="Novo equipamento",
        acao=url_for("equipamentos.criar"),
        valores=valores,
        **opcoes(),
    )


@bp.post("/novo")
def criar():
    # Recebe o formulário de cadastro e salva
    bairro_id = request.form.get("bairro_id", "")
    valores = {
        "nome": request.form.get("nome", "").strip(),
        "tipo": request.form.get("tipo", ""),
        "ip": request.form.get("ip", "").strip(),
        "bairro_id": int(bairro_id) if bairro_id else None,
    }

    erro = validar(valores)
    if erro:
        # Devolve o mesmo formulário com o erro e o que já foi digitado
        return render_template(
            "equipamentos/form.html",
            titulo="Novo equipamento",
            acao=url_for("equipamentos.criar"),
            valores=valores,
            erro=erro,
            **opcoes(),
        )

    service.criar(valores)
    return redirect(url_for("equipamentos.listar"))


@bp.get("/<int:equipamento_id>/editar")
def editar_form(equipamento_id):
    # Mostra o formulário preenchido com os dados atuais do equipamento
    equipamento = service.buscar(equipamento_id)
    if equipamento is None:
        abort(404)

    valores = {
        "nome": equipamento.nome,
        "tipo": equipamento.tipo,
        "ip": str(equipamento.ip) if equipamento.ip else "",
        "bairro_id": equipamento.bairro_id,
    }
    return render_template(
        "equipamentos/form.html",
        titulo="Editar equipamento",
        acao=url_for("equipamentos.editar", equipamento_id=equipamento.id),
        valores=valores,
        **opcoes(),
    )


@bp.post("/<int:equipamento_id>/editar")
def editar(equipamento_id):
    # Recebe o formulário de edição e salva
    equipamento = service.buscar(equipamento_id)
    if equipamento is None:
        abort(404)

    bairro_id = request.form.get("bairro_id", "")
    valores = {
        "nome": request.form.get("nome", "").strip(),
        "tipo": request.form.get("tipo", equipamento.tipo),
        "ip": request.form.get("ip", "").strip(),
        "bairro_id": int(bairro_id) if bairro_id else None,
    }

    erro = validar(valores)
    if erro:
        return render_template(
            "equipamentos/form.html",
            titulo="Editar equipamento",
            acao=url_for("equipamentos.editar", equipamento_id=equipamento.id),
            valores=valores,
            erro=erro,
            **opcoes(),
        )

    service.atualizar(equipamento, valores)
    return redirect(url_for("equipamentos.listar"))


@bp.post("/<int:equipamento_id>/desativar")
def desativar(equipamento_id):
    # Marca o equipamento como inativo
    equipamento = service.buscar(equipamento_id)
    if equipamento is None:
        abort(404)

    service.desativar(equipamento)
    return redirect(url_for("equipamentos.listar"))
