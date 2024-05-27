from typing import Optional

import requests


class RestClient:
    STAT_TIMEOUT = 5
    READ_TIMEOUT = 10

    def __init__(self, base_url: str, cert_file_path: Optional[str] = None):
        self.base_url = base_url
        self.cert_file_path = cert_file_path

    def stat(self, uuid: str) -> dict:
        """Requests file metadata.

        Args:
            uuid: unique file identifier

        Returns:
            file metadata as json dict

        Raises:
            requests.HTTPError
            requests.RequestException
        """
        resp = requests.get(f"{self.base_url}/file/{uuid}/stat",
                            cert=self.cert_file_path,
                            timeout=self.STAT_TIMEOUT)
        resp.raise_for_status()

        return resp.json()

    def read(self, uuid: str) -> bytes:
        """Requests file content.

        Args:
            uuid: unique file identifier

        Returns:
            file content

        Raises:
            requests.HTTPError
            requests.RequestException
        """
        resp = requests.get(f"{self.base_url}/file/{uuid}/read",
                            cert=self.cert_file_path,
                            timeout=self.READ_TIMEOUT)
        resp.raise_for_status()

        return resp.content
