# Scaletta delle uscite

È la memoria del lavoro automatico sui contenuti: ogni giro parte da zero e legge questo file.

**Regola.** Prendi la PRIMA riga con stato `da fare`, scrivi e pubblica quella pagina, poi cambia lo stato in `fatta AAAA-MM-GG`.
Non saltare righe e non cambiare l'ordine, salvo indicazione di Val. Quando restano meno di 6 righe `da fare`, aggiungine 6 in fondo
(vedi «Come scegliere le nuove»), mantenendo l'alternanza dei tipi.

Tipi di pagina:
- **guida** → `src/guide/<slug>.html` – per i piccoli produttori che vogliono vendere alla ristorazione;
- **territorio** → `src/territori/<slug>.html` – una zona del Lazio: cosa si produce, cosa cerca la ristorazione;
- **cucine** → `src/cucine/<slug>.html` – un prodotto del Lazio visto da chi cucina: denominazioni, stagione, formati, cosa chiedere.

I titoli sono di lavoro. Denominazioni, norme e numeri si scrivono solo dopo averli controllati sulle fonti (vedi `automazione.md`).

| n | tipo | slug | titolo di lavoro | chi la cerca | stato |
|---|------|------|------------------|--------------|-------|
| 1 | guida | vendere-formaggi-ai-ristoranti | Vendere formaggi a ristoranti e hotel | caseifici e allevatori: «vendere formaggi ai ristoranti», «fornitore formaggi ristoranti» | da fare |
| 2 | territorio | produttori-sabina | Produttori della Sabina (Rieti e Roma nord) | produttori della zona; chef che cercano «prodotti della Sabina» | da fare |
| 3 | guida | etichetta-prodotti-alimentari-piccoli-produttori | L'etichetta dei prodotti alimentari per i piccoli produttori | «etichetta prodotti alimentari cosa scrivere», «etichetta allergeni» | da fare |
| 4 | cucine | formaggi-del-lazio | Formaggi del Lazio per la ristorazione | chef e F&B: «formaggi del Lazio», «pecorino per ristoranti» | da fare |
| 5 | guida | lotto-e-rintracciabilita | Lotto e rintracciabilità, spiegati semplice | «numero di lotto obbligatorio», «rintracciabilità alimenti piccoli produttori» | da fare |
| 6 | territorio | produttori-castelli-romani | Produttori dei Castelli Romani | produttori della zona; «prodotti tipici Castelli Romani» | da fare |
| 7 | guida | vendere-vino-e-birra-ai-ristoranti | Vendere vino e birra artigianale ai ristoranti | cantine e birrifici: «vendere vino ai ristoranti», «birra artigianale ristoranti» | da fare |
| 8 | cucine | legumi-del-lazio | Legumi del Lazio per la ristorazione | «legumi del Lazio», «lenticchie per ristoranti» | da fare |
| 9 | guida | campionatura-come-presentarsi-a-uno-chef | Il campione: come presentarsi a uno chef | «come proporre un prodotto a un ristorante» | da fare |
| 10 | territorio | produttori-ciociaria | Produttori della Ciociaria (Frosinone) | produttori della zona; «prodotti tipici Ciociaria» | da fare |
| 11 | guida | trasporto-alimenti-piccoli-produttori | Trasporto degli alimenti per i piccoli produttori | «trasporto alimenti furgone requisiti», «consegnare ai ristoranti» | da fare |
| 12 | cucine | nocciole-e-castagne-del-lazio | Nocciole e castagne del Lazio per la ristorazione | pasticceri e chef: «nocciola romana», «castagne del Lazio» | da fare |
| 13 | guida | prezzo-per-la-ristorazione | Il prezzo per la ristorazione: come calcolarlo | «prezzo ingrosso ristoranti come calcolare» | da fare |
| 14 | territorio | produttori-agro-pontino | Produttori dell'Agro Pontino e della provincia di Latina | produttori della zona; «prodotti tipici Latina» | da fare |
| 15 | guida | vendere-conserve-e-sottoli-ai-ristoranti | Vendere conserve e sottoli alla ristorazione | «vendere conserve ai ristoranti», «laboratorio conserve requisiti» | da fare |
| 16 | cucine | ortaggi-del-lazio | Carciofo romanesco e ortaggi del Lazio per la ristorazione | «carciofo romanesco IGP», «verdure di stagione Lazio» | da fare |
| 17 | guida | fornire-gli-hotel-colazioni-e-buffet | Fornire gli hotel: colazioni e buffet | «fornitore hotel colazioni», «prodotti locali colazione hotel» | da fare |
| 18 | territorio | produttori-valle-aniene | Produttori della Valle dell'Aniene e dei Monti Simbruini | produttori della zona | da fare |
| 19 | guida | vendere-legumi-e-cereali-ai-ristoranti | Vendere legumi e cereali ai ristoranti | «vendere legumi ai ristoranti» | da fare |
| 20 | cucine | miele-del-lazio | Miele del Lazio per la ristorazione | «miele per hotel colazioni», «miele del Lazio» | da fare |
| 21 | guida | vendere-pasta-e-farine-artigianali | Vendere pasta e farine artigianali alla ristorazione | pastifici e mulini: «farine per ristoranti», «pasta artigianale ristoranti» | da fare |
| 22 | territorio | produttori-reatino | Produttori del Reatino e della montagna | produttori della zona | da fare |
| 23 | guida | stagionalita-e-continuita-di-fornitura | Stagionalità e continuità di fornitura | «fornitura stagionale ristoranti» | da fare |
| 24 | cucine | vini-del-lazio | I vini del Lazio per la carta dei vini | sommelier e ristoratori: «vini del Lazio DOC» | da fare |
| 25 | territorio | produttori-litorale-romano | Produttori del Litorale e della Campagna romana | produttori della zona | da fare |
| 26 | guida | qr-su-etichetta-e-menu | Il QR su etichetta e menu: a cosa serve | «QR code etichetta alimentare», «QR menu produttore» | da fare |

## Già pubblicate

- guide: vendere-olio-ai-ristoranti, vendere-miele-a-ristoranti-e-hotel, haccp-piccoli-produttori (26/11/2026), più le cinque guide storiche elencate in `build.py`;
- territori: produttori-tuscia (27/11/2026);
- cucine: olio-extravergine-del-lazio (28/11/2026).

## Come scegliere le nuove

1. Parti da cosa cerca la gente: le ricerche annotate nel `registro.md` dopo il resoconto mensile (Search Console) e una ricerca sul web delle domande più frequenti di produttori e chef.
2. Una pagina, una ricerca principale. Niente doppioni: controlla le cartelle `src/` e l'elenco `STORICHE` in `build.py`.
3. Preferisci gli argomenti dove possiamo dire qualcosa di utile e controllabile: prodotti che viaggiano bene, obblighi veri, zone del Lazio.
4. Scrivi la riga con: tipo, slug, titolo di lavoro, chi la cerca.

## Zone per i contatti

Il lavoro di preparazione dei contatti segue le pagine di territorio: Tuscia (in corso), poi Sabina, Castelli Romani, Ciociaria,
Agro Pontino, Valle dell'Aniene, Reatino, Litorale. Si passa alla zona successiva quando la sua pagina è online.
