# Sito di Filo Corto (ilfilocorto.it)

Rete di piccoli produttori per ristoranti, bar e hotel. Solo materie prime italiane. Si parte dal Lazio.

## Come è fatto

- `strumenti/pagine.py` – i testi delle pagine principali (home, produttori, cucine, check-up, come funziona, chi siamo,
  domande, prova, riga per il menu, pagina per consorzi e territori, grazie, errore, 404, crediti).
- `src/pagine/` – le pagine principali in forma di sorgente (le scrive `pagine.py`); `scheda.html` e `privacy.html` sono scritte a mano.
- `src/guide/` – guide per i produttori. `src/territori/` – le zone del Lazio. `src/cucine/` – i prodotti del Lazio per chi cucina.
- `src/produttori/` – le pagine dei produttori della rete (vedi sotto).
- `build.py` – un solo comando: riscrive le pagine principali, costruisce `site/`, la sitemap, i QR, e controlla collegamenti e parole vietate.
- `strumenti/qr.py` – genera i codici QR senza librerie esterne.
- `site/` – i file che il server copia sopra `public_html`. `site/foto.php` scarica una volta le foto libere e le serve dal sito;
  `site/invia.php` riceve i moduli.
- `docs/` – come lavora da solo il sito (`automazione.md`), cosa scrivere (`scaletta.md`), cosa è uscito (`registro.md`).

Sul server restano alcuni file che non sono in questo archivio: cinque guide storiche (elenco `STORICHE` in `build.py`),
i caratteri (`fonts/`), `.htaccess`, `robots.txt`. Usano lo stesso `style.css`: le classi vecchie vanno lasciate.

## Per pubblicare

    python3 build.py        # deve finire con «Controlli: collegamenti a posto, nessuna parola vietata»
    git add -A && git commit -m "…" && git push

Il server scarica l'archivio al minuto 17 di ogni ora e copia `site/` in `public_html` (non cancella mai file dal server).
Servono solo Python 3 e le sue librerie standard.

## Regole dei testi

Italiano semplice, «Lazio», nessuna data del piano, nessuna vendita promessa, mai la parola «verificato»,
nessun telefono, nessun riferimento ad altri progetti, norme e denominazioni controllate sulle fonti.
Il dettaglio è in `docs/automazione.md`.

## Pagine dei produttori della rete

Si pubblica la pagina di un produttore SOLO quando ci sono tutte e tre le cose:
1. scheda di adesione compilata, con la casella «Vorrei la pagina sul sito»;
2. check-up in azienda fatto;
3. testo approvato per iscritto dal produttore (anche una risposta email «va bene»): la data va nel campo `consenso`.

Come si fa: copiare `esempi/produttore-modello.html` in `src/produttori/<nome-azienda>.html`, compilarlo,
mettere le foto (JPG, larghe al massimo 1600 px) in `site/produttori/foto/`, eseguire `python3 build.py`, commit e push.
Il generatore crea la pagina, il suo QR (`site/produttori/qr/<nome>.svg`, da mettere su etichette, cassette e menu),
l'elenco «I produttori della rete» (/produttori/), la voce «La rete» nel menu, il riquadro in home e aggiorna la sitemap.
Senza la data del consenso il generatore si ferma.

Regole: solo cose dichiarate e dimostrabili dal produttore; biologico, DOP, IGP solo con il certificato;
nessuna proprietà salutistica; niente prezzi e niente telefono sulla pagina; mai «verificato»; nessuna vendita promessa.
Per togliere una pagina: cancellare il file in `src/produttori/`, ricostruire, e cancellare i file dal server.

## Foto

Le foto del sito hanno licenza libera (Unsplash) e sono elencate, con gli autori, in `crediti.html`.
Per aggiungerne una: nome e codice in `$FOTO` e la combinazione in `$IN_USO` dentro `site/foto.php`, l'autore in
`FOTO_CREDITI` dentro `strumenti/pagine.py`. Controllo: `https://ilfilocorto.it/foto.php?stato=1`.
Se una foto non si scarica, il sito mostra un disegno al suo posto. Le foto dei produttori sono dei produttori.

## Missione e regola sull'origine (decisa da Val il 27/11/2026)

Filo Corto dà visibilità ai piccoli produttori e tutela il prodotto vero delle nostre terre: nella rete entrano solo
prodotti fatti con materie prime coltivate o allevate in Italia, niente prodotti importati (né UE né extra UE).
Visione italiana, si parte dal Lazio. È una regola della rete, guardata al check-up: non presentarla come certificazione.
La vetrina dei produttori è aperta a tutti; gli ordini, per ora, sono per ristoranti, bar e hotel.
