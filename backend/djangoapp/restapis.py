"""HTTP client for the Express + MongoDB microservice and the sentiment analyzer."""
import logging
from urllib.parse import quote

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


class BackendError(Exception):
    def __init__(self, status, message):
        super().__init__(message)
        self.status = status
        self.message = message


def _handle(response):
    try:
        payload = response.json()
    except ValueError:
        payload = {'error': response.text[:200]}
    if response.status_code >= 400:
        message = payload.get('error') if isinstance(payload, dict) else str(payload)
        raise BackendError(response.status_code, message or 'Backend error')
    return payload


def get_request(endpoint, **params):
    url = f'{settings.BACKEND_URL}/{endpoint.lstrip("/")}'
    try:
        response = requests.get(url, params=params or None, timeout=settings.EXPRESS_TIMEOUT)
    except requests.RequestException as exc:
        logger.error('GET %s failed: %s', url, exc)
        raise BackendError(503, 'Dealer service is unavailable') from exc
    return _handle(response)


def post_review(data):
    url = f'{settings.BACKEND_URL}/insert_review'
    headers = {'X-API-Key': settings.EXPRESS_API_KEY} if settings.EXPRESS_API_KEY else {}
    try:
        response = requests.post(url, json=data, headers=headers, timeout=settings.EXPRESS_TIMEOUT)
    except requests.RequestException as exc:
        logger.error('POST %s failed: %s', url, exc)
        raise BackendError(503, 'Dealer service is unavailable') from exc
    return _handle(response)


def analyze_review_sentiments(text):
    url = f'{settings.SENTIMENT_ANALYZER_URL}/analyze/{quote(text, safe="")}'
    try:
        return _handle(requests.get(url, timeout=settings.EXPRESS_TIMEOUT))
    except (requests.RequestException, BackendError) as exc:
        logger.warning('Sentiment analysis failed: %s', exc)
        return {'sentiment': 'neutral'}
