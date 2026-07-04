## Aggiornamento sessione — 04/07/2026

### Attività svolte con il supporto dell'IA

Durante questa sessione abbiamo usato ChatGPT come supporto operativo per avviare il progetto in modo ordinato.

In particolare, abbiamo chiesto supporto per:

- verificare la presenza dei file di progetto e del riferimento al repository GitHub;
- confermare la gerarchia dei materiali da seguire;
- iniziare la compilazione del file `docs/uso-ia.md`;
- preparare una prima bozza del `docs/devlog.md`;
- preparare i comandi Git per configurare correttamente gli utenti locali collegati al repository;
- individuare il primo blocco tecnico da sviluppare, cioè i modelli dati `LoginAttempt` e `BanDecision`.

### Come abbiamo usato l'IA

L'IA è stata usata come tutor e supporto alla pianificazione, non come risolutore automatico del progetto.

Le risposte ricevute sono state usate per chiarire il flusso di lavoro e per trasformare i requisiti della consegna in attività più concrete. In questa fase l'obiettivo non era produrre subito tutto il codice, ma capire come procedere senza creare una struttura troppo complessa.

Abbiamo usato l'IA anche per ottenere bozze iniziali di documentazione. Queste bozze non vengono considerate definitive: devono ancora essere riviste, adattate e approvate dal gruppo prima di essere inserite nel repository.

### Cosa abbiamo accettato

Abbiamo accettato:

- l'idea di procedere per fasi, partendo dalla struttura del progetto e poi dai modelli dati;
- l'impostazione del file `docs/uso-ia.md` con sezioni dedicate a richieste, output, parti accettate, parti modificate e parti rifiutate;
- una bozza di devlog, da rivedere prima del commit;
- i comandi Git per configurare `user.name` e `user.email` sui computer dei membri del gruppo;
- il suggerimento di iniziare dai modelli dati perché sono una base comune per parser, engine, persistenza e test.

### Cosa abbiamo modificato

Abbiamo considerato le risposte dell'IA come materiale di partenza.

Dovremmo modificare:

- il testo della documentazione;
- le descrizioni del devlog, per fare in modo che raccontino quello che abbiamo fatto;
- eventuali nomi, esempi o dettagli tecnici non perfettamente coerenti con il repository;
- il codice proposto, se durante l'implementazione risulta troppo complesso o non allineato al livello delle lezioni.

### Cosa abbiamo rifiutato o non applicato

Non abbiamo accettato:

- la generazione completa dell'intero progetto in un'unica soluzione;
- l'idea di scrivere codice avanzato non ancora spiegabile dal gruppo;
- l'uso dell'IA per sostituire la nostra comprensione del progetto;
- l'inserimento automatico di documentazione non riletta;

### Codice generato o suggerito

In questa sessione l'IA ha suggerito una possibile implementazione iniziale per:

- `src/ban_engine/models.py`;
- `tests/test_models.py`.

Questa parte non è ancora considerata automaticamente definitiva. Prima di inserirla nel progetto, bisognerà leggerla, capirla, provarla con `pytest` e modificarla dove necessario.

### Impatto reale sul progetto

L'impatto principale dell'IA oggi è stato organizzativo e documentale.

Abbiamo chiarito:

- quali file seguire;
- come documentare l'uso dell'IA;
- come scrivere un devlog coerente;
- come configurare gli utenti Git;
- quale modulo sviluppare per primo.

Non sono ancora state completate funzionalità operative del motore di ban. Il progetto è ancora nella fase iniziale di setup, documentazione e pianificazione tecnica.

### Verifica da parte del gruppo

Prima del commit, il gruppo controllerà che:

- il testo inserito in `docs/uso-ia.md` rappresenti davvero l'uso fatto dell'IA;
- scrittura del devlog con le attività effettivamente svolte;
- eventuale codice suggerito sia compreso e testato;
