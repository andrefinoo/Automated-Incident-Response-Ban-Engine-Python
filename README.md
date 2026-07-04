@'
# Automated Incident Response Ban Engine

CLI didattica in Python che analizza log SSH, rileva tentativi di brute-force e blocca o simula il blocco degli IP sospetti tramite backend firewall polimorfici.

La modalità `--dry-run` consente di mostrare le azioni previste senza modificare il firewall reale, rendendo il progetto sicuro per test, demo e discussione orale.

## Requisiti

- Python 3.11+
- pytest

## Setup

```bash
git clone https://github.com/andrefinoo/Automated-Incident-Response-Ban-Engine-Python.git
cd Automated-Incident-Response-Ban-Engine-Python
python -m venv .venv