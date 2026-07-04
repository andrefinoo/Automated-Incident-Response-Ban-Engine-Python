# Devlog

## 04/07/2026 — Allineamento iniziale e primi modelli dati

Oggi abbiamo iniziato il lavoro sul progetto **Automated Incident Response Ban Engine**.

La prima attività è stata chiarire il perimetro del progetto e l’ordine di priorità dei materiali. Abbiamo deciso di usare le lezioni Python come riferimento principale per lo stile del codice.

Abbiamo poi verificato i file fondamentali del progetto: la proposta, la consegna, la checklist operativa e il riferimento al repository GitHub. Questo ci ha permesso di avere una roadmap più chiara e di capire da dove partire senza andare subito a scrivere codice in modo disordinato.

Un punto importante della giornata è stato l’allineamento sul metodo di lavoro: procederemo per piccoli blocchi, completando un modulo alla volta. 

Abbiamo iniziato anche a compilare `docs/uso-ia.md`, dichiarando in modo trasparente come stiamo usando l’IA. Per ora l’abbiamo usata soprattutto come supporto alla pianificazione, alla lettura dei requisiti, alla preparazione della documentazione iniziale e alla revisione delle prime scelte tecniche.

Successivamente abbiamo preparato i comandi Git per configurare correttamente gli utenti collegati al repository. 

Dopo la parte organizzativa, abbiamo iniziato il primo blocco tecnico del progetto: i modelli dati del dominio.

Abbiamo lavorato sul file `src/ban_engine/models.py`, dove abbiamo previsto:

- la funzione `validate_ip`, che usa `ipaddress` per validare e normalizzare indirizzi IPv4 e IPv6;
- la classe `LoginAttempt`, che rappresenta un tentativo di login fallito estratto da un log SSH;
- la classe `BanDecision`, che rappresenta la decisione di bannare un IP quando supera la soglia di tentativi falliti.

Questi modelli sono volutamente semplici: contengono solo i dati necessari e alcune validazioni di base. Inoltre, i metodi `to_dict()` ci serviranno più avanti per salvare informazioni in JSON, senza dover duplicare la logica di conversione in altri moduli.

Abbiamo poi preparato il file `tests/test_models.py`, con i primi test automatici sui modelli dati. I test controllano che:

- un IPv4 valido venga accettato;
- un IPv6 valido venga accettato;
- un IP non valido generi errore;
- uno username vuoto venga convertito in `None`;
- `LoginAttempt.to_dict()` produca dati compatibili con JSON;
- `BanDecision` rifiuti un numero di tentativi non valido.

Questa parte ci aiuta a partire con una base più solida, perché prima di costruire parser, engine e persistenza vogliamo essere sicuri che gli oggetti principali funzionino correttamente.

Prima del commit abbiamo aggiunto pytest.ini ed eseguito i test con:

```bash
python -m pytest -q