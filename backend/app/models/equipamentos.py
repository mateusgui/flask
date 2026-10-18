from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, Boolean, CheckConstraint, ForeignKey, Identity, String, true
from sqlalchemy.dialects.postgresql import INET
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db

if TYPE_CHECKING:
    from app.models.bairros import Bairro
    from app.models.incidentes import Incidente

TIPOS_EQUIPAMENTO = ("olt", "roteador", "switch", "servidor")


class Equipamento(db.Model):
    __tablename__ = "equipamentos"
    __table_args__ = (
        CheckConstraint(f"tipo IN {TIPOS_EQUIPAMENTO}", name="ck_equipamentos_tipo"),
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    nome: Mapped[str] = mapped_column(String(100))
    tipo: Mapped[str] = mapped_column(String(20))
    # O psycopg devolve o INET como objeto do módulo ipaddress, use str(ip) ao serializar
    ip: Mapped[str | None] = mapped_column(INET)
    bairro_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("bairros.id"))
    ativo: Mapped[bool] = mapped_column(Boolean, server_default=true())

    bairro: Mapped[Bairro | None] = relationship(back_populates="equipamentos")
    incidentes: Mapped[list[Incidente]] = relationship(back_populates="equipamento")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nome": self.nome,
            "tipo": self.tipo,
            "ip": str(self.ip) if self.ip is not None else None,
            "bairro_id": self.bairro_id,
            "ativo": self.ativo,
        }

    def __repr__(self) -> str:
        return f"<Equipamento {self.id} {self.nome}>"