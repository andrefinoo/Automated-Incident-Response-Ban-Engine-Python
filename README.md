# Automated Incident Response Ban Engine

Repository del progetto finale di laboratorio Python di Andrea Finocchielli e Alessio Ordazzo.

Il progetto consiste in una CLI didattica che analizza log SSH, rileva tentativi di brute-force e decide se un indirizzo IP deve essere bloccato quando supera una soglia configurabile in una finestra temporale.

La modalità `dry-run` permette di simulare il ban senza modificare realmente il firewall del sistema, così la demo resta sicura e controllabile.

## Obiettivo del progetto

L'obiettivo è realizzare un piccolo motore di risposta agli incidenti ispirato a strumenti come Fail2ban.

Il programma dovrà:

- leggere log SSH da file;
- riconoscere tentativi di login falliti;
- estrarre e validare indirizzi IPv4 e IPv6;
- raggruppare i tentativi per IP;
- applicare una soglia di ban;
- ignorare gli IP presenti in whitelist;
- usare backend firewall polimorfici;
- salvare configurazione e stato in JSON;
- fornire test automatici con pytest.

## Requisiti

- Python 3.11+
- pytest

Le dipendenze sono indicate in:

```bash
requirements.txt
```

## Setup del progetto

Clonare il repository:

```bash
git clone https://github.com/andrefinoo/Automated-Incident-Response-Ban-Engine-Python.git
cd Automated-Incident-Response-Ban-Engine-Python
```

Creare l'ambiente virtuale:

```bash
python -m venv .venv
```

Attivare l'ambiente virtuale su Windows PowerShell:

```powershell
.venv\Scripts\activate
```

Attivare l'ambiente virtuale su Linux/macOS:

```bash
source .venv/bin/activate
```

Installare le dipendenze:

```bash
pip install -r requirements.txt
```

## Comandi principali previsti

Su Windows PowerShell:

```powershell
$env:PYTHONPATH="src"
python -m ban_engine --help
```

Esecuzione in modalità dry-run:

```powershell
$env:PYTHONPATH="src"
python -m ban_engine --log examples/auth.log --config examples/config.json --dry-run
```

Su Linux/macOS:

```bash
PYTHONPATH=src python -m ban_engine --help
```

Esecuzione in modalità dry-run:

```bash
PYTHONPATH=src python -m ban_engine --log examples/auth.log --config examples/config.json --dry-run
```

## Test

Su Windows PowerShell:

```powershell
$env:PYTHONPATH="src"
pytest -q
```

Su Linux/macOS:

```bash
PYTHONPATH=src pytest -q
```

## Struttura del repository

```text
docs/                  documentazione del progetto
examples/              file di esempio per demo e test
src/ban_engine/        codice sorgente principale
src/ban_engine/firewall/ backend firewall
tests/                 test automatici con pytest
requirements.txt       dipendenze del progetto
README.md              guida iniziale del repository
```

## Architettura prevista

La parte OOP principale riguarda i backend firewall.

La classe base astratta sarà `FirewallBackend`, con metodi comuni come:

- `block_ip(ip: str)`
- `unblock_ip(ip: str)`
- `is_blocked(ip: str)`

Le sottoclassi previste sono:

- `DryRunFirewallBackend`
- `LinuxIptablesBackend`
- `WindowsFirewallBackend`

L'engine userà il tipo astratto `FirewallBackend`, senza dipendere direttamente dal sistema operativo. Questo permette di usare il polimorfismo per cambiare backend senza modificare la logica centrale.

## Stato del progetto

Il progetto è in fase di sviluppo.  
La prima milestone consiste nel rendere il repository ordinato, documentato, testabile e pronto per implementare il core applicativo.