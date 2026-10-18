from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Identity,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db
from app.models.incidentes import STATUS

if TYPE_CHECKING:
    from app.models.incidentes import Incidente
    from app.models.usuarios import Usuario


class IncidenteAtualizacao(db.Model):
    __tablename__ = "incidente_atualizacoes"
    __table_args__ = (
        CheckConstraint(
            f"status_novo IS NULL OR status_novo IN {STATUS}",
            name="ck_incidente_atualizacoes_status_novo",
        ),
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    incidente_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("incidentes.id", ondelete="CASCADE")
    )
    usuario_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("usuarios.id"))
    mensagem: Mapped[str] = mapped_column(Text)
    status_novo: Mapped[str | None] = mapped_column(String(15))
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    incidente: Mapped[Incidente] = relationship(back_populates="atualizacoes")
    usuario: Mapped[Usuario] = relationship(back_populates="atualizacoes")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "incidente_id": self.incidente_id,
            "usuario_id": self.usuario_id,
            "mensagem": self.mensagem,
            "status_novo": self.status_novo,
            "criado_em": self.criado_em.isoformat() if self.criado_em else None,
        }

    def __repr__(self) -> str:
        return f"<IncidenteAtualizacao {self.id} incidente={self.incidente_id}>"