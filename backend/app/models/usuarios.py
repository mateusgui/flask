from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    DateTime,
    Identity,
    String,
    func,
    true,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db

if TYPE_CHECKING:
    from app.models.incidentes import Incidente
    from app.models.incidente_atualizacoes import IncidenteAtualizacao

PERFIS = ("operador", "supervisor")


class Usuario(db.Model):
    __tablename__ = "usuarios"
    __table_args__ = (
        CheckConstraint(f"perfil IN {PERFIS}", name="ck_usuarios_perfil"),
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    nome: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(160), unique=True)
    senha_hash: Mapped[str] = mapped_column(String(255))
    perfil: Mapped[str] = mapped_column(String(20))
    ativo: Mapped[bool] = mapped_column(Boolean, server_default=true())
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    incidentes_abertos: Mapped[list[Incidente]] = relationship(
        back_populates="aberto_por", foreign_keys="Incidente.aberto_por_id"
    )
    incidentes_responsavel: Mapped[list[Incidente]] = relationship(
        back_populates="responsavel", foreign_keys="Incidente.responsavel_id"
    )
    atualizacoes: Mapped[list[IncidenteAtualizacao]] = relationship(
        back_populates="usuario"
    )

    def definir_senha(self, senha: str) -> None:
        self.senha_hash = generate_password_hash(senha)

    def senha_confere(self, senha: str) -> bool:
        return check_password_hash(self.senha_hash, senha)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "perfil": self.perfil,
            "ativo": self.ativo,
            "criado_em": self.criado_em.isoformat() if self.criado_em else None,
        }

    def __repr__(self) -> str:
        return f"<Usuario {self.id} {self.email}>"