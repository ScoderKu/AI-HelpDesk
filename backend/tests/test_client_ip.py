import ipaddress
import os
import unittest
from unittest.mock import patch

os.environ.setdefault("MYSQL_USER", "test")
os.environ.setdefault("MYSQL_PASSWORD", "test")
os.environ.setdefault("MYSQL_DATABASE", "test")

from fastapi import Request

from app import main


def make_request(peer_ip: str, forwarded_for: str | None = None) -> Request:
    headers = []
    if forwarded_for is not None:
        headers.append((b"x-forwarded-for", forwarded_for.encode("ascii")))

    return Request(
        {
            "type": "http",
            "http_version": "1.1",
            "method": "GET",
            "scheme": "http",
            "path": "/",
            "raw_path": b"/",
            "query_string": b"",
            "headers": headers,
            "client": (peer_ip, 12345),
            "server": ("localhost", 8000),
        }
    )


class GetClientIpTests(unittest.TestCase):
    def test_ignores_forwarded_header_from_untrusted_peer(self) -> None:
        with patch.object(main, "TRUSTED_PROXY_NETWORKS", ()):
            request = make_request("192.0.2.10", "198.51.100.25")

            self.assertEqual(main.get_client_ip(request), "192.0.2.10")

    def test_extracts_client_ip_from_single_trusted_proxy(self) -> None:
        networks = (ipaddress.ip_network("172.30.0.2/32"),)
        with patch.object(main, "TRUSTED_PROXY_NETWORKS", networks):
            request = make_request("172.30.0.2", "192.0.2.10")

            self.assertEqual(main.get_client_ip(request), "192.0.2.10")

    def test_clients_behind_same_proxy_get_distinct_ip_keys(self) -> None:
        networks = (ipaddress.ip_network("172.30.0.2/32"),)
        with patch.object(main, "TRUSTED_PROXY_NETWORKS", networks):
            first_client = make_request("172.30.0.2", "192.0.2.10")
            second_client = make_request("172.30.0.2", "192.0.2.11")

            self.assertNotEqual(
                main.get_client_ip(first_client),
                main.get_client_ip(second_client),
            )

    def test_skips_trusted_hops_and_untrusted_header_prefix(self) -> None:
        networks = (ipaddress.ip_network("172.30.0.0/24"),)
        with patch.object(main, "TRUSTED_PROXY_NETWORKS", networks):
            request = make_request(
                "172.30.0.2",
                "198.51.100.200, 192.0.2.10, 172.30.0.3",
            )

            self.assertEqual(main.get_client_ip(request), "192.0.2.10")

    def test_malformed_header_falls_back_to_trusted_peer(self) -> None:
        networks = (ipaddress.ip_network("172.30.0.2/32"),)
        with patch.object(main, "TRUSTED_PROXY_NETWORKS", networks):
            request = make_request("172.30.0.2", "not-an-ip")

            self.assertEqual(main.get_client_ip(request), "172.30.0.2")

    def test_missing_header_falls_back_to_trusted_peer(self) -> None:
        networks = (ipaddress.ip_network("172.30.0.2/32"),)
        with patch.object(main, "TRUSTED_PROXY_NETWORKS", networks):
            request = make_request("172.30.0.2")

            self.assertEqual(main.get_client_ip(request), "172.30.0.2")


if __name__ == "__main__":
    unittest.main()
