# Sito di Filo Corto (ilfilocorto.it)

- `src/guide/` – una guida per file: intestazione `chiave: valore`, riga `---`, corpo HTML.
- `src/pagine/` – pagine singole (scheda di adesione, privacy).
- `build.py` – genera `site/`: guide, indice delle guide, sitemap.
- `site/` – i file che il server copia sopra `public_html` (le altre pagine restano sul server).

Per pubblicare una guida: aggiungere il file in `src/guide/`, eseguire `python3 build.py`, fare commit e push.
Il server scarica il repository ogni ora e copia `site/` in `public_html`.

Regole dei testi: italiano semplice, «Lazio», nessuna data del piano, nessuna vendita promessa,
mai la parola «verificato», nessun riferimento ad altri progetti, norme controllate sulle fonti.
