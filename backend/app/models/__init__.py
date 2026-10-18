# Importar todos os models aqui garante que o SQLAlchemy e o Flask-Migrate
# enxerguem todas as tabelas, inclusive a incidente_bairros.
from app.models.bairros import Bairro
from app.models.equipamentos import TIPOS_EQUIPAMENTO, Equipamento
from app.models.incidentes import (
    CATEGORIAS,
    SEVERIDADES,
    STATUS,
    Incidente,
    incidente_bairros,
)
from app.models.incidente_atualizacoes import IncidenteAtualizacao
from app.models.usuarios import PERFIS, Usuario

__all__ = [
    "Bairro",
    "Equipamento",
    "Incidente",
    "IncidenteAtualizacao",
    "Usuario",
    "incidente_bairros",
    "CATEGORIAS",
    "SEVERIDADES",
    "STATUS",
    "PERFIS",
    "TIPOS_EQUIPAMENTO",
]