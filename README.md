# Registro de Incidentes (NOC)

Aplicação web para o NOC de um provedor de internet registrar incidentes de rede
(rompimento de fibra, queda de energia, falha de equipamento) e acompanhar a
resolução deles. Cada incidente guarda os bairros afetados, o equipamento
envolvido, a linha do tempo das atualizações e o tempo até a solução, o que
permite medir o MTTR (tempo médio de reparo) da operação.

## Stack

- Python 3.12 + Flask 3 (páginas renderizadas no servidor com Jinja)
- SQLAlchemy 2 + Flask-Migrate (Alembic)
- PostgreSQL 16
- Docker Compose (api + db + adminer)

## Como rodar

```
docker compose up -d
docker compose exec api flask db upgrade
```

Depois carregue os dados de exemplo (usuários, bairros, equipamentos e
incidentes) rodando o `seed.sql`:

```
docker compose exec -T db psql -U noc_user -d noc_incidentes < seed.sql
```

O `seed.sql` limpa as tabelas antes de inserir, então pode ser rodado de novo
sempre que você quiser voltar ao estado inicial.

A aplicação fica em `http://localhost:8000` (a home redireciona para a lista de
incidentes). O Adminer, para olhar o banco, fica em `http://localhost:8080`
(servidor `db`, credenciais do `.env`).

## Usuários do seed

Senha de todos: `senha123`

| E-mail | Perfil |
|---|---|
| carla.mendes@noc.local | supervisor |
| mateus.vilela@noc.local | operador |
| rafael.souza@noc.local | operador |

> A tela de login ainda não existe: os usuários são usados como autor do
> incidente e das atualizações.

## Estrutura de pastas

```
backend/
├── wsgi.py                 # entrypoint: cria o app
└── app/
    ├── __init__.py         # create_app: configura, registra blueprints e a rota "/"
    ├── config.py           # lê as variáveis de ambiente
    ├── extensions.py       # db e migrate
    ├── models/             # as tabelas
    ├── services/           # as regras e o acesso ao banco
    ├── routes/             # os blueprints (URLs)
    ├── templates/          # o HTML (Jinja)
    └── static/style.css    # o CSS
```

Cada camada tem um papel só:

- **models** — descrevem as tabelas e os relacionamentos. Nenhuma consulta vive aqui,
  só os campos, as constraints e propriedades derivadas (como o `mttr` do incidente).
- **services** — são as únicas que falam com o banco: montam o `select`, dão
  `db.session.add` e `commit`. Não conhecem HTTP (nada de `request` ou `redirect`).
- **routes** — ligam a URL à service: leem o `request.form`, convertem texto para
  `int`/`None`, validam, chamam a service e devolvem `render_template` ou `redirect`.
- **templates** — só exibem o que a rota passou, usando os objetos direto
  (`incidente.equipamento.nome`). Sem lógica de negócio.

## Comandos úteis

```
docker compose logs -f api        # ver os logs
docker compose down              # parar
docker compose down -v           # parar e apagar o banco
```
