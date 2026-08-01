"""Background job helpers: create a row, run a coroutine, record the result.

FastAPI BackgroundTasks is enough for v1 (single worker); the jobs table gives
the frontend something to poll and preserves results across reloads.
"""
import traceback
import uuid
from collections.abc import Awaitable, Callable

from .. import db


async def create(kind: str, case_id: uuid.UUID | None, payload: dict) -> str:
    job_id = await db.fetchval(
        "insert into jobs(kind, case_id, payload) values($1,$2,$3) returning id",
        kind, case_id, payload,
    )
    return str(job_id)


async def run(job_id: str, work: Callable[[], Awaitable[dict]]) -> None:
    """Execute `work` and persist status/result. Intended for BackgroundTasks."""
    await db.execute(
        "update jobs set status='running', updated_at=now() where id=$1",
        uuid.UUID(job_id),
    )
    try:
        result = await work()
        await db.execute(
            "update jobs set status='done', result=$2, updated_at=now() where id=$1",
            uuid.UUID(job_id), result or {},
        )
    except Exception as exc:
        await db.execute(
            "update jobs set status='error', error=$2, updated_at=now() where id=$1",
            uuid.UUID(job_id), f"{exc}\n{traceback.format_exc()[-2000:]}",
        )


async def get(job_id: str) -> dict | None:
    row = await db.fetchrow("select * from jobs where id=$1", uuid.UUID(job_id))
    return dict(row) if row else None
