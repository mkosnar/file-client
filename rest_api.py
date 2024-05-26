import requests


def stat(base_url: str, uuid: str) -> dict:
    """

    Returns:
        file metadata as json dict

    Raises:
        requests.HTTPError
        requests.RequestException
    """
    resp = requests.get(f"{base_url}/file/{uuid}/stat", timeout=5)
    resp.raise_for_status()

    return resp.json()


def read(base_url: str, uuid: str) -> bytes:
    """

    Returns:
        file content

    Raises:
        requests.HTTPError
        requests.RequestException
    """
    resp = requests.get(f"{base_url}/file/{uuid}/read", timeout=5)
    resp.raise_for_status()

    return resp.content
