# Uso dell'intelligenza artificiale

## 1. Premessa

Durante il progetto abbiamo usato strumenti di intelligenza artificiale come assistenti. L'IA non è integrata nel programma e non prende decisioni durante l'analisi dei log: il Ban Engine usa soltanto regole, regex, configurazione e codice Python deterministico.

Gli strumenti utilizzati sono stati:

- **Gemini**, soprattutto nella fase iniziale di proposta e brainstorming;
- **ChatGPT**, per analisi dei requisiti, confronto tra soluzioni, debugging, test e revisione della documentazione.

PyCharm, Git e pytest sono stati gli strumenti con cui abbiamo verificato il lavoro, ma non sono strumenti di IA.

Le proposte dell'IA non sono state considerate corrette automaticamente. Il criterio seguito è stato:

1. leggere il suggerimento;
2. confrontarlo con consegna, appunti e codice esistente;
3. adattarlo alla struttura reale;
4. eseguire test o prove controllate;
5. mantenere solo ciò che sappiamo realmente.

## 2. Analisi della consegna e pianificazione

### Cosa abbiamo chiesto

- riassumere i requisiti del progetto;
- distinguere requisiti obbligatori e miglioramenti;
- trasformare la consegna in una checklist;
- verificare che l'idea fosse abbastanza concreta;
- proporre un ordine di sviluppo.

### Suggerimenti ricevuti

L'IA ha suggerito di separare:

- modelli;
- parser;
- motore decisionale;
- backend firewall;
- configurazione;
- persistenza;
- CLI;
- test e documentazione.

Ha inoltre suggerito di completare ogni modulo insieme ai relativi test, invece di scrivere tutto il programma e testarlo soltanto alla fine.

### Cosa abbiamo accettato

Abbiamo accettato la divisione per responsabilità e l'ordine generale: struttura, modelli, parser, backend, engine, configurazione, stato e documentazione.

### Cosa abbiamo modificato o rifiutato

Abbiamo evitato architetture troppo grandi, pattern non richiesti e dipendenze esterne. La checklist è stata usata come guida, non come sostituto delle decisioni del gruppo.

### Verifica

La pianificazione è stata confrontata con la consegna, la proposta approvata, la struttura del repository e la cronologia Git.

## 3. Progettazione della gerarchia firewall

### Cosa abbiamo chiesto

- come soddisfare il requisito di ereditarietà in modo significativo;
- quali metodi inserire nella classe base;
- come separare il sistema operativo dal motore;
- come includere una modalità sicura per test e demo.

### Suggerimenti ricevuti

Sono stati proposti:

- `FirewallBackend` come classe astratta;
- `block_ip()`, `unblock_ip()` e `is_blocked()` come contratto;
- backend Linux, Windows e dry-run;
- composizione tra engine e backend;
- test polimorfici.

### Cosa abbiamo accettato

Abbiamo adottato la gerarchia perché ogni implementazione concreta è realmente un backend firewall. Abbiamo mantenuto il dry-run come sottoclasse autonoma.

### Cosa abbiamo modificato o rifiutato

Abbiamo scartato una catena di condizioni sul sistema operativo dentro l'engine e funzioni separate per ogni piattaforma. Abbiamo mantenuto soltanto i metodi necessari al progetto.

### Verifica

La classe base non può essere istanziata; tutte le sottoclassi implementano il contratto; un test usa oggetti differenti attraverso il tipo comune `FirewallBackend`.

## 4. Modelli e validazione degli IP

### Cosa abbiamo chiesto

- quali campi servissero in `LoginAttempt` e `BanDecision`;
- se usare classi normali, dizionari o dataclass;
- come validare IPv4 e IPv6;
- come preparare i dati per JSON.

### Suggerimenti ricevuti

L'IA ha proposto dataclass, `ipaddress.ip_address()` e metodi `to_dict()`.

### Cosa abbiamo accettato

Abbiamo usato dataclass e il modulo standard `ipaddress`. La validazione è centralizzata in `validate_ip()`.

### Cosa abbiamo modificato o rifiutato

Abbiamo mantenuto pochi campi e poche regole, evitando modelli troppo ricchi o librerie di validazione esterne. La regex viene usata per estrarre l'indirizzo dal log, non per dichiararlo valido.

### Verifica

I test coprono IPv4, IPv6, valori errati, username vuota, conteggi non validi e serializzazione.

## 5. Parser dei log SSH

### Cosa abbiamo chiesto

- come riconoscere `Failed password`, `Failed publickey` e `Invalid user`;
- come estrarre timestamp, username e IP;
- come gestire righe non pertinenti;
- quali casi limite aggiungere ai test.

### Suggerimenti ricevuti

L'IA ha mostrato possibili regex e ha consigliato pattern separati invece di una sola espressione molto lunga. Ha proposto di restituire `None` per le righe ignorate.

### Cosa abbiamo accettato

Abbiamo mantenuto pattern distinti, lettura riga per riga e costruzione di `LoginAttempt`.

### Cosa abbiamo modificato o rifiutato

Le regex sono state ridotte ai formati necessari per l'MVP. Non abbiamo accettato un parser universale né pattern non accompagnati da test. Per i timestamp privi di anno è stata adottata una regola semplice e documentata.

### Verifica

Sono state provate righe valide, righe accettate da SSH ma non sospette, IP non validi e file misti.

## 6. Problemi di import e configurazione di pytest

### Problema sottoposto all'IA

Durante i test comparivano errori di import legati alla struttura `src/` e a percorsi che dipendevano dal nome della cartella locale.

### Alternative suggerite

- impostare `PYTHONPATH=src`;
- installare il package con `pip install -e .`;
- inserire `src/` nel percorso dei test tramite `conftest.py`.

### Soluzione adottata

Abbiamo usato `tests/conftest.py` durante lo sviluppo e aggiunto l'installazione editable nei requisiti.

### Cosa abbiamo rifiutato

Import come `RepoPython.src...`, perché non rappresentavano il package e cambiavano da una macchina all'altra.

### Verifica

La suite è stata eseguita dalla root con `python -m pytest -q`.

## 7. Backend Linux e Windows

### Cosa abbiamo chiesto

- come costruire comandi `iptables` e `netsh`;
- se usare stringhe o liste con `subprocess`;
- quando usare `check=True`;
- come testare senza privilegi amministrativi.

### Suggerimenti ricevuti

L'IA ha consigliato:

- liste di argomenti;
- niente `shell=True`;
- `check=True` per aggiunta e rimozione;
- `check=False` per il controllo di esistenza;
- mock di `subprocess.run()`.

### Cosa abbiamo accettato

Queste indicazioni sono state integrate nei backend. Per Windows è stato usato un nome di regola deterministico con prefisso `BanEngine`.

### Cosa abbiamo modificato o rifiutato

I comandi sono stati adattati ai nomi e alla struttura effettiva del progetto. Non abbiamo eseguito comandi firewall reali nei test.

### Verifica

I test controllano la lista completa degli argomenti, i codici di ritorno simulati e l'output del comando Windows.

## 8. Debugging del test polimorfico

### Problema sottoposto all'IA

Il test polimorfico non registrava le chiamate ai mock come previsto quando Linux e Windows venivano patchati contemporaneamente a livello di `subprocess.run()`.

### Analisi ricevuta

I due moduli fanno riferimento allo stesso oggetto `subprocess`. Patch sovrapposte sullo stesso attributo potevano interferire e rendere poco chiaro quale mock ricevesse la chiamata.

### Soluzione adottata

Abbiamo separato gli obiettivi:

- i test dei backend verificano i comandi `subprocess`;
- il test del polimorfismo verifica la chiamata allo stesso metodo su oggetti concreti diversi;
- per Linux e Windows usa `patch.object()` sul metodo dell'istanza;
- il dry-run mantiene il comportamento reale.

### Cosa abbiamo rifiutato

Non abbiamo eliminato il test e non abbiamo ridotto le asserzioni dei test specifici solo per ottenere un risultato verde.

### Verifica

Dopo la modifica, ogni backend viene chiamato una volta e il dry-run registra l'IP nel proprio set.

## 9. IncidentResponseEngine

### Cosa abbiamo chiesto

- come raggruppare gli eventi per IP;
- come applicare soglia e finestra temporale;
- dove controllare la whitelist;
- come evitare blocchi duplicati;
- quali test fossero indispensabili.

### Suggerimenti ricevuti

Sono state discusse una soluzione semplice con cicli annidati e una finestra scorrevole più efficiente.

### Cosa abbiamo accettato

Abbiamo scelto l'algoritmo più leggibile per l'MVP. Il backend viene interrogato con `is_blocked()` prima della chiamata a `block_ip()`.

### Cosa abbiamo modificato o rifiutato

Non abbiamo introdotto strutture incrementali, concorrenza o ottimizzazioni premature. La logica è stata adattata ai modelli e ai test già presenti.

### Verifica

I test coprono soglia raggiunta, sotto soglia, eventi fuori finestra, whitelist e secondo tentativo di blocco dello stesso IP.

## 10. Configurazione JSON

### Cosa abbiamo chiesto

- come unire valori predefiniti, file JSON e opzioni CLI;
- quali validazioni eseguire;
- come segnalare file mancanti e JSON malformato;
- come gestire la whitelist.

### Suggerimenti ricevuti

L'IA ha proposto una dataclass `AppConfig`, una funzione di caricamento unica e validazioni esplicite campo per campo.

### Cosa abbiamo accettato

Abbiamo adottato valori predefiniti e la precedenza CLI sui valori caricati. Gli IP della whitelist vengono normalizzati con la stessa funzione dei modelli.

### Cosa abbiamo modificato o rifiutato

Non abbiamo usato librerie esterne di schema validation. Il numero dei backend ammessi è limitato alle implementazioni presenti.

### Verifica

I test coprono default, configurazione personalizzata, file mancante, JSON errato e whitelist non valida.

## 11. Persistenza dello storico

### Cosa abbiamo chiesto

- come aggiungere decisioni senza cancellare lo storico;
- come mantenere un JSON valido;
- come gestire file e cartelle non esistenti;
- quali errori non ignorare.

### Suggerimenti ricevuti

È stato suggerito di caricare la lista esistente, estenderla e riscrivere il documento completo. È stata anche proposta la creazione automatica delle cartelle padre.

### Cosa abbiamo accettato

La soluzione mantiene un unico array JSON leggibile e non sovrascrive semanticamente gli elementi precedenti.

### Cosa abbiamo modificato o rifiutato

Non abbiamo adottato un database, locking o scrittura concorrente perché fuori dallo scopo dell'MVP. Non abbiamo usato append testuale, che produrrebbe JSON non valido.

### Verifica

I test coprono file assente, prima scrittura, seconda scrittura e file corrotto.

## 12. CLI e flusso completo

### Cosa abbiamo chiesto

- come organizzare gli argomenti con `argparse`;
- come restituire exit code coerenti;
- come stampare un report breve;
- come rendere il dry-run la scelta più sicura.

### Suggerimenti ricevuti

Sono stati proposti un entry point tramite `__main__.py`, override per soglia e finestra, gestione degli errori attesi e un riepilogo finale.

### Cosa abbiamo accettato

La CLI coordina i moduli ma non contiene la loro logica interna. `--dry-run` può attivare la simulazione e non disattivarla.

### Cosa abbiamo modificato o rifiutato

Non è stato aggiunto il rilevamento automatico del sistema operativo. Il backend viene scelto dal file JSON, scelta più semplice e prevedibile per la demo.

### Verifica

Il test CLI esegue un flusso dry-run completo con un file temporaneo e verifica la creazione dello storico. Un secondo test controlla l'errore per log mancante.

## 13. Suggerimenti rifiutati o ridotti durante il progetto

Nel complesso abbiamo evitato:

- framework o librerie non necessarie;
- un database per un semplice storico JSON;
- rilevamento e modifica automatica del firewall durante i test;
- `shell=True` nei comandi;
- regex uniche troppo complesse;
- ereditarietà tra classi che non hanno una relazione “è un”;
- condizioni sul sistema operativo dentro l'engine;
- ottimizzazioni premature dell'algoritmo temporale;
- test che richiedessero amministratore;

## 14. Impatto dell'interazione umano-IA

L'IA ha accelerato il confronto tra alternative e ha aiutato a individuare casi limite prima di arrivare alla prova manuale. Il contributo più utile non è stato produrre molte righe di codice, ma rendere espliciti problemi che altrimenti sarebbero rimasti impliciti:

- separazione tra decisione e mitigazione;
- differenza tra ereditarietà e composizione;
- import indipendenti dalla cartella locale;
- test dei comandi senza esecuzione reale;
- rischio di sovrascrivere lo storico;
- differenza tra stato persistente e stato del firewall;
- precedenza tra configurazione e CLI.

Le decisioni finali, i commit, l'esecuzione dei test e l'eventuale uso dei backend reali restano responsabilità del gruppo.

## 16. Dichiarazione finale

Dichiariamo di aver usato Gemini e ChatGPT come strumenti di supporto per progettazione, chiarimenti, debugging, generazione di casi di test, revisione e organizzazione della documentazione. I suggerimenti sono stati selezionati e adattati; le parti non coerenti con requisiti, coerenza del progetto o codice reale sono state scartate.

L’IA è stata utilizzata anche come supporto per il layout, la formattazione e l’organizzazione della documentazione. I contenuti, le decisioni tecniche e le informazioni descritte sono stati forniti dal gruppo; l’IA si è limitata a sistemarli e renderli più chiari e ordinati.
