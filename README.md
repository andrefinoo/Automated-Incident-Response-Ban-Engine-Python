# Automated Incident Response Ban Engine

CLI didattica in Python che analizza log SSH, rileva tentativi di brute-force e blocca gli IP sospetti tramite backend firewall polimorfici. La modalità `--dry-run` permette di mostrare le azioni senza modificare il firewall reale.

## Setup

```bash
git clone https://github.com/andrefinoo/Automated-Incident-Response-Ban-Engine-Python
cd Automated Incident Response Ban Engine
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Avvio rapido

```bash
python -m ban_engine --help
python -m ban_engine scan examples/auth.log --dry-run --threshold 3 --window-minutes 10
python -m ban_engine status --state-file data/state.json
```

## Test

```bash
pytest
```

## Struttura

```text
src/ban_engine/       codice sorgente
tests/                test pytest
docs/                 documentazione di progetto
examples/             log di esempio per demo sicura
```
