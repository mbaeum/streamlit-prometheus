import logging
from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread

from prometheus_client import start_http_server

logger = logging.getLogger("streamlit-observe")


def _port_is_open(port: int, host: str = "127.0.0.1") -> bool:
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.settimeout(0.5)
        return sock.connect_ex((host, port)) == 0


def start_exporter(port: int):
    logger.info(f"Starting Prometheus exporter on :{port}")
    start_http_server(port)


def start_exporter_thread(port: int):
    thread = Thread(
        target=start_exporter,
        args=(port,),
        daemon=True,
        name="streamlit-observe-exporter",
    )
    thread.start()
