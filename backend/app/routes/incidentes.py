from flask import Blueprint, abort, redirect, render_template, request, url_for

from app.models import CATEGORIAS, SEVERIDADES
from app.services import bairros as bairros_service
from app.services import equipamentos as equipamentos_service
from app.services import incidentes as service
from app.services import usuarios as usuarios_service

bp = Blueprint("incidentes", __name__, url_prefix="/incidentes")


def opcoes():
    # Listas usadas pelos selects e checkboxes do formulário
    return {
        "categorias": CATEGORIAS,
        "severidades": SEVERIDADES,
        "equipamentos": equipamentos_service.listar(),
        "usuarios": usuarios_service.listar(),
        "bairros": bairros_service.listar(),
    }


@bp.get("")
def listar():
    # Lista os incidentes, do mais recente para o mais antigo
    return render_template("incidentes/lista.html", incidentes=service.listar())


@bp.get("/<int:incidente_id>")
def detalhar(incidente_id):
    # Mostra todos os dados do incidente e a linha do tempo
    incidente = service.buscar(incidente_id)
    if incidente is None:
        abort(404)

    return render_template("incidentes/detalhe.html", incidente=incidente)


@bp.get("/novo")
def novo_form():
    # Mostra o formulário vazio de abertura de incidente
    valores = {
        "titulo": "",
        "descricao": "",
        "categoria": CATEGORIAS[0],
        "severidade": SEVERIDADES[0],
        "clientes_afetados": 0,
        "equipamento_id": None,
        "aberto_por_id": None,
        "bairros_ids": [],
    }
    return render_template(
        "incidentes/form.html",
        titulo="Novo incidente",
        acao=url_for("incidentes.criar"),
        valores=valores,
        incidente=None,
        **opcoes(),
    )


@bp.post("/novo")
def criar():
    # Recebe o formulário e abre o incidente
    # O formulário manda tudo como texto, então aqui converto para o que a service espera
    equipamento_id = request.form.get("equipamento_id", "")
    aberto_por_id = request.form.get("aberto_por_id", "")
    clientes_afetados = request.form.get("clientes_afetados", "")

    valores = {
        "titulo": request.form.get("titulo", "").strip(),
        "descricao": request.form.get("descricao", "").strip(),
        "categoria": request.form.get("categoria", ""),
        "severidade": request.form.get("severidade", ""),
        "clientes_afetados": int(clientes_afetados) if clientes_afetados else 0,
        "equipamento_id": int(equipamento_id) if equipamento_id else None,
        "aberto_por_id": int(aberto_por_id) if aberto_por_id else None,
        "bairros_ids": [int(x) for x in request.form.getlist("bairros_ids")],
    }

    if (
        not valores["titulo"]
        or not valores["categoria"]
        or not valores["severidade"]
        or valores["aberto_por_id"] is None
    ):
        # Devolve o mesmo formulário com o erro e o que já foi digitado
        return render_template(
            "incidentes/form.html",
            titulo="Novo incidente",
            acao=url_for("incidentes.criar"),
            valores=valores,
            incidente=None,
            erro="Título, categoria, severidade e aberto por são obrigatórios.",
            **opcoes(),
        )

    incidente = service.criar(valores)
    return redirect(url_for("incidentes.detalhar", incidente_id=incidente.id))


@bp.get("/<int:incidente_id>/editar")
def editar_form(incidente_id):
    # Mostra o formulário preenchido com os dados atuais do incidente
    incidente = service.buscar(incidente_id)
    if incidente is None:
        abort(404)

    valores = {
        "titulo": incidente.titulo,
        "descricao": incidente.descricao or "",
        "categoria": incidente.categoria,
        "severidade": incidente.severidade,
        "clientes_afetados": incidente.clientes_afetados,
        "equipamento_id": incidente.equipamento_id,
        "responsavel_id": incidente.responsavel_id,
    }
    return render_template(
        "incidentes/form.html",
        titulo="Editar incidente",
        acao=url_for("incidentes.editar", incidente_id=incidente.id),
        valores=valores,
        incidente=incidente,
        **opcoes(),
    )


@bp.post("/<int:incidente_id>/editar")
def editar(incidente_id):
    # Recebe o formulário de edição e salva
    incidente = service.buscar(incidente_id)
    if incidente is None:
        abort(404)

    equipamento_id = request.form.get("equipamento_id", "")
    responsavel_id = request.form.get("responsavel_id", "")
    clientes_afetados = request.form.get("clientes_afetados", "")

    valores = {
        "titulo": request.form.get("titulo", "").strip(),
        "descricao": request.form.get("descricao", "").strip(),
        "categoria": request.form.get("categoria", ""),
        "severidade": request.form.get("severidade", ""),
        "clientes_afetados": int(clientes_afetados) if clientes_afetados else 0,
        "equipamento_id": int(equipamento_id) if equipamento_id else None,
        "responsavel_id": int(responsavel_id) if responsavel_id else None,
    }

    if not valores["titulo"] or not valores["categoria"] or not valores["severidade"]:
        return render_template(
            "incidentes/form.html",
            titulo="Editar incidente",
            acao=url_for("incidentes.editar", incidente_id=incidente.id),
            valores=valores,
            incidente=incidente,
            erro="Título, categoria e severidade são obrigatórios.",
            **opcoes(),
        )

    service.atualizar(incidente, valores)
    return redirect(url_for("incidentes.detalhar", incidente_id=incidente.id))


@bp.post("/<int:incidente_id>/resolver")
def resolver(incidente_id):
    # Fecha o incidente com causa raiz e solução
    incidente = service.buscar(incidente_id)
    if incidente is None:
        abort(404)

    # Já fechado: não resolve de novo, só volta para o detalhe
    if incidente.status in ("resolvido", "cancelado"):
        return redirect(url_for("incidentes.detalhar", incidente_id=incidente.id))

    service.resolver(
        incidente,
        {
            "causa_raiz": request.form.get("causa_raiz", "").strip(),
            "solucao": request.form.get("solucao", "").strip(),
        },
    )
    return redirect(url_for("incidentes.detalhar", incidente_id=incidente.id))
