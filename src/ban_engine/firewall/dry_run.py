from .base import FirewallBackend

class DryRunFirewallBackend(FirewallBackend):

   def __init__(self) -> None:
       self.blocked_ips: set[str] = set()

   def block_ip(self, ip: str) -> None:
       self.blocked_ips.add(ip)
       print(f"[DRY-RUN] Blocco IP: {ip}")

   def unblock_ip(self, ip: str) -> None:
       self.blocked_ips.discard(ip)
       print(f"[DRY-RUN] Sblocco IP: {ip}")

   def is_blocked(self, ip: str) -> bool:
       return ip in self.blocked_ips
