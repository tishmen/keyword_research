import traceback

from celery import shared_task
from celery.utils.log import get_task_logger

from data.scrapers import google_results, contents
from data.helpers import contents_helpers

log = get_task_logger(__name__)


@shared_task(bind=True)
def scrape_google_results_task(self, keyword):
    try:
        google_results.scrape(keyword)
    except Exception:
        log.error('Traceback: %s', traceback.format_exc())
        raise


@shared_task(bind=True)
def scrape_google_result_count_task(self, keyword):
    try:
        google_results.scrape_count(keyword)
    except Exception:
        log.error('Traceback: %s', traceback.format_exc())
        raise


@shared_task(bind=True)
def scrape_contents_task(self, result):
    try:
        contents.scrape(result)
    except Exception:
        log.error('Traceback: %s', traceback.format_exc())
        raise


@shared_task(bind=True)
def process_contents_task(self, content):
    try:
        contents_helpers.process(content)
    except Exception:
        log.error('Traceback: %s', traceback.format_exc())
        raise


@shared_task(bind=True)
def create_summary_task(self, content):
    try:
        contents_helpers.summarize(content)
    except Exception:
        log.error('Traceback: %s', traceback.format_exc())
        raise
