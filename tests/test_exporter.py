import socket  # noqa: F401
from unittest.mock import MagicMock, patch

from streamlit_prometheus.exporter import (
    _port_is_open,
    start_exporter,
    start_exporter_thread,
)


@patch("streamlit_prometheus.exporter.socket")
def test__port_is_open(mock_socket_cls):
    mock_sock = MagicMock()
    mock_socket_cls.return_value.__enter__.return_value = mock_sock
    mock_sock.connect_ex.return_value = 0

    result = _port_is_open(8080)

    assert result is True
    mock_sock.settimeout.assert_called_once_with(0.5)
    mock_sock.connect_ex.assert_called_once_with(("127.0.0.1", 8080))


@patch("streamlit_prometheus.exporter.socket")
def test__port_is_closed(mock_socket_cls):
    mock_sock = MagicMock()
    mock_socket_cls.return_value.__enter__.return_value = mock_sock
    mock_sock.connect_ex.return_value = 111  # non-zero → closed

    result = _port_is_open(8080)

    assert result is False


@patch("streamlit_prometheus.exporter.socket")
def test_custom_host(mock_socket_cls):
    mock_sock = MagicMock()
    mock_socket_cls.return_value.__enter__.return_value = mock_sock
    mock_sock.connect_ex.return_value = 0

    _port_is_open(5432, host="localhost")

    mock_sock.connect_ex.assert_called_once_with(("localhost", 5432))


@patch("streamlit_prometheus.exporter.start_http_server")
def test_start_exporter_starts_server_and_logs(mock_start_http_server):
    port = 8000

    start_exporter(port)

    mock_start_http_server.assert_called_once_with(port)


@patch("streamlit_prometheus.exporter.Thread")
def test_start_exporter_thread_creates_and_starts_thread(mock_thread_cls):
    mock_thread = MagicMock()
    mock_thread_cls.return_value = mock_thread

    start_exporter_thread(9100)

    mock_thread_cls.assert_called_once()
    mock_thread.start.assert_called_once()
