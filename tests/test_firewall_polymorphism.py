import pytest

from ban_engine.firewall.base import FirewallBackend
from ban_engine.firewall.dry_run import DryRunFirewallBackend

def test_firewall_backend_is_abstract() -> None:


   with pytest.raises(TypeError):
       FirewallBackend()

def test_dry_run_backend_is_firewall_backend() -> None:
   backend = DryRunFirewallBackend()


   assert isinstance(backend, FirewallBackend)

def test_dry_run_backend_blocks_ip() -> None:
   backend = DryRunFirewallBackend()


   backend.block_ip("192.168.1.10")


   assert backend.is_blocked("192.168.1.10") is True

def test_dry_run_backend_unblocks_ip() -> None:
   backend = DryRunFirewallBackend()
   backend.block_ip("192.168.1.10")


   backend.unblock_ip("192.168.1.10")


   assert backend.is_blocked("192.168.1.10") is False

def test_dry_run_backend_unblocks_ip() -> None:
   backend = DryRunFirewallBackend()
   backend.block_ip("192.168.1.10")


   backend.unblock_ip("192.168.1.10")


   assert backend.is_blocked("192.168.1.10") is False
