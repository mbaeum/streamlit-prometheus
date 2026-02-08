import logging
from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread

from prometheus_client import start_http_server

logger = logging.getLogger("streamlit-observe")

_DEFAULT_HOST = "127.0.0.1"


def _port_is_open(port: int, host: str = _DEFAULT_HOST) -> bool:
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.settimeout(0.5)
        return sock.connect_ex((host, port)) == 0


def _start_exporter(port: int, host: str = _DEFAULT_HOST):
    logger.info(f"Starting Prometheus exporter on :{port}")
    start_http_server(port=port, addr=host)


def _start_exporter_thread(port: int, host: str = _DEFAULT_HOST):
    thread = Thread(
        target=_start_exporter,
        args=(
            port,
            host,
        ),
        daemon=True,
        name="streamlit-observe-exporter",
    )
    thread.start()


def _start_once(port: int, host: str = _DEFAULT_HOST):
    if not _port_is_open(port, host):
        logger.info(f"Exporter already running on port {port}")
    else:
        _start_exporter_thread(port)
