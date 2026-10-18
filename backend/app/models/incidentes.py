from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Identity,
    Integer,
    String,
    Table,
    Text,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db

if TYPE_CHECKING:
    from app.models.bairros import Bairro
    from app.models.equipamentos import Equipamento
    from app.models.incidente_atualizacoes import IncidenteAtualizacao
    from app.models.usuarios import Usuario

CATEGORIAS = (
    "rompimento_fibra",
    "queda_energia",
    "falha_equipamento",
    "manutencao_programada",
    "outro",
)
SEVERIDADES = ("baixa", "media", "alta", "critica")
STATUS = ("aberto", "em_andamento", "resolvido", "cancelado")


# Tabela de ligação N:N entre incidentes e bairros (não tem classe própria)
incidente_bairros = Table(
    "incidente_bairros",
    db.metadata,
    Column(
        "incidente_id",
        BigInteger,
        ForeignKey("incidentes.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column("bairro_id", BigInteger, ForeignKey("bairros.id"), primary_key=True),
)


class Incidente(db.Model):
    __tablename__ = "incidentes"
    __table_args__ = (
        CheckConstraint(f"categoria IN {CATEGORIAS}", name="ck_incidentes_categoria"),
        CheckConstraint(f"severidade IN {SEVERIDADES}", name="ck_incidentes_severidade"),
        CheckConstraint(f"status IN {STATUS}", name="ck_incidentes_status"),
        CheckConstraint("clientes_afetados >= 0", name="ck_incidentes_clientes_afetados"),
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    titulo: Mapped[str] = mapped_column(String(150))
    descricao: Mapped[str | None] = mapped_column(Text)
    categoria: Mapped[str] = mapped_column(String(30))
    severidade: Mapped[str] = mapped_column(String(10))
    status: Mapped[str] = mapped_column(String(15), server_default="aberto")
    clientes_afetados: Mapped[int] = mapped_column(Integer, server_default=text("0"))

    equipamento_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("equipamentos.id")
    )
    aberto_por_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("usuarios.id"))
    responsavel_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("usuarios.id")
    )

    aberto_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    resolvido_em: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    causa_raiz: Mapped[str | None] = mapped_column(Text)
    solucao: Mapped[str | None] = mapped_column(Text)

    # Duas FKs para usuarios: cada relationship precisa dizer qual coluna usa
    aberto_por: Mapped[Usuario] = relationship(
        back_populates="incidentes_abertos", foreign_keys=[aberto_por_id]
    )
    responsavel: Mapped[Usuario | None] = relationship(
        back_populates="incidentes_responsavel", foreign_keys=[responsavel_id]
    )
    equipamento: Mapped[Equipamento | None] = relationship(back_populates="incidentes")
    bairros: Mapped[list[Bairro]] = relationship(
        secondary=incidente_bairros, back_populates="incidentes"
    )
    atualizacoes: Mapped[list[IncidenteAtualizacao]] = relationship(
        back_populates="incidente",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="IncidenteAtualizacao.criado_em",
    )

    @property
    def mttr(self) -> timedelta | None:
        """Tempo até resolver. None enquanto o incidente não foi resolvido."""
        if self.resolvido_em is None or self.aberto_em is None:
            return None
        return self.resolvido_em - self.aberto_em

    def to_dict(self) -> dict:
        mttr = self.mttr
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descricao": self.descricao,
            "categoria": self.categoria,
            "severidade": self.severidade,
            "status": self.status,
            "clientes_afetados": self.clientes_afetados,
            "equipamento_id": self.equipamento_id,
            "aberto_por_id": self.aberto_por_id,
            "responsavel_id": self.responsavel_id,
            "bairros": [b.to_dict() for b in self.bairros],
            "aberto_em": self.aberto_em.isoformat() if self.aberto_em else None,
            "resolvido_em": self.resolvido_em.isoformat() if self.resolvido_em else None,
            "mttr_minutos": round(mttr.total_seconds() / 60) if mttr else None,
            "causa_raiz": self.causa_raiz,
            "solucao": self.solucao,
        }

    def __repr__(self) -> str:
        return f"<Incidente {self.id} [{self.status}] {self.titulo}>"