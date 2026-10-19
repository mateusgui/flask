from flask import Blueprint, jsonify, request

from app.services import bairros as service

bp = Blueprint("bairros", __name__, url_prefix="/api/bairros")

@bp.get("")
def listar():
    bairros = service.listar()
    return jsonify([b.to_dict() for b in bairros])

@bp.get("/<int:bairro_id>")
def detalhar(bairro_id):
    bairro = service.buscar(bairro_id)
    if bairro is None:
        return jsonify({"erro": "Bairro não encontrado"}), 404
    return jsonify(bairro.to_dict())

@bp.post("")
def criar():
    dados = request.get_json()
    if not dados or not dados.get("nome") or not dados.get("regiao"):
        return jsonify({"erro": "Nome e região são obrigatórios"}), 400
    bairro = service.criar(dados)
    return jsonify(bairro.to_dict()), 201

@bp.put("/<int:bairro_id>")
def atualizar(bairro_id):
    dados = request.get_json()
    bairro = service.buscar(bairro_id)
    if bairro is None:
        return jsonify({"erro": "Bairro não encontrado"}), 404
    bairro = service.atualizar(bairro, dados)
    return jsonify(bairro.to_dict())