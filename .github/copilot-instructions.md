## Quick context for AI coding agents

This repository contains student lab exercises (CMPT 221L) implemented as small Flask webapps that demonstrate SQL/ORM patterns with PostgreSQL. Focus your edits on the `labs/` subfolders (each lab is standalone). Typical languages/frameworks: Python 3.x, Flask, SQLAlchemy, and raw SQL via SQLAlchemy `text()`.

Key paths to inspect when making changes:
- `README.md` — course & workflow info (forking, branching, submitting PRs).
- `labs/lab-3/` — simple Flask app using `db.server` (Flask-SQLAlchemy). See `app.py` and `db/server.py` for app initialization patterns.
- `labs/lab-4/` — shows both raw SQL (`db/sql.py`) and SQLAlchemy ORM (`db/orm.py`) approaches. `app.py` demonstrates how routes call these utilities.
- `labs/lab-6/` — basic user signup/login skeleton. `app.py`, `db/server.py`, `db/query.py`, and `db/schema/` contain relevant patterns.

Project-specific conventions and patterns
- Each lab defines a `create_app()` or top-level `app` in `app.py`; prefer editing the lab folder you were asked to change.
- DB initialization:
  - Lab 3 uses Flask-SQLAlchemy and places `app` in `db/server.py`; importing `db.schema.*` happens after db is created.
  - Labs 4 and 6 use SQLAlchemy core/ORM with `Base = declarative_base()` and `init_database()` in `db/server.py`. Use `get_session()` to obtain a session and always close it in finally blocks (see `db/sql.py`).
- Naming: tables/classes use PascalCase in Python files (e.g. `Users`, `Course`, `ProfessorCourse`) and the Postgres table names include quoted mixed-case (e.g. "Courses"). When writing raw SQL match the quoted names.
- Environment: DB credentials are loaded from a `.env` file via `python-dotenv` and expect these keys: `db_name`, `db_owner`, `db_pass`. Use `postgresql://{owner}:{pass}@localhost/{db}` URIs.

Typical developer workflows and commands
- Install dependencies: repository lists `requirements.txt` at the root. Prefer creating a venv and installing there:
  - python -m venv venv
  - source venv/bin/activate
  - pip install -r requirements.txt
- Running apps locally: for lab folders that define `create_app()` run the file directly (e.g. `python labs/lab-4/app.py`) or use Flask tooling after setting FLASK_APP if preferred. The apps call `init_database()` on startup which creates tables.
- DB: PostgreSQL must be available locally and the database named in `.env` must exist and be reachable. The code will print a connection success/failure message when starting.

Patterns to follow when changing code
- Prefer small, local edits inside a lab folder rather than cross-cutting changes across labs.
- When adding DB operations:
  - For raw SQL use `db.server.get_session()` / `PostgresSession()` and ensure commit/rollback and session.close() in finally blocks (see `labs/lab-4/db/sql.py`).
  - For ORM use declarative `Base` models in `db/schema/` and `sessionmaker` from `db/server.py`.
- Templates live under `templates/` per lab. When changing route behavior show minimal HTML changes; instructor grading expects template names unchanged unless assignment asks differently.

Examples from this codebase
- Raw SQL read: `labs/lab-4/db/sql.py:get_all_courses()` uses `text()` and `session.execute(...).fetchall()` and then closes the session in finally.
- ORM init: `labs/lab-4/db/server.py:init_database()` imports `db.schema` models and calls `Base.metadata.create_all(bind=engine)`.
- Flask app pattern: `labs/lab-6/app.py:create_app()` sets `SQLALCHEMY_DATABASE_URI` from `.env` values, calls `init_database()` inside `app.app_context()`, then registers routes.

What NOT to do
- Don’t assume a containerized DB or CI. Tests/builds are not present; do not add heavyweight infra changes.
- Don’t change global project-level settings (root `README.md`, top-level structure) unless the user asks. Keep edits scoped to the relevant lab unless requested.

If you make changes
- Run the modified lab locally (activate venv, ensure Postgres running, then `python labs/<lab-x>/app.py`) and verify the app starts and prints DB connection messages.
- Keep commits small and include the lab number in the commit message, e.g. `lab-6: implement signup insert`.

Questions for the user
- Should edits apply to a specific lab (which one)?
- Do you want test scaffolding or CI added, or keep changes minimal to the lab code?

If anything above is unclear, ask for the target lab and I will adjust the guidance or update examples.
