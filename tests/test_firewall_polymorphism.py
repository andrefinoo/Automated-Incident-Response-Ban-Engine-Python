"""Test della gerarchia dei backend firewall."""

import pytest

from ban_engine.firewall.base import FirewallBackend


def test_firewall_backend_is_abstract() -> None:
    """La classe astratta non può essere istanziata direttamente."""
    with pytest.raises(TypeError):
        FirewallBackend()