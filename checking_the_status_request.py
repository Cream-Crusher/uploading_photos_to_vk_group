import requests


def get_request_status(response):
    try:
        response.raise_for_status()
    except requests.HTTPError() as e:
        status_code = e.response.status_code
        print(status_code)