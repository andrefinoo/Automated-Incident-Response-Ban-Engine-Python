import pytest
from unittest.mock import patch


from ban_engine.firewall.linux import LinuxIptablesBackend
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


@patch("ban_engine.firewall.linux.subprocess.run")
def test_linux_backend_blocks_ip(mock_run) -> None:
   backend = LinuxIptablesBackend()


   backend.block_ip("192.168.1.10")


   mock_run.assert_called_once_with(
       [
           "iptables",
           "-A",
           "INPUT",
           "-s",
           "192.168.1.10",
           "-j",
           "DROP",
       ],
       check=True,
   )


@patch("ban_engine.firewall.linux.subprocess.run")
def test_linux_backend_unblocks_ip(mock_run) -> None:
   backend = LinuxIptablesBackend()


   backend.unblock_ip("192.168.1.10")


   mock_run.assert_called_once_with(
       [
           "iptables",
           "-D",
           "INPUT",
           "-s",
           "192.168.1.10",
           "-j",
           "DROP",
       ],
       check=True,
   )


@patch("ban_engine.firewall.linux.subprocess.run")
def test_linux_backend_detects_blocked_ip(mock_run) -> None:
   mock_run.return_value.returncode = 0
   backend = LinuxIptablesBackend()


   result = backend.is_blocked("192.168.1.10")


   assert result is True
   mock_run.assert_called_once_with(
       [
           "iptables",
           "-C",
           "INPUT",
           "-s",
           "192.168.1.10",
           "-j",
           "DROP",
       ],
       check=False,
       capture_output=True,
   )


@patch("ban_engine.firewall.linux.subprocess.run")
def test_linux_backend_detects_unblocked_ip(mock_run) -> None:
   mock_run.return_value.returncode = 1
   backend = LinuxIptablesBackend()


   result = backend.is_blocked("192.168.1.10")


   assert result is False
