from __future__ import annotations

"""Simple DI wiring helpers for services and repos.

Routers can `Depends()` these callables to get instances. For the hackathon MVP,
we use in-memory repos so the app runs without a database.
"""

from fastapi import Depends

from app.config import get_settings
from app.repositories.claims_repo import ClaimsRepo
from app.repositories.files_repo import FilesRepo
from app.repositories.jobs_repo import JobsRepo
from app.repositories.providers_repo import ProvidersRepo
from app.repositories.users_repo import UsersRepo
from app.repositories.webhooks_repo import WebhooksRepo
from app.services.ai_drafting_service import AIDraftingService
from app.services.email_service import EmailService
from app.services.idempotency_service import IdempotencyService
from app.services.ocr_service import OCRService
from app.services.pdf_service import PDFService
from app.services.storage_service import StorageService
from app.services.submission_service import SubmissionService
from app.services.virus_scan_service import VirusScanService


def get_users_repo() -> UsersRepo:
    return UsersRepo()


def get_files_repo() -> FilesRepo:
    return FilesRepo()


def get_providers_repo() -> ProvidersRepo:
    return ProvidersRepo()


def get_claims_repo() -> ClaimsRepo:
    return ClaimsRepo()


def get_jobs_repo() -> JobsRepo:
    return JobsRepo()


def get_webhooks_repo() -> WebhooksRepo:
    return WebhooksRepo()


def get_storage_service(
    files: FilesRepo = Depends(get_files_repo),
    jobs: JobsRepo = Depends(get_jobs_repo),
):
    return StorageService(settings=get_settings(), files_repo=files, jobs_repo=jobs)


def get_virus_scan_service():
    return VirusScanService()


def get_ocr_service():
    return OCRService()


def get_pdf_service():
    return PDFService(settings=get_settings())


def get_email_service():
    return EmailService(settings=get_settings())


def get_ai_drafting_service(
    claims: ClaimsRepo = Depends(get_claims_repo),
    files: FilesRepo = Depends(get_files_repo),
    providers: ProvidersRepo = Depends(get_providers_repo),
    jobs: JobsRepo = Depends(get_jobs_repo),
):
    return AIDraftingService(
        settings=get_settings(),
        claims_repo=claims,
        files_repo=files,
        providers_repo=providers,
        jobs_repo=jobs,
    )


def get_submission_service():
    return SubmissionService()


def get_idempotency_service():
    return IdempotencyService()

