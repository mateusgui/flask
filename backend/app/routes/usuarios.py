from flask import Blueprint, jsonify, request

from app.services import usuarios as service

bp = Blueprint("usuarios", __name__, url_prefix="/api/usuarios")


@bp.get("")
def listar():
    usuarios = service.listar()
    return jsonify([u.to_dict() for u in usuarios])


@bp.get("/<int:usuario_id>")
def detalhar(usuario_id):
    usuario = service.buscar(usuario_id)
    if usuario is None:
        return jsonify({"erro": "Usuário não encontrado"}), 404
    return jsonify(usuario.to_dict())


@bp.post("")
def criar():
    dados = request.get_json()
    if not dados or not dados.get("nome") or not dados.get("email") or not dados.get("senha"):
        return jsonify({"erro": "nome, email e senha são obrigatórios"}), 400
    usuario = service.criar(dados)
    return jsonify(usuario.to_dict()), 201


@bp.put("/<int:usuario_id>")
def atualizar(usuario_id):
    usuario = service.buscar(usuario_id)
    if usuario is None:
        return jsonify({"erro": "Usuário não encontrado"}), 404
    usuario = service.atualizar(usuario, request.get_json())
    return jsonify(usuario.to_dict())


@bp.delete("/<int:usuario_id>")
def desativar(usuario_id):
    usuario = service.buscar(usuario_id)
    if usuario is None:
        return jsonify({"erro": "Usuário não encontrado"}), 404
    service.desativar(usuario)
    return "", 204