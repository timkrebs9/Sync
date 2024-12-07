[![Build and deploy to Azure](https://github.com/timkrebs9/Sync/actions/workflows/main_sync-api.yml/badge.svg)](https://github.com/timkrebs9/Sync/actions/workflows/main_sync-api.yml)

### Project Struktur

snyc/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py         # Konfigurationseinstellungen
│   │   └── database.py       # Datenbankverbindung und Konfiguration
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── task_model.py     # SQLAlchemy Datenbankmodelle
│   │   └── user_model.py     # Benutzermodell (optional)
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── task_schema.py    # Pydantic Schemas für Validierung
│   │   └── user_schema.py    # Benutzer-Schemas (optional)
│   │
│   ├── crud/
│   │   ├── __init__.py
│   │   ├── task_crud.py      # CRUD-Operationen für Aufgaben
│   │   └── user_crud.py      # CRUD für Benutzer (optional)
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── endpoints/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── tasks.py
│   │   │   │   └── users.py
│   │   │   └── router.py     # V1 Router
│   │   │
│   │   └── v2/
│   │       ├── __init__.py
│   │       ├── endpoints/
│   │       │   ├── __init__.py
│   │       │   ├── tasks.py  # Neue Endpunkte oder erweiterte Version
│   │       │   └── users.py
│   │       └── router.py     # V2 Router
│   │
│   └── services/
│       ├── __init__.py
│       ├── task_service.py   # Businesslogik für Aufgaben
│       └── auth_service.py   # Authentifizierungsservice
│
├── tests/
│   ├── __init__.py
│   ├── test_tasks.py
│   └── test_users.py
│
├── migrations/
│   └── versions/              # Alembic Migrationsskripte
│
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── alembic.ini
├── README.md
└── .env