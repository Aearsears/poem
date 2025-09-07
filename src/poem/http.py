import http.client
import json
from urllib.parse import urlsplit
import logging

logger = logging.getLogger(__name__)


class HTTP:
    @staticmethod
    def get(url: str, headers: dict = None) -> dict:
        """Send a GET request."""
        scheme, host, path = HTTP.get_host(url)
        logging.debug(
            f"GET {url} -> scheme: {scheme}, host: {host}, path: {path}")

        if scheme == 'https':
            conn = http.client.HTTPSConnection(host)
        else:
            conn = http.client.HTTPConnection(host)

        conn.request("GET", path, headers=headers)
        res = conn.getresponse()
        raw_data = res.read()
        logging.debug(f"Response data size: {len(raw_data)} bytes")
        data = json.loads(raw_data.decode("utf-8"))
        conn.close()
        return data

    @staticmethod
    def get_host(url: str) -> tuple[str | None, str | None, str | None]:
        """Extract the host from a URL."""
        parsed_url = urlsplit(url)
        return parsed_url.scheme, parsed_url.hostname, parsed_url.path
