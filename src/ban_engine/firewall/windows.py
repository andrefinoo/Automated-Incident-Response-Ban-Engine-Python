import subprocess

from .base import FirewallBackend

class WindowsFirewallBackend(FirewallBackend):

   def block_ip(self, ip: str) -> None:
       rule_name = f"BanEngine-{ip}"


       subprocess.run(
           [
               "netsh",
               "advfirewall",
               "firewall",
               "add",
               "rule",
               f"name={rule_name}",
               "dir=in",
               "action=block",
               f"remoteip={ip}",
           ],
           check=True,
       )

   def unblock_ip(self, ip: str) -> None:
       rule_name = f"BanEngine-{ip}"

       subprocess.run(
           [
               "netsh",
               "advfirewall",
               "firewall",
               "delete",
               "rule",
               f"name={rule_name}",
           ],
           check=True,
       )

   def is_blocked(self, ip: str) -> bool:
       rule_name = f"BanEngine-{ip}"

       result = subprocess.run(
           [
               "netsh",
               "advfirewall",
               "firewall",
               "show",
               "rule",
               f"name={rule_name}",
           ],
           check=False,
           capture_output=True,
           text=True,
       )

       return result.returncode == 0 and rule_name in result.stdout
