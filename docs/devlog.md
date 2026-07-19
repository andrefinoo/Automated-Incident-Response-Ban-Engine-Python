# Devlog — Diario di sviluppo

Il diario ricostruisce lo sviluppo del progetto seguendo le date, l’ordine, gli autori e i messaggi dei commit presenti nella cronologia GitHub.

---

# Settimana 1 — Struttura iniziale, modelli e parser

Durante la prima settimana abbiamo preparato la base del repository, definito i primi modelli dati, configurato i test e implementato il parser dei log SSH.

## 3 luglio 2026 — Creazione della struttura del progetto

Abbiamo iniziato creando la struttura generale del progetto e i primi file operativi. Sono state predisposte le cartelle dedicate al codice sorgente, ai test, alla documentazione e ai file di esempio.

Questa prima organizzazione ci ha permesso di separare fin dall’inizio le diverse parti del progetto e di avere una base ordinata su cui lavorare.

**Commit:**

- `Costruzione struttura progetto e creazione di file operativi` — `494be39` — andrefinoo

## 4 luglio 2026 — Sistemazione del repository e modelli dati

Abbiamo completato l’allineamento iniziale del repository e corretto la struttura dei file. Sono stati aggiornati anche il `README` e la proposta, in modo da descrivere più chiaramente l’obiettivo del progetto e la struttura prevista.

Nel commit `aggiunge modelli dati, test e documentazione iniziale` abbiamo implementato `models.py` e il relativo file di test. In `models.py` sono stati definiti i modelli usati dal programma per rappresentare i tentativi di accesso rilevati e le decisioni di ban. I test verificano la creazione degli oggetti, la validazione degli indirizzi IP e la conversione dei dati nel formato necessario per il salvataggio in JSON.

Nello stesso aggiornamento è stata aggiunta anche la prima versione della documentazione del progetto.

**Commit, in ordine cronologico:**

- `completa allineamento iniziale del repository` — `76b8688` — andrefinoo
- `sistemata struttura, aggiornato README e proposta` — `bdac3b6` — andrefinoo
- `sistema file iniziali del repository` — `a3223b9` — andrefinoo
- `aggiunge modelli dati, test e documentazione iniziale` — `7e04b52` — andrefinoo

## 6 luglio 2026 — Configurazione dei test

Abbiamo configurato `pytest` aggiungendo il file `conftest.py`. Questa modifica ha permesso di gestire correttamente gli import del codice contenuto nella cartella `src` durante l’esecuzione dei test.

Nello stesso commit è stata aggiornata anche la documentazione, mantenendo le istruzioni allineate alla struttura effettiva del progetto.

**Commit:**

- `configura pytest con conftest e aggiorna documentazione` — `2fcd772` — andrefinoo

## 8 luglio 2026 — Parser dei log SSH

Abbiamo implementato il parser dei log SSH e i relativi test.

Il parser legge le righe del file di log, riconosce gli eventi di autenticazione fallita ed estrae le informazioni utili, come timestamp, indirizzo IP e username. Le righe che non rappresentano un tentativo fallito vengono ignorate senza interrompere il programma.

I test verificano il riconoscimento delle righe supportate e il comportamento con righe non pertinenti o dati non validi.

Nello stesso aggiornamento sono stati modificati anche il devlog e la documentazione relativa all’uso dell’intelligenza artificiale.

**Commit:**

- `aggiunge parser SSH, test e aggiorna documentazione IA e devlog` — `0edc633` — andrefinoo

---

# Settimana 2 — Gerarchia dei backend firewall

Durante la seconda settimana abbiamo sviluppato la parte orientata agli oggetti del progetto, costruendo la classe base astratta e le tre implementazioni concrete del backend firewall.

## 14 luglio 2026 — Classe base del firewall

Abbiamo aggiunto `base.py`, che contiene la classe astratta `FirewallBackend`.

La classe stabilisce il contratto comune che deve essere rispettato da tutti i backend attraverso i metodi:

- `block_ip()`
- `unblock_ip()`
- `is_blocked()`

In questo modo l’engine può utilizzare un backend attraverso un’unica interfaccia, senza dipendere direttamente dalla sua implementazione.

Successivamente abbiamo aggiunto il primo test della classe base e semplificato `__init__.py`, evitando di concentrare nel file iniziale del package responsabilità che appartengono agli altri moduli.

**Commit, in ordine cronologico:**

- `Aggiunta di base.py del firewall` — `6e3c9d9` — andrefinoo
- `Aggiunto primo test relativo a base.py e ridimensionato __init__.py` — `86e04ef` — andrefinoo

## 16 luglio 2026 — Backend dry-run

Abbiamo implementato `dry_run.py`, il backend usato per simulare il comportamento del firewall.

Il dry-run permette di provare il programma senza applicare modifiche reali al sistema operativo. È utile durante lo sviluppo, nei test automatici e durante la dimostrazione del progetto, perché non richiede privilegi amministrativi.

Abbiamo inoltre aggiornato `__init__.py` e aggiunto i controlli necessari nel test del polimorfismo, verificando che il backend dry-run possa essere utilizzato tramite l’interfaccia `FirewallBackend`.

**Commit:**

- `Implementazione dry_run.py, aggiornamento __init__ e test_firewall_polymorphism` — `aa70d61` — Alessio Ordazzo

## 17 luglio 2026 — Backend Linux e Windows

Abbiamo implementato i backend destinati ai sistemi operativi reali.

Il backend Linux, contenuto in `linux.py`, gestisce il blocco degli indirizzi IP attraverso i comandi di `iptables`.

Il backend Windows, contenuto in `windows.py`, esegue le operazioni equivalenti attraverso Windows Firewall.

Entrambe le classi rispettano i metodi definiti da `FirewallBackend`. Questo consente all’engine di usare dry-run, Linux o Windows nello stesso modo, dimostrando il polimorfismo previsto dal progetto.

In entrambi gli aggiornamenti sono stati modificati anche `__init__.py` e i test sul comportamento polimorfico.

**Commit, in ordine cronologico:**

- `Implementazione linux.py, aggiornamento __init__ e test_firewall_polymorphism` — `b3a20aa` — Alessio Ordazzo
- `Implementazione windows.py, aggiornamento __init__ e test_firewall_polymorphism` — `75f54ad` — Alessio Ordazzo

---

# Settimana 3 — Engine, configurazione, persistenza e CLI

Durante la terza settimana abbiamo collegato le parti sviluppate in precedenza. Sono stati implementati il motore centrale, la configurazione JSON, la persistenza dello storico e l’interfaccia da terminale.

## 18 luglio 2026 — Engine di rilevamento

Abbiamo implementato `engine.py` e i test contenuti in `test_engine.py`.

L’engine riceve i tentativi estratti dal parser, li raggruppa per indirizzo IP e controlla quanti eventi rientrano nella finestra temporale configurata.

Prima di bloccare un indirizzo verifica:

- che sia stata raggiunta la soglia;
- che l’IP non appartenga alla whitelist;
- che l’indirizzo non risulti già bloccato;
- che i tentativi rientrino nella finestra temporale prevista.

Quando le condizioni vengono soddisfatte, l’engine crea una decisione di ban e richiama il backend attraverso l’interfaccia comune `FirewallBackend`.

I test verificano i casi principali, come il raggiungimento della soglia, gli eventi fuori dalla finestra temporale, la whitelist e gli IP già bloccati.

**Commit:**

- `Implementazione engine.py e test_engine.py` — `a826e2f` — andrefinoo

## 18 luglio 2026 — Configurazione JSON

Nella stessa giornata abbiamo implementato `config.py`, `test_config.py` e il file `config.json` di esempio.

La configurazione permette di impostare:

- numero massimo di tentativi;
- durata della finestra temporale;
- whitelist;
- backend da utilizzare;
- modalità dry-run;
- percorso del file di stato.

Sono stati aggiunti controlli per gestire valori non validi, JSON malformati e configurazioni incomplete. In assenza di alcune opzioni, il programma può utilizzare i valori predefiniti previsti.

**Commit:**

- `Implementazione config.py, test_config.py e config.json` — `7b4a50e` — andrefinoo

## 19 luglio 2026 — Persistenza dello storico

Abbiamo implementato `state.py` e `test_state.py`.

Questo modulo gestisce lo storico delle decisioni di ban attraverso un file JSON. Il programma può leggere lo storico esistente e aggiungere le nuove decisioni senza cancellare quelle già salvate.

Sono stati testati anche i casi in cui:

- il file non esiste ancora;
- il JSON non è valido;
- il contenuto non è una lista;
- non ci sono nuove decisioni da salvare;
- la cartella di destinazione deve essere creata.

**Commit:**

- `Implementazione state.py e test_state.py` — `ae0fc44` — andrefinoo

## 19 luglio 2026 — Implementazione e test della CLI

Abbiamo implementato la CLI e i test contenuti in `test_cli.py`.

La CLI rappresenta il punto di ingresso del programma e collega tutti i moduli sviluppati nelle settimane precedenti. Il flusso principale comprende:

1. lettura degli argomenti inseriti dall’utente;
2. caricamento della configurazione JSON;
3. applicazione degli eventuali valori passati da terminale;
4. scelta del backend;
5. analisi del file di log;
6. esecuzione dell’engine;
7. salvataggio delle decisioni;
8. stampa del riepilogo finale.

I test della CLI verificano il flusso principale e la gestione degli errori prevedibili.

**Commit:**

- `Implementazione cli.py e test_cli.py` — `86df838` — Alessio Ordazzo


## 19 luglio 2026 — Completamento definitivo della documentazione

Abbiamo completato e revisionato definitivamente la documentazione del progetto. Sono stati allineati il devlog, il manuale tecnico, il manuale utente, il documento sulle scelte implementative e quello sull’uso dell’intelligenza artificiale.

Durante la revisione finale abbiamo controllato che i nomi dei file, le funzionalità descritte, i comandi della CLI, la configurazione, i backend e il funzionamento dell’engine fossero coerenti con il codice effettivamente presente nel repository.

È stata inoltre sistemata la struttura dei documenti, mantenendo un linguaggio semplice e diretto e distinguendo chiaramente le istruzioni per l’utente dalle spiegazioni rivolte agli sviluppatori.

---

# Stato finale raggiunto

Al termine della terza settimana il progetto comprende:

- struttura organizzata in `src`, `tests`, `docs` ed `examples`;
- modelli dati;
- parser dei log SSH;
- classe astratta `FirewallBackend`;
- backend dry-run;
- backend Linux;
- backend Windows;
- engine con soglia, finestra temporale e whitelist;
- configurazione JSON;
- persistenza dello storico;
- CLI;
- test automatici per i moduli principali.

Il progetto ha quindi raggiunto un MVP completo: il programma può leggere un log SSH, riconoscere i tentativi falliti, valutare gli indirizzi sospetti, scegliere il backend configurato, simulare o applicare il blocco e salvare lo storico delle decisioni.
