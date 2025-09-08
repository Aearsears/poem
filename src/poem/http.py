import http.client
import json
from urllib.parse import urlsplit
import logging

logger = logging.getLogger(__name__)


class HTTPClient:
    def __init__(self, host: str, port: int = None, timeout: int = 30):
        parsed_url = urlsplit(host)
        _host = parsed_url.hostname
        self.scheme = parsed_url.scheme
        if self.scheme == 'https':
            self.conn = http.client.HTTPSConnection(_host)
        else:
            self.conn = http.client.HTTPConnection(_host)
        self.timeout = timeout

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()

    def get(self, path: str, headers: dict = None) -> dict:
        """Send a GET request to path, relative to the initialized host."""
        logging.debug(
            f"GET {path} -> scheme: {self.scheme}, host: {self.conn.host}, path: {path}")

        self.conn.request("GET", path, headers=headers)
        res = self.conn.getresponse()
        raw_data = res.read()
        logging.debug(f"Response data size: {len(raw_data)} bytes")
        data = json.loads(raw_data.decode("utf-8"))
        return data

    @staticmethod
    def get_host(url: str) -> tuple[str | None, str | None, str | None]:
        """Extract the host from a URL."""
        parsed_url = urlsplit(url)
        return parsed_url.scheme, parsed_url.hostname, parsed_url.path


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
