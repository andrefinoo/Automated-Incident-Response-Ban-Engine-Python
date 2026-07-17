import subprocess

from .base import FirewallBackend

class LinuxIptablesBackend(FirewallBackend):


   def block_ip(self, ip: str) -> None:
       command = [
           "iptables",
           "-A",
           "INPUT",
           "-s",
           ip,
           "-j",
           "DROP",
       ]


       subprocess.run(command, check=True)


   def unblock_ip(self, ip: str) -> None:
       command = [
           "iptables",
           "-D",
           "INPUT",
           "-s",
           ip,
           "-j",
           "DROP",
       ]


       subprocess.run(command, check=True)


   def is_blocked(self, ip: str) -> bool:
       command = [
           "iptables",
           "-C",
           "INPUT",
           "-s",
           ip,
           "-j",
           "DROP",
       ]


       result = subprocess.run(
           command,
           check=False,
           capture_output=True,
       )


       return result.returncode == 0
