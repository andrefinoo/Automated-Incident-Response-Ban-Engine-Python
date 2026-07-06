# Devlog

Questo documento raccoglie il diario di bordo del gruppo durante lo sviluppo del progetto
**Automated Incident Response Ban Engine**.

Lo usiamo per tenere traccia del lavoro svolto, delle decisioni prese, dei problemi incontrati
e dei passi successivi. Le entry sono scritte in modo diretto, così da poterle collegare alla
storia Git e spiegare facilmente il percorso seguito durante l'orale.

---

## Entry

### Settimana 1 — 04/07/2026

Oggi abbiamo iniziato il lavoro sul progetto **Automated Incident Response Ban Engine**.

La prima attività è stata chiarire il perimetro del progetto e l’ordine di priorità dei materiali.
Abbiamo deciso di usare le lezioni Python come riferimento principale per lo stile del codice,
così da evitare soluzioni troppo complesse o difficili da spiegare durante l’orale.

Abbiamo poi verificato i file fondamentali del progetto: la proposta, la consegna, la checklist
operativa e il riferimento al repository GitHub. Questo ci ha permesso di avere una roadmap
più chiara e di capire da dove partire senza scrivere codice in modo disordinato.

Un punto importante della giornata è stato l’allineamento sul metodo di lavoro: procederemo
per piccoli blocchi, completando un modulo alla volta. L’obiettivo è avere codice semplice,
leggibile e difendibile.

Abbiamo iniziato anche a compilare `docs/uso-ia.md`, dichiarando in modo trasparente come
stiamo usando l’IA. Per ora l’abbiamo usata soprattutto come supporto alla pianificazione,
alla lettura dei requisiti, alla preparazione della documentazione iniziale e alla revisione delle
prime scelte tecniche.

Successivamente abbiamo preparato i comandi Git per configurare correttamente gli utenti
collegati al repository. Questo passaggio è importante perché la consegna richiede una
cronologia Git chiara, con commit riconducibili ai membri del gruppo.

Dopo la parte organizzativa, abbiamo iniziato il primo blocco tecnico del progetto: i modelli
dati del dominio.

Abbiamo lavorato su `src/ban_engine/models.py`, dove abbiamo introdotto:

- `validate_ip`, funzione che usa `ipaddress` per validare e normalizzare indirizzi IPv4 e IPv6;
- `LoginAttempt`, modello che rappresenta un tentativo di login fallito estratto da un log SSH;
- `BanDecision`, modello che rappresenta la decisione di bannare un IP quando supera la soglia di tentativi falliti.

Questi modelli sono volutamente semplici: contengono solo i dati necessari e alcune
validazioni di base. La scelta è coerente con il nostro obiettivo di mantenere il codice
leggibile e spiegabile. Inoltre, i metodi `to_dict()` ci serviranno più avanti per salvare dati in
JSON senza duplicare la logica di conversione in altri moduli.

Abbiamo poi preparato `tests/test_models.py`, con i primi test automatici sui modelli dati.
I test controllano la validazione degli IP, la gestione dello username vuoto, la conversione in
dizionario e alcuni casi non validi di `BanDecision`.

Un problema pratico incontrato è stato l’avvio dei test con `PYTHONPATH=src pytest -q`.
Il comando non funzionava in modo affidabile su tutte le macchine, quindi abbiamo scelto
una soluzione più stabile e coerente con lo scaffolding del corso: aggiungere `tests/conftest.py`.

Questo file aggiunge automaticamente `src/` al percorso di import durante l’esecuzione dei test.
In questo modo possiamo lanciare i test dalla root del progetto con:

```bash
python -m pytest -q 
```

### Settimana 2 — [da compilare]

### Settimana 3 — [da compilare]

