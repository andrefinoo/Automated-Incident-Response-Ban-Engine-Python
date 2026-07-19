# Manuale utente — Automated Incident Response Ban Engine

## 1. A cosa serve

Il programma legge un file di log SSH e cerca tentativi di accesso falliti. Quando lo stesso indirizzo IP produce troppi eventi in poco tempo, il programma può:

- simulare il blocco, senza modificare il computer;
- aggiungere una regola al firewall Linux;
- aggiungere una regola a Windows Firewall.

Per le prime prove usa sempre la modalità **dry-run**. È il comportamento predefinito ed è sicuro anche senza privilegi di amministratore.

## 2. Prima installazione

### 2.1 Apri il terminale nella cartella del progetto

La cartella deve contenere almeno:

- `requirements.txt`;
- `pyproject.toml`;
- `src/`;
- `examples/`.

### 2.2 Crea un ambiente virtuale

```bash
python -m venv .venv
```

### 2.3 Attiva l'ambiente

Linux o macOS:

```bash
source .venv/bin/activate
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Windows Prompt dei comandi:

```cmd
.venv\Scripts\activate.bat
```

### 2.4 Installa il progetto

```bash
python -m pip install -r requirements.txt
```

### 2.5 Controlla che la CLI funzioni

```bash
python -m ban_engine --help
```

Non usare il file `main.py` presente nella root: l'applicazione si avvia con `python -m ban_engine`.

## 3. Prima esecuzione sicura

Il repository contiene già un log e una configurazione di esempio.

```bash
python -m ban_engine \
  --log examples/auth.log \
  --config examples/config.json \
  --dry-run
```

Su Windows puoi scrivere il comando su una sola riga:

```powershell
python -m ban_engine --log examples/auth.log --config examples/config.json --dry-run
```

Durante la simulazione possono comparire messaggi simili a:

```text
[DRY-RUN] Blocco IP: 192.0.2.10
```

Alla fine viene stampato un riepilogo:

```text
Analisi completata
Righe analizzate: ...
Tentativi falliti riconosciuti: ...
IP sospetti: ...
IP in whitelist: ...
IP bannati: ...
```

Il dry-run non crea regole nel firewall. Conserva i blocchi solo nella memoria del processo e li perde alla chiusura.

## 4. Uso senza file di configurazione

Puoi eseguire il programma usando i valori predefiniti:

```bash
python -m ban_engine --log examples/auth.log --dry-run
```

Valori predefiniti:

- soglia: `3` tentativi;
- finestra: `300` secondi;
- whitelist vuota;
- backend dry-run;
- storico: `ban_state.json`.

## 5. Opzioni disponibili

| Opzione | Obbligatoria | Esempio | Funzione |
|---|---:|---|---|
| `--log` | sì | `--log examples/auth.log` | Indica il file da analizzare |
| `--config` | no | `--config examples/config.json` | Carica la configurazione JSON |
| `--dry-run` | no | `--dry-run` | Forza la simulazione sicura |
| `--threshold` | no | `--threshold 5` | Cambia la soglia per questa esecuzione |
| `--window` | no | `--window 120` | Cambia la finestra in secondi |
| `--state` | no | `--state output/history.json` | Cambia il file dello storico |

Esempio con valori personalizzati:

```bash
python -m ban_engine \
  --log examples/auth.log \
  --dry-run \
  --threshold 5 \
  --window 180 \
  --state output/ban_history.json
```

Gli argomenti della riga di comando hanno precedenza sui valori presenti nel file di configurazione per soglia, finestra, dry-run e percorso dello storico.

## 6. Preparare il file di configurazione

Crea un file JSON simile a questo:

```json
{
  "max_attempts": 3,
  "window_seconds": 120,
  "whitelist": [
    "127.0.0.1",
    "::1"
  ],
  "backend": "dry-run",
  "dry_run": true,
  "state_file": "examples/ban_state.json"
}
```

### Significato dei campi

- `max_attempts`: quanti eventi servono per bloccare l'IP. La soglia è inclusiva: con valore `3`, il terzo evento nella finestra produce il ban.
- `window_seconds`: intervallo di tempo usato per raggruppare gli eventi.
- `whitelist`: indirizzi che non devono essere bloccati.
- `backend`: `dry-run`, `linux` oppure `windows`.
- `dry_run`: se è `true`, il programma simula sempre il blocco.
- `state_file`: file JSON dove salvare lo storico.

Il JSON usa:

- virgolette doppie;
- `true` e `false` in minuscolo;
- virgole tra i campi, ma non dopo l'ultimo elemento.

## 7. Whitelist

La whitelist serve a proteggere indirizzi conosciuti, per esempio il localhost o un host amministrativo.

```json
"whitelist": [
  "127.0.0.1",
  "192.168.1.10",
  "2001:db8::1"
]
```

Gli indirizzi vengono validati all'avvio. Un valore non valido interrompe l'esecuzione con un messaggio di errore.

## 8. Cambiare soglia e finestra

### Da configurazione

```json
{
  "max_attempts": 5,
  "window_seconds": 60
}
```

Significa: blocca un IP quando raggiunge almeno cinque eventi riconosciuti in una finestra di sessanta secondi.

### Solo per una singola esecuzione

```bash
python -m ban_engine --log examples/auth.log --dry-run --threshold 5 --window 60
```

Questa modifica non riscrive il file di configurazione.

## 9. Storico dei ban

Quando il programma produce una decisione di ban, la salva nel file indicato da `state_file` o `--state`.

Esempio:

```json
[
  {
    "ip": "192.0.2.10",
    "attempts_count": 3,
    "window_seconds": 60,
    "reason": "3 tentativi falliti in 60 secondi",
    "created_at": "2026-07-19T10:30:00"
  }
]
```

Le nuove decisioni vengono aggiunte a quelle esistenti. Se il file non esiste, viene creato. Se non ci sono nuovi ban, il file non viene modificato.

Lo storico è un registro delle decisioni. Non viene usato per ricreare automaticamente le regole firewall al riavvio.

## 10. Usare il firewall reale

### Attenzione

Esegui questa modalità soltanto su una macchina di test o su un sistema che sei autorizzato ad amministrare. Una regola errata può interrompere connessioni legittime, compreso l'accesso remoto alla macchina.

Il flag `--dry-run` può solo attivare la simulazione. Per usare un backend reale devi modificare il file JSON impostando `dry_run` a `false`.

### Linux con iptables

Configurazione:

```json
{
  "backend": "linux",
  "dry_run": false
}
```

Avvio tipico:

```bash
sudo .venv/bin/python -m ban_engine --log /var/log/auth.log --config config.json
```

Requisiti:

- `iptables` installato;
- privilegi amministrativi;
- accesso al file di log.

Il programma aggiunge regole in ingresso con azione `DROP`.

### Windows Firewall

Configurazione:

```json
{
  "backend": "windows",
  "dry_run": false
}
```

Apri PowerShell come amministratore e avvia:

```powershell
python -m ban_engine --log .\auth.log --config .\config.json
```

Le regole create hanno nomi simili a:

```text
BanEngine-192.0.2.10
```

## 11. Quali righe vengono riconosciute

Il parser cerca principalmente:

- `Failed password`;
- `Failed publickey`;
- `Invalid user`.

Esempio valido:

```text
Jul 16 08:00:00 server sshd[1]: Failed password for root from 192.0.2.10 port 22 ssh2
```

Le righe come `Accepted password` vengono ignorate.

Il parser può contare separatamente una riga `Invalid user` e la successiva riga `Failed password`, anche quando appartengono allo stesso tentativo. Quando scegli la soglia, tieni conto di questo comportamento.

## 12. Come leggere il report

- **Righe analizzate:** tutte le righe presenti nel file.
- **Tentativi falliti riconosciuti:** righe trasformate in eventi dal parser.
- **IP sospetti:** indirizzi diversi presenti negli eventi riconosciuti.
- **IP in whitelist:** indirizzi sospetti esclusi perché autorizzati.
- **IP bannati:** nuove decisioni di blocco prodotte in questa esecuzione.

Un IP sospetto non è sempre bannato. Può essere sotto soglia, in whitelist o già considerato bloccato dal backend.

## 13. Errori comuni

### `File di configurazione non trovato`

Controlla il percorso dopo `--config`.

```bash
python -m ban_engine --log examples/auth.log --config examples/config.json
```

### `JSON non valido`

Controlla virgolette, virgole e valori booleani. Il messaggio indica la riga del problema.

### `Indirizzo IP non valido`

Un indirizzo nella whitelist o nel log non è riconosciuto come IPv4 o IPv6 valido.

### `No module named ban_engine`

Esegui l'installazione dalla root:

```bash
python -m pip install -r requirements.txt
```

Verifica anche che l'ambiente virtuale sia attivo.

### `iptables` o `netsh` non trovato

Hai selezionato un backend non disponibile sul sistema. Torna al dry-run oppure scegli il backend corretto nel file JSON.

### Permesso negato

I backend reali richiedono privilegi amministrativi. Il dry-run non li richiede.

### Exit code `2`

Il programma usa il codice `2` per errori di input, file, configurazione, sistema o comando firewall. Il codice `0` indica un'esecuzione completata.

## 14. Eseguire i test

Dalla root del repository:

```bash
python -m pytest -q
```

I test dei backend reali non modificano il firewall: le chiamate di sistema vengono simulate.

## 15. Comportamenti non presenti

La versione attuale:

- non segue il log in tempo reale;
- non offre un comando CLI per sbloccare un IP;
- non sceglie automaticamente Linux o Windows;
- non ripristina i blocchi leggendo lo storico;
- non sostituisce strumenti di produzione come Fail2ban.

