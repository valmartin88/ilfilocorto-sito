# Come lavora da solo il sito

Il sito di Filo Corto cresce con tre lavori pianificati. Ognuno parte da zero: la memoria è in questa cartella
(`scaletta.md`, `registro.md`) e nel `README.md`.

## I tre lavori

1. **Una pagina nuova** – martedì e venerdì fino al 31/01/2027, poi solo il martedì.
   Prende la prima riga `da fare` di `scaletta.md`, controlla i fatti sulle fonti, scrive la pagina, costruisce il sito,
   aggiorna scaletta e registro, pubblica. In coda fa il controllo di salute (sotto).
2. **Contatti da proporre** – ogni mercoledì. Cerca nuovi produttori e «moltiplicatori» (consorzi, GAL, biodistretti,
   mercati contadini) e prepara le righe nel foglio privato dei contatti. **Non invia niente.**
3. **Resoconto** – il primo del mese: salute del sito, pagine uscite, stato della scaletta, bandi aperti da tenere d'occhio.

## Cosa non succede mai senza Val

- Nessuna email e nessun messaggio parte da solo: i contatti si preparano, li approva Val, si inviano uno per volta.
- Nessuna pagina di un produttore esce senza scheda di adesione, check-up e testo approvato per iscritto (vedi README).
- Nessuna spesa, nessuna iscrizione, nessuna domanda a bandi.
- Elenchi di contatti e bozze di email non stanno in questo archivio, che è pubblico.

## Come si pubblica una pagina

1. Aggiungere il file nella cartella giusta di `src/` (formato: righe `chiave: valore`, una riga `---`, il corpo HTML).
   - guida: `titolo` (meno di 60 caratteri), `h1`, `desc` (120–160 caratteri), `breve`, `intro`, `data` (AAAA-MM-GG);
   - territorio: gli stessi campi più `zona`;
   - cucine: gli stessi campi della guida;
   - facoltativi per tutte: `foto` (uno dei nomi in `site/foto.php`) e `foto_alt`.
2. `python3 build.py`. Deve finire con «Controlli: collegamenti a posto, nessuna parola vietata».
   Se elenca errori, si correggono prima di pubblicare.
3. Commit su `main` e push. Il server scarica l'archivio al minuto 17 di ogni ora e copia `site/` sul sito.

## Regole dei testi

- Italiano semplice, frasi brevi. Si dice «Lazio». Nessuna data del piano.
- Nessuna vendita promessa. Il margine di Filo Corto è «sempre dichiarato», senza percentuali.
- Check-up gratuito solo «per i primi produttori». Non è una certificazione.
- Solo materie prime italiane: è una regola della rete, non una certificazione.
- Mai la parola «verificato». Nessun numero di telefono. Nessun riferimento ad altri progetti.
- Nessun nome di azienda privata nelle guide, nei territori e nelle pagine per le cucine.
- Ogni norma, numero, obbligo e ogni DOP/IGP/DOC/PAT si scrive solo dopo averlo trovato su una fonte ufficiale o affidabile
  (Regione Lazio, ARSIAL, disciplinari, Gazzetta Ufficiale, ministeri, ISTAT). Se la conferma non c'è, non si scrive.
- Le fonti usate vanno nel `registro.md`.

## Controllo di salute (a ogni giro)

- La pagina uscita nel giro precedente è online? (indirizzo nel registro)
- `https://ilfilocorto.it/` risponde e mostra le ultime uscite?
- `https://ilfilocorto.it/foto.php?stato=1`: se una foto «manca», aprire una volta `foto.php?prepara=1`.
  Se manca ancora, il sito mostra un disegno al suo posto: annotarlo nel registro, non è un'emergenza.
- Anomalie che durano due giri di fila: scriverle a Val in una riga.

## Lavori che richiedono il computer di Val (browser con accesso già fatto)

- Leggere Search Console e annotare le ricerche nel registro.
- Portare in `src/guide/` le cinque guide storiche che oggi stanno solo sul server (elenco `STORICHE` in `build.py`).
- Inviare le email approvate dalla casella di Filo Corto.
- Accorciare l'intervallo con cui il server scarica l'archivio.
