from __future__ import annotations
from dataclasses import dataclass

import streamlit as st


@dataclass
class PrometheusConfig:
    enabled: bool = False
    exporter_port: int = 9101


    @classmethod
    def from_streamlit_config(cls) -> PrometheusConfig:
        config = PrometheusConfig()
        enabled = st.get_option("prometheus.enabled")
        if isinstance(enabled, bool):
            config.enabled = enabled

        exporter_port = st.get_option("prometheus.port")
        if isinstance(exporter_port, int):
            config.exporter_port = exporter_port

        return config
