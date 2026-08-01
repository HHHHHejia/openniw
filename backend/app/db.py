"""asyncpg connection pool + tiny query helpers.

The backend is the only client of the database, so we skip an ORM and use
plain SQL. All OpenNIW tables live in the dedicated "openniw" schema so a
shared database (e.g. a reused Supabase project) is never polluted.

Supabase's pooler multiplexes server connections, so a session-level
`SET search_path` is unreliable; every query therefore runs inside a
transaction with `SET LOCAL search_path`, which is guaranteed to apply.
"""
import json
from typing import Any

import asyncpg

from .config import get_settings

_pool: asyncpg.Pool | None = None

SEARCH_PATH = "openniw, public"


async def _init_conn(conn: asyncpg.Connection) -> None:
    await conn.set_type_codec(
        "jsonb", encoder=json.dumps, decoder=json.loads, schema="pg_catalog"
    )
    await conn.set_type_codec(
        "json", encoder=json.dumps, decoder=json.loads, schema="pg_catalog"
    )


async def get_pool() -> asyncpg.Pool:
    global _pool
    if _pool is None:
        settings = get_settings()
        _pool = await asyncpg.create_pool(
            settings.database_url,
            min_size=1,
            max_size=5,
            init=_init_conn,
            # The pooler (pgbouncer/supavisor) breaks cross-query prepared
            # statements.
            statement_cache_size=0,
        )
    return _pool


async def close_pool() -> None:
    global _pool
    if _pool is not None:
        await _pool.close()
        _pool = None


async def _run(method: str, query: str, args: tuple) -> Any:
    pool = await get_pool()
    async with pool.acquire() as conn:
        async with conn.transaction():
            await conn.execute(f"set local search_path to {SEARCH_PATH}")
            return await getattr(conn, method)(query, *args)


async def fetch(query: str, *args: Any) -> list[asyncpg.Record]:
    return await _run("fetch", query, args)


async def fetchrow(query: str, *args: Any) -> asyncpg.Record | None:
    return await _run("fetchrow", query, args)


async def fetchval(query: str, *args: Any) -> Any:
    return await _run("fetchval", query, args)


async def execute(query: str, *args: Any) -> str:
    return await _run("execute", query, args)
