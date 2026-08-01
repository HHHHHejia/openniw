"""Apply SQL migrations in filename order. Run at startup and via CLI:

    python -m app.migrate
"""
import asyncio
import pathlib

import asyncpg

from .config import get_settings

MIGRATIONS_DIR = pathlib.Path(__file__).parent / "migrations"


async def migrate() -> list[str]:
    settings = get_settings()
    conn = await asyncpg.connect(settings.database_url, statement_cache_size=0)
    applied: list[str] = []
    try:
        await conn.execute("create schema if not exists openniw")
        await conn.execute(
            """create table if not exists openniw.schema_migrations (
                   name text primary key,
                   applied_at timestamptz not null default now()
               )"""
        )
        done = {
            r["name"]
            for r in await conn.fetch("select name from openniw.schema_migrations")
        }
        for path in sorted(MIGRATIONS_DIR.glob("*.sql")):
            if path.name in done:
                continue
            # Each migration file starts with `set search_path to openniw;`
            # and runs as a single multi-statement query, so the path applies
            # for the whole file regardless of pooler mode.
            await conn.execute(path.read_text())
            await conn.execute(
                "insert into openniw.schema_migrations(name) values($1)", path.name
            )
            applied.append(path.name)
    finally:
        await conn.close()
    return applied


if __name__ == "__main__":
    names = asyncio.run(migrate())
    print("applied:", names or "nothing (up to date)")
