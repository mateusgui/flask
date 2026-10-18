from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, Identity, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db

if TYPE_CHECKING:
    from app.models.equipamentos import Equipamento
    from app.models.incidentes import Incidente


class Bairro(db.Model):
    __tablename__ = "bairros"

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), unique=True)
    regiao: Mapped[str | None] = mapped_column(String(30))

    equipamentos: Mapped[list[Equipamento]] = relationship(back_populates="bairro")
    incidentes: Mapped[list[Incidente]] = relationship(
        secondary="incidente_bairros", back_populates="bairros"
    )

    def to_dict(self) -> dict:
        return {"id": self.id, "nome": self.nome, "regiao": self.regiao}

    def __repr__(self) -> str:
        return f"<Bairro {self.id} {self.nome}>"