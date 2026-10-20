from flask import Blueprint, render_template

from app.services import relatorios as service

bp = Blueprint("relatorios", __name__, url_prefix="/relatorios")


@bp.get("/mttr")
def mttr():
    # Mostra o tempo médio de reparo dos incidentes resolvidos
    return render_template("relatorios/mttr.html", relatorio=service.mttr())
