import logging
from typing import Any

import linkedin_api

import models.job
import models.job_source
import utils.dicts
from . import SITE, SITE_SHORTNAME

LOGGER = logging.getLogger(__name__)


def run(client: linkedin_api.Linkedin, **search_kwargs):
    results = client.search_jobs(**search_kwargs)
    jobs = [_get_job(client, result) for result in results]
    return [job for job in jobs if job is not None]


def _get_job(
        client: linkedin_api.Linkedin,
        result: dict[str, Any]
) -> models.job.Job:
    job_urn = result["trackingUrn"]
    job = client.get_job(job_urn.split(':')[-1])
    if job is None:
        return None
    try:
        job_company_name = utils.dicts.find(job["companyDetails"], "name")
    except KeyError:
        job_company_name = ""
        LOGGER.warning(
            "No company name: %s: %s",
            SITE, job_urn
        )
    try:
        job_title = job["title"]
    except KeyError:
        job_title = ""
        LOGGER.warning(
            "No job title: %s: %s",
            SITE, job_urn
        )
    try:
        job_description = job["description"]["text"]
    except KeyError:
        job_description = ""
        LOGGER.warning(
            "No job description: %s: %s: %s: %s",
            SITE, job_urn, job_company_name, job_title
        )
    try:
        job_apply_url = utils.dicts.find(job["applyMethod"], "companyApplyUrl")
    except KeyError:
        job_apply_url = ""
        LOGGER.warning(
            "No company apply URL: %s: %s: %s: %s",
            SITE, job_urn, job_company_name, job_title
        )
    try:
        return models.job.Job(
            company_name=job_company_name,
            title=job_title,
            description=job_description,
            apply_url=job_apply_url,
            source=models.job_source.JobSource(
                shortname=SITE_SHORTNAME,
                site=SITE,
                url="",
                urn=job_urn
            )
        )
    except Exception:
        return None
