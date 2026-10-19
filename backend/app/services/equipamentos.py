from sqlalchemy import select

from app.extensions import db
from app.models import Equipamento


def listar():
    return db.session.scalars(select(Equipamento).order_by(Equipamento.nome)).all()
