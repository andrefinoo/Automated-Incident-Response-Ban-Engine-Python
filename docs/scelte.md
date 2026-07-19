# Scelte implementative

Questo documento raccoglie le decisioni tecniche che hanno richiesto un confronto tra più alternative. L'obiettivo non è elencare ogni riga di codice, ma spiegare perché il progetto è stato organizzato in questo modo e quali compromessi sono stati accettati.

## 1. Ereditarietà per i backend firewall

### Problema

Linux, Windows e la modalità di simulazione devono offrire le stesse operazioni, ma le eseguono in modo diverso.

### Scelta

Abbiamo definito la classe astratta `FirewallBackend` con tre metodi:

```python
block_ip(ip: str) -> None
unblock_ip(ip: str) -> None
is_blocked(ip: str) -> bool
```

Le sottoclassi concrete sono:

- `DryRunFirewallBackend`;
- `LinuxIptablesBackend`;
- `WindowsFirewallBackend`.

### Perché l'ereditarietà è adatta

La relazione “è un” è corretta: ogni classe concreta **è un backend firewall** e deve rispettare lo stesso contratto. Il motore può ricevere un riferimento di tipo `FirewallBackend` e chiamare gli stessi metodi senza conoscere la sottoclasse.

Questo è il punto di polimorfismo:

```python
self.backend.block_ip(ip)
```

Il metodo eseguito dipende dall'oggetto concreto ricevuto a runtime.

### Alternative scartate

**Funzioni separate**, come `block_ip_linux()` e `block_ip_windows()`, avrebbero obbligato il chiamante a scegliere ogni volta la funzione corretta.

**Una catena di `if` dentro l'engine** avrebbe accoppiato la logica di rilevamento al sistema operativo:

```python
if backend == "linux":
    ...
elif backend == "windows":
    ...
```

Ogni nuovo backend avrebbe richiesto una modifica al motore.

**Solo composizione senza contratto comune** avrebbe permesso di passare oggetti diversi, ma senza garantire in modo esplicito che implementassero tutte le operazioni richieste.

### Compromesso

La gerarchia introduce più file e classi rispetto a una soluzione procedurale. In cambio offre un'interfaccia chiara, test isolati ed estensione più semplice.

## 2. Composizione tra engine e backend

L'ereditarietà non viene usata ovunque. `IncidentResponseEngine` non eredita da `FirewallBackend`, perché un motore di risposta agli incidenti non è un firewall.

La relazione corretta è “ha un”:

```python
class IncidentResponseEngine:
    def __init__(self, backend: FirewallBackend, ...):
        self.backend = backend
```

Qui abbiamo usato composizione e dependency injection. Il backend viene fornito dall'esterno, quindi il motore può essere testato con il dry-run o con un oggetto controllato.

## 3. Dry-run come backend autonomo

### Problema

I test e la demo non devono modificare il firewall reale o richiedere privilegi amministrativi.

### Scelta

`DryRunFirewallBackend` implementa lo stesso contratto degli altri backend e conserva gli IP in un `set`.

### Perché non un semplice flag nei backend reali

Aggiungere `if dry_run` dentro Linux e Windows avrebbe duplicato condizioni e mescolato simulazione e comandi reali. Un backend autonomo rappresenta invece una strategia completa e sostituibile.

### Compromesso

Lo stato del dry-run vive solo in memoria e viene perso alla chiusura. È corretto per test e demo, ma non simula una persistenza reale del firewall.

## 4. `set` per whitelist e IP bloccati

Whitelist e IP bloccati non devono contenere duplicati. Il `set` rende naturale questa regola e offre un controllo di appartenenza diretto:

```python
if ip in self.whitelist:
    continue
```

Una lista avrebbe funzionato, ma avrebbe permesso duplicati e richiesto una ricerca lineare. L'ordine non è necessario in questi due casi, quindi il `set` è più adatto.

## 5. Dataclass per i modelli del dominio

`LoginAttempt`, `BanDecision` e `AppConfig` sono dataclass.

La scelta riduce il codice ripetitivo per costruttori e rappresentazione degli oggetti, lasciando visibili i campi principali. Abbiamo aggiunto `__post_init__()` soltanto dove serve validazione.

Alternative come dizionari grezzi avrebbero reso più facile sbagliare il nome di una chiave e avrebbero nascosto il significato dei dati. 

## 6. Validazione IP con `ipaddress`

Abbiamo usato `ipaddress.ip_address()` invece di scrivere una regex completa per IPv4 e IPv6.

Vantaggi:

- supporto della libreria standard;
- gestione sia IPv4 sia IPv6;
- normalizzazione degli indirizzi;
- errore chiaro su input non valido;
- meno codice da mantenere e testare.

Le regex restano adatte a trovare il testo dell'indirizzo dentro una riga di log, ma non sono state usate come validatore definitivo.

## 7. Pattern SSH separati

Il parser usa pattern distinti per:

- password fallita;
- chiave pubblica fallita;
- utente non valido.

Un'unica regex avrebbe ridotto il numero di variabili, ma sarebbe stata più difficile da leggere e modificare. I pattern separati permettono di collegare ogni formato a un test specifico.

Abbiamo limitato il parser ai casi necessari all'MVP. Non prova a interpretare qualsiasi possibile distribuzione o configurazione SSH, perché un parser universale avrebbe aumentato molto la complessità.

## 8. Riga non pertinente restituita come `None`

`parse_line()` restituisce `None` quando la riga non rappresenta un evento gestito.

Questa scelta evita di usare eccezioni per un caso normale. Un log contiene molte righe valide ma non interessanti, quindi ignorarle è parte del flusso previsto, non un errore.

Gli errori vengono invece mantenuti per dati realmente invalidi, come un indirizzo IP malformato in una riga che corrisponde a un pattern.

## 9. Lettura del log riga per riga

`parse_file()` itera direttamente sul file. Non usa `read()` per caricare tutto in memoria.

La soluzione è semplice e può gestire file più grandi senza una crescita proporzionale della memoria usata dal parser. La lista finale dei tentativi viene comunque conservata in memoria perché l'engine attuale lavora su tutti gli eventi insieme.

## 10. Anno corrente per i timestamp SSH

I log OpenSSH usati dal progetto riportano mese, giorno e ora, ma non l'anno. Abbiamo aggiunto l'anno corrente per ottenere un `datetime` completo.

Alternative considerate:

- chiedere l'anno come argomento CLI;
- dedurlo dal nome o dalla data del file;
- mantenere un timestamp parziale;
- usare sempre l'ora di lettura.

Per l'MVP l'anno corrente è la soluzione più semplice. Il compromesso è che un log storico analizzato in un anno diverso riceve timestamp non corretti. Il fallback a `datetime.now()` evita un crash, ma può alterare il conteggio temporale: per una versione di produzione sarebbe preferibile segnalare o scartare la riga.

## 11. Algoritmo semplice per la finestra temporale

L'engine ordina gli eventi di ogni IP e prova ciascun evento come inizio di una finestra. Conta gli eventi successivi finché la differenza supera `window_seconds`.

La complessità nel caso peggiore è `O(n²)` per gli eventi dello stesso IP.

Abbiamo valutato una finestra scorrevole con due indici, più efficiente, ma scelto la versione con cicli annidati perché:

- è più semplice da testare;
- riduce il rischio di errori sugli estremi della finestra;
- i file di esempio hanno dimensioni limitate.

Il miglioramento è possibile senza cambiare l'interfaccia pubblica dell'engine.

## 12. Soglia inclusiva

Il blocco avviene quando:

```python
attempts_count >= max_attempts
```

Nel codice questa regola è espressa saltando il ban soltanto quando il conteggio è inferiore alla soglia.

Con soglia `3`, il terzo tentativo nella finestra genera una decisione. È una semantica intuitiva e viene verificata dai test.

## 13. Controllo di whitelist e duplicati prima del ban

Prima di contare e bloccare, l'engine:

1. salta gli IP in whitelist;
2. chiede al backend se l'IP è già bloccato.

Questo evita chiamate inutili e regole duplicate. Abbiamo mantenuto il controllo nel backend perché è il componente che conosce il proprio stato reale o simulato.

## 14. Configurazione JSON con valori predefiniti

JSON è stato scelto perché:

- fa parte degli argomenti del corso;
- è supportato dalla libreria standard;
- è leggibile;
- rappresenta bene liste, stringhe, numeri e booleani;
- è adatto sia a configurazione sia a storico.

`load_config()` può essere chiamata senza percorso e restituisce valori predefiniti. Questo rende possibile una prova rapida con il solo `--log`.

Un file indicato esplicitamente ma mancante produce errore. Non viene ignorato, perché l'utente ha dichiarato di voler usare proprio quel file.

## 15. Override da riga di comando

Soglia, finestra e percorso dello stato possono essere cambiati senza modificare il JSON. La CLI ha precedenza perché rappresenta la scelta più specifica per l'esecuzione corrente.

Il flag `--dry-run` può soltanto attivare la modalità sicura. Non esiste un flag per disattivarla. Per usare un backend reale bisogna impostare `dry_run: false` nel file di configurazione. Questa scelta riduce il rischio di attivare per errore un firewall reale con un singolo parametro digitato male.

## 16. Backend scelto dalla configurazione, non dal sistema operativo

`create_backend()` usa il nome ricevuto:

- `linux` crea `LinuxIptablesBackend`;
- `windows` crea `WindowsFirewallBackend`;
- ogni altro caso già validato porta al dry-run.

Il rilevamento automatico del sistema operativo era previsto nella proposta iniziale, ma non è presente nell'implementazione finale. La scelta esplicita è più prevedibile durante test e demo, anche se richiede una configurazione corretta da parte dell'utente.

## 17. Comandi `subprocess` come liste

I backend reali passano liste a `subprocess.run()` e non usano `shell=True`.

Questo rende più chiaro dove finisce un argomento e ne inizia un altro, evita l'interpretazione della shell e semplifica i test.

Per `block_ip()` e `unblock_ip()` viene usato `check=True`, perché un fallimento deve interrompere il flusso. Per `is_blocked()` viene usato `check=False`: un codice diverso da zero può significare semplicemente che la regola non esiste.

## 18. Mock dei comandi nei test

I test non devono cambiare il firewall della macchina che li esegue. `subprocess.run()` viene quindi sostituito con mock.

I test specifici controllano i comandi costruiti. Il test polimorfico usa `patch.object()` sui metodi delle istanze Linux e Windows, evitando interferenze tra patch applicate allo stesso modulo `subprocess`.

Abbiamo scartato l'idea di eseguire test reali condizionati al sistema operativo: avrebbero richiesto privilegi, lasciato regole residue e reso la suite poco ripetibile.

## 19. Storico preservato con lettura, estensione e riscrittura

Per aggiungere nuove decisioni:

1. viene caricato il contenuto esistente;
2. la lista viene estesa;
3. il file viene riscritto.

Non usiamo l'append testuale perché un documento JSON deve mantenere una struttura valida unica. Scrivere un oggetto dopo l'altro produrrebbe un file non leggibile da `json.load()`.

Il compromesso è che il costo cresce con lo storico e non esiste locking. Per l'MVP è accettabile; in un servizio concorrente sarebbe preferibile un database o una scrittura atomica con file temporaneo.

## 20. Errori convertiti in exit code

La CLI cattura errori prevedibili di file, configurazione, sistema e `subprocess`, stampa un messaggio su `stderr` e restituisce `2`.

Non abbiamo nascosto ogni eccezione con un `except Exception`, perché renderebbe più difficile riconoscere bug non previsti. Il codice `0` indica successo; `2` segnala un problema di input o esecuzione.

## 21. Uso quasi esclusivo della libreria standard

Il programma usa `argparse`, `abc`, `dataclasses`, `datetime`, `ipaddress`, `json`, `pathlib`, `re`, `subprocess` e `sys`.

Non sono state aggiunte librerie esterne per compiti già coperti bene da Python. Questo riduce dipendenze, tempi di installazione e problemi di compatibilità. L'unica dipendenza di sviluppo dichiarata è pytest.

## 22. Limiti accettati nell'MVP

Abbiamo lasciato fuori:

- monitoraggio continuo del log;
- un comando CLI di sblocco;
- ripristino dei blocchi dallo storico;
- deduplicazione tra `Invalid user` e `Failed password` della stessa sessione;
- supporto Linux separato per IPv6;
- rilevamento automatico del sistema operativo;
- algoritmo lineare per la finestra;
- persistenza concorrente o database.

Queste non sono funzionalità nascoste: sono estensioni successive.
