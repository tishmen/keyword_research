import traceback

from celery import shared_task
from celery.utils.log import get_task_logger

from data.models import Result
from data.scrapers import google_results

log = get_task_logger(__name__)


@shared_task(bind=True)
def scrape_google_results_task(self, keyword):
    try:
        results = google_results.scrape(keyword)
        log.info('Got {} results for {}'.format(len(results), keyword))
        for result in results:
            obj = Result(**result)
            obj.save()
    except Exception:
        log.error('Traceback: %s', traceback.format_exc())
        raise
