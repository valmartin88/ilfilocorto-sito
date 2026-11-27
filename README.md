# Sito di Filo Corto (ilfilocorto.it)

- `src/guide/` – una guida per file: intestazione `chiave: valore`, riga `---`, corpo HTML.
- `src/pagine/` – pagine singole (scheda di adesione, privacy).
- `build.py` – genera `site/`: guide, indice delle guide, sitemap.
- `site/` – i file che il server copia sopra `public_html` (le altre pagine restano sul server).

Per pubblicare una guida: aggiungere il file in `src/guide/`, eseguire `python3 build.py`, fare commit e push.
Il server scarica il repository ogni ora e copia `site/` in `public_html`.

Regole dei testi: italiano semplice, «Lazio», nessuna data del piano, nessuna vendita promessa,
mai la parola «verificato», nessun riferimento ad altri progetti, norme controllate sulle fonti.

## Pagine dei produttori della rete

Si pubblica la pagina di un produttore SOLO quando ci sono tutte e tre le cose:
1. scheda di adesione compilata, con la casella «Vorrei la pagina sul sito»;
2. check-up in azienda fatto;
3. testo approvato per iscritto dal produttore (anche una risposta email «va bene»): la data va nel campo `consenso`.

Come si fa: copiare `esempi/produttore-modello.html` in `src/produttori/<nome-azienda>.html`, compilarlo,
mettere le foto (JPG, larghe al massimo 1600 px) in `site/produttori/foto/`, eseguire `python3 build.py`, commit e push.
Il generatore crea la pagina, l'elenco «I produttori della rete» (/produttori/) e aggiorna la sitemap.
Senza la data del consenso il generatore si ferma.

Regole: solo cose dichiarate e dimostrabili dal produttore; biologico, DOP, IGP solo con il certificato;
nessuna proprietà salutistica; niente prezzi e niente telefono sulla pagina; mai «verificato»; nessuna vendita promessa.
Quando esce il primo produttore, aggiungere il link «I produttori» nel menu e in home (pagine sul server).
Per togliere una pagina: cancellare il file in `src/produttori/`, ricostruire, e cancellare il file dal server.

## Pagine di territorio

`src/territori/<slug>.html`, stesso formato delle guide (titolo, h1, desc, breve, intro, zona, data, `---`, corpo).
Il generatore crea la pagina, l'indice /territori/ e la sitemap. Una zona per pagina:
Tuscia (fatta), Sabina, Castelli Romani, Ciociaria, Agro Pontino, poi Valle dell'Aniene, Reatino, Litorale.
Solo DOP, IGP, DOC e PAT controllati sulle fonti (ARSIAL, Regione Lazio, disciplinari). Nessun nome di azienda.
