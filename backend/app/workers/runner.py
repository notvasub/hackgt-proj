from __future__ import annotations

import asyncio

from app.repositories.jobs_repo import JobsRepo
from app.services.ai_drafting_service import AIDraftingService


async def run_once(jobs: JobsRepo, ai: AIDraftingService):
    job = await jobs.claim_next(queue_type="draft_generation")
    if not job:
        return False
    try:
        await jobs.start(job.id)
        # In this MVP, assume job.result includes claim_id; but our enqueue immediately processes.
        await jobs.succeed(job.id, result={"ok": True})
    except Exception as e:  # noqa: BLE001
        await jobs.fail(job.id, str(e))
    return True


async def main():
    jobs = JobsRepo()
    ai = AIDraftingService.__new__(AIDraftingService)  # Not actually used in MVP loop
    while True:
        did = await run_once(jobs, ai)  # noqa: F841
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())

