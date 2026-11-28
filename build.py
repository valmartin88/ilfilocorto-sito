#!/usr/bin/env python3
"""Filo Corto – genera il sito.

Uso: python3 build.py
Prima riscrive le pagine principali (strumenti/pagine.py -> src/pagine/), poi costruisce site/:
- src/pagine/<nome>.html      -> site/<nome>.html
- src/guide/<slug>.html       -> site/guide/<slug>.html          guide per i produttori
- src/territori/<slug>.html   -> site/territori/<slug>.html      le zone del Lazio
- src/cucine/<slug>.html      -> site/per-le-cucine/<slug>.html  i prodotti del Lazio, per chi cucina
- src/produttori/<slug>.html  -> site/produttori/<slug>.html     i produttori della rete, ognuno con il suo QR
  Si pubblica un produttore SOLO dopo scheda di adesione, check-up e consenso scritto (vedi README).
Ogni file in src/ comincia con righe "chiave: valore", poi una riga "---", poi il corpo HTML.
Alla fine controlla collegamenti e parole vietate: se trova un errore si ferma (e non si pubblica).
La cartella site/ viene copiata sopra public_html dal server (vedi README). Servono solo le librerie standard di Python.
"""
import json, pathlib, datetime, re, runpy, sys

RADICE = pathlib.Path(__file__).parent
sys.path.insert(0, str(RADICE / 'strumenti'))
import qr  # noqa: E402

URL = 'https://ilfilocorto.it/'
CSS_V = '11'
MESI = ['gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno', 'luglio', 'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre']
AUTORE = {'@type': 'Person', 'name': 'Valerio Semeraro', 'jobTitle': 'Food Specialist e consulente HACCP'}
EDITORE = {'@type': 'Organization', 'name': 'Filo Corto', 'logo': {'@type': 'ImageObject', 'url': URL + 'icona.png'}}

# Guide pubblicate prima di questo sistema: i file restano sul server, qui servono per indice e sitemap.
STORICHE = [
    ('vendere-ai-ristoranti', 'Come vendere ai ristoranti: la guida per piccoli produttori', 'I passi concreti: prodotti, listino, documenti, campione, consegne, pagamenti.'),
    ('documenti-per-vendere-ai-ristoranti', 'Documenti e requisiti per vendere a ristoranti e hotel', 'Registrazione, autocontrollo, lotti, etichette, imballaggi, trasporto.'),
    ('cosa-chiede-uno-chef', 'Cosa chiede uno chef a un fornitore', 'Le tre domande di ogni cucina, viste da dentro.'),
    ('listino-per-ristoranti', 'Come preparare un listino per ristoranti', 'Cosa scriverci, in quale forma, con un esempio.'),
    ('filiera-corta-km-0', 'Filiera corta e chilometro zero: cosa dice la legge', 'Le definizioni della legge 61/2022, in parole semplici.'),
]
# File che stanno solo sul server (non nel repository): il controllo dei collegamenti li considera presenti.
SOLO_SERVER = {'guide/' + s + '.html' for s, _, _ in STORICHE} | {'fonts/archivo.woff2', 'fonts/manrope.woff2'}
PAGINE_FISSE = ['', 'produttori.html', 'cucine.html', 'come-funziona.html', 'check-up.html', 'prova.html', 'riga-menu.html', 'guide/', 'domande.html', 'chi-siamo.html', 'filo-doro.html', 'enti.html', 'privacy.html']

LOGO = '<svg width="46" height="46" viewBox="0 0 60 60" fill="none" aria-hidden="true"><circle cx="30" cy="38" r="16.85" fill="#F2F4F0" stroke="#E8692C" stroke-width="6.3"/><circle cx="30" cy="38" r="5.85" fill="#12302B"/><path d="M30 21 C 30 11, 37 5, 48 5 C 48 15, 41 21, 30 21 Z" fill="#2f5d3a"/></svg>'
ORG = {'@context': 'https://schema.org', '@type': 'Organization', 'name': 'Filo Corto', 'url': URL, 'logo': URL + 'icona.png', 'email': 'info@ilfilocorto.it', 'areaServed': 'Lazio',
       'slogan': 'Dal produttore alla cucina',
       'description': 'Filo Corto dà visibilità ai piccoli produttori e porta il prodotto vero delle nostre terre in ristoranti, bar e hotel. Solo materie prime italiane. Rete in costruzione: si parte dal Lazio.',
       'founder': {'@type': 'Person', 'name': 'Valerio Semeraro'}}
# Comparsa allo scorrimento e menu a scomparsa sui telefoni.
SCRIPT = ('<script>(function(){var t=document.querySelector(".t2"),b=t&&t.querySelector(".apri");if(b){var chiudi=function(){t.classList.remove("aperto");b.setAttribute("aria-expanded","false")};'
          'b.addEventListener("click",function(){b.setAttribute("aria-expanded",t.classList.toggle("aperto")?"true":"false")});'
          't.querySelectorAll(".menu a").forEach(function(a){a.addEventListener("click",chiudi)});document.addEventListener("keydown",function(e){if(e.key==="Escape")chiudi()})}'
          'if(!("IntersectionObserver"in window)||matchMedia("(prefers-reduced-motion: reduce)").matches)return;'
          'var el=document.querySelectorAll(".porta2,.tessera,ol.passi li,.fili>div,.elenco-guide a,.modulo,.riquadro,.manifesto p,.tappe,.gettoni,.testa,.pilastri>div,.carta-s,.passi-h>div,.cat,.foto,.diverso,.passaporto,.carta-menu");'
          'var o=new IntersectionObserver(function(v){v.forEach(function(e){if(e.isIntersecting){e.target.classList.add("in");o.unobserve(e.target)}})},{rootMargin:"0px 0px -8% 0px"});'
          'el.forEach(function(x){if(x.getBoundingClientRect().top>innerHeight){x.classList.add("rv");o.observe(x)}})})();</script>')
MENU = [('produttori.html', 'Produttori'), ('cucine.html', 'Per chi compra'), ('come-funziona.html', 'Come funziona'), ('check-up.html', 'Check-up'), ('guide/', 'Guide'), ('chi-siamo.html', 'Chi siamo')]
STATO = {'rete': False, 'cucine': False}   # cosa esiste già: decide alcune voci di menu e piede


def leggi(percorso):
    testo = percorso.read_text(encoding='utf-8')
    testa, corpo = testo.split('\n---\n', 1)
    dati = {}
    for riga in testa.splitlines():
        if ':' in riga:
            k, v = riga.split(':', 1)
            dati[k.strip()] = v.strip()
    dati['corpo'] = corpo.strip()
    dati['slug'] = percorso.stem
    return dati


def carica(cartella, chiave):
    c = RADICE / 'src' / cartella
    return sorted((leggi(p) for p in c.glob('*.html')), key=chiave) if c.exists() else []


def mese(data):
    return MESI[int(data[5:7]) - 1] + ' ' + data[:4]


def cta(r):
    return ('<section class="sez verde-b"><div class="wrap fascia"><h2>Produci in Italia? Partiamo dal Lazio.</h2>'
            f'<a class="btn miele" href="{r}produttori.html#candidati">Candidati in 2 minuti →</a></div></section>')


def cta_cucine(r):
    return ('<section class="sez miele-b"><div class="wrap fascia"><h2>Lo vuoi nella tua cucina?</h2>'
            f'<a class="btn" href="{r}cucine.html#richiesta">Chiedi un campione →</a></div></section>')


def foto_presenti():
    """Le foto disponibili: quelle nella cartella site/foto/ più quelle elencate in strumenti/foto-sul-server.txt."""
    radice = RADICE
    nomi = {p.stem for p in (radice / 'site' / 'foto').glob('*.jpg')}
    elenco = radice / 'strumenti' / 'foto-sul-server.txt'
    if elenco.exists():
        for riga in elenco.read_text(encoding='utf-8').splitlines():
            if riga.strip() and not riga.startswith('#'):
                nomi.add(riga.split()[0].removesuffix('.jpg'))
    return nomi


def foto_banda(r, nome, alt):
    if nome + '-banda' not in foto_presenti():
        alt = ''   # finché la foto non c'è esce un disegno decorativo: nessuna descrizione
    return (f'<div class="wrap"><figure class="foto larga"><img src="{r}foto.php?f={nome}&amp;v=banda" alt="{alt}" width="1600" height="640" decoding="async"></figure></div>')


def voce(href, titolo, breve):
    return f'<a href="{href}"><b>{titolo}</b><span>{breve}</span><i>→</i></a>'


def briciole_schema(*passi):
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList',
            'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': u} for i, (n, u) in enumerate(passi)]}


def pagina(percorso, titolo, desc, corpo, r='', menu=None, schemi=(), articolo=False, noindex=False):
    url = URL + percorso.replace('index.html', '')
    h = ['<!doctype html>', '<html lang="it">', '<head>', '<meta charset="utf-8">', '<meta name="viewport" content="width=device-width, initial-scale=1">',
         f'<title>{titolo}</title>', f'<meta name="description" content="{desc}">']
    h.append('<meta name="robots" content="noindex">' if noindex else f'<link rel="canonical" href="{url}">')
    h += [f'<meta property="og:type" content="{"article" if articolo else "website"}">', '<meta property="og:site_name" content="Filo Corto">',
          f'<meta property="og:title" content="{titolo}">', f'<meta property="og:description" content="{desc}">', f'<meta property="og:url" content="{url}">',
          f'<meta property="og:image" content="{URL}og.png">', '<meta property="og:image:width" content="1200">', '<meta property="og:image:height" content="630">',
          '<meta property="og:locale" content="it_IT">', '<meta name="twitter:card" content="summary_large_image">',
          '<meta name="theme-color" content="#2f5d3a">', f'<link rel="icon" href="{r}favicon.svg" type="image/svg+xml">', f'<link rel="apple-touch-icon" href="{r}icona.png">',
          f'<link rel="preload" href="{r}fonts/archivo.woff2" as="font" type="font/woff2" crossorigin>',
          '<script>document.documentElement.className="js"</script>', f'<link rel="stylesheet" href="{r}style.css?v={CSS_V}">']
    for s in (ORG, *schemi):
        h.append('<script type="application/ld+json">' + json.dumps(s, ensure_ascii=False) + '</script>')
    voci = list(MENU)
    if STATO['rete']:
        voci.insert(2, ('produttori/', 'La rete'))
    h += ['</head>', '<body>', '<a class="salta" href="#contenuto">Vai al contenuto</a>',
          f'<div class="barra"><div class="wrap">Lazio · Rete in costruzione · <a href="{r}produttori.html#candidati">Raccogliamo le adesioni dei produttori</a></div></div>',
          '<header class="testata t2"><div class="wrap">',
          f'<a class="marchio" href="{r or "./"}" aria-label="Filo Corto, pagina iniziale">{LOGO}<span><b>filo corto</b><small>Dal produttore alla cucina</small></span></a>',
          f'<div class="azioni"><a class="btn verde" href="{r}produttori.html#candidati">Candidati</a>'
          '<button class="apri" type="button" aria-expanded="false" aria-controls="menu">Menu<i></i></button></div>',
          '<nav class="menu" id="menu" aria-label="Menu principale">']
    for href, nome in voci:
        h.append(f'<a href="{r}{href}"' + (' aria-current="page"' if menu == href else '') + f'>{nome}</a>')
    rete = f'<a href="{r}produttori/">I produttori della rete</a>' if STATO['rete'] else ''
    cucine = f'<a href="{r}per-le-cucine/">Prodotti del Lazio per le cucine</a>' if STATO['cucine'] else ''
    h += [f'<a class="btn verde" href="{r}produttori.html#candidati">Candidati</a>', '</nav>', '</div></header>', '<main id="contenuto">', corpo, '</main>',
          '<footer class="piede"><div class="wrap">', '<div class="col">',
          '<div><b class="w">filo corto</b><p>Dal produttore alla cucina.<br>Solo materie prime italiane.<br>Rete in costruzione: si parte dal Lazio.</p></div>',
          f'<div><h3>Produttori</h3><a href="{r}produttori.html">Entra nella rete</a>{rete}<a href="{r}check-up.html">Il check-up</a><a href="{r}filo-doro.html">Il filo d’oro</a><a href="{r}prova.html">Sei pronto? Fai la prova</a><a href="{r}guide/">Guide per vendere ai ristoranti</a><a href="{r}territori/">I territori del Lazio</a></div>',
          f'<div><h3>Per chi compra</h3><a href="{r}cucine.html">Ristoranti, hotel e aziende</a>{cucine}<a href="{r}come-funziona.html">Come funziona</a><a href="{r}riga-menu.html">La riga per il menu</a></div>',
          f'<div><h3>Filo Corto</h3><a href="{r}chi-siamo.html">Chi siamo</a><a href="{r}domande.html">Domande frequenti</a><a href="{r}enti.html">Per consorzi e territori</a><a href="mailto:info@ilfilocorto.it">info@ilfilocorto.it</a><a href="{r}privacy.html">Informativa privacy</a><a href="{r}crediti.html">Crediti delle immagini</a></div>', '</div>',
          '<div class="fine"><span>Un progetto <a href="https://sicurofood.com" rel="noopener">SicuroFood</a></span><span>© 2026 Filo Corto</span></div>',
          '</div></footer>', SCRIPT + '</body>', '</html>', '']
    return '\n'.join(h)


def articolo(d, nome_sezione, url_sezione, nota, coda, occhiello='', menu=None, luogo=None):
    """Pagina di lettura (guida, territorio, prodotto per le cucine): stessa forma per tutte."""
    percorso = url_sezione + d['slug'] + '.html'
    url = URL + percorso
    art = {'@context': 'https://schema.org', '@type': 'Article', 'headline': d['h1'], 'description': d['desc'], 'inLanguage': 'it', 'datePublished': d['data'], 'dateModified': d['data'],
           'mainEntityOfPage': url, 'image': URL + 'og.png', 'author': AUTORE, 'publisher': EDITORE}
    if luogo:
        art['about'] = {'@type': 'Place', 'name': luogo, 'containedInPlace': {'@type': 'AdministrativeArea', 'name': 'Lazio'}}
    schemi = [art, briciole_schema(('Filo Corto', URL), (nome_sezione, URL + url_sezione), (d['h1'], url))]
    banda = foto_banda('../', d['foto'], d.get('foto_alt', '')) if d.get('foto') else ''
    corpo = ('<div class="wrap"><div class="capo"><p class="briciole"><a href="../">Filo Corto</a> / <a href="./">' + nome_sezione + '</a></p>'
             + (f'<p class="occhiello">{occhiello}</p>' if occhiello else '')
             + f'<h1>{d["h1"]}</h1><p class="grande">{d["intro"]}</p>'
             f'<p class="piccolo">A cura di Valerio Semeraro, Food Specialist e consulente HACCP · Aggiornata a {mese(d["data"])}<br>'
             'Scritta con l\'aiuto dell\'intelligenza artificiale, su fonti ufficiali. <a href="../come-funziona.html#ia">Come lavoriamo</a></p></div></div>'
             + (banda + '<section class="sez bianca">' if banda else '<div class="filo"></div><section class="sez bianca" style="border-top:0">')
             + f'<div class="wrap"><article class="prosa">{d["corpo"]}<div class="nota"><p><strong>Nota.</strong> {nota}</p></div></article></div></section>' + coda)
    (RADICE / 'site' / url_sezione).mkdir(parents=True, exist_ok=True)
    (RADICE / 'site' / percorso).write_text(pagina(percorso, d['titolo'], d['desc'], corpo, r='../', menu=menu, schemi=schemi, articolo=True), encoding='utf-8')


def indice(url_sezione, nome, titolo, desc, h1, intro, voci, coda, menu=None, banda='', dopo=''):
    corpo = (f'<div class="wrap"><div class="capo"><p class="briciole"><a href="../">Filo Corto</a> / {nome}</p><h1>{h1}</h1><p class="grande">{intro}</p></div></div>' + banda
             + f'<section class="sez bianca"><div class="wrap"><div class="elenco-guide">{voci}</div>{dopo}</div></section>' + coda)
    (RADICE / 'site' / url_sezione).mkdir(parents=True, exist_ok=True)
    (RADICE / 'site' / url_sezione / 'index.html').write_text(pagina(url_sezione + 'index.html', titolo, desc, corpo, r='../', menu=menu), encoding='utf-8')


def altre(titolo_occhiello, titolo, voci):
    return f'<section class="sez"><div class="wrap"><div class="testa"><p class="occhiello">{titolo_occhiello}</p><h2>{titolo}</h2></div><div class="elenco-guide">{voci}</div></div></section>' if voci else ''


# ---------- Guide per i produttori ----------
# Intestazione di src/guide/<slug>.html: titolo, h1, desc, breve, intro, data (AAAA-MM-GG); facoltativi: foto, foto_alt.

def guide(nuove):
    tutte = [(g['slug'], g['h1'], g['breve']) for g in nuove] + STORICHE
    for g in nuove:
        vicine = ''.join(voce(s + '.html', t, b) for s, t, b in [t for t in tutte if t[0] != g['slug']][:3])
        articolo(g, 'Guide', 'guide/', 'Questa guida è informativa e riassume le regole generali. Per i casi particolari fa fede la norma, e l\'ufficio a cui chiedere è la ASL del tuo territorio.',
                 altre('Continua a leggere', 'Altre guide', vicine) + cta('../'), menu='guide/')
    dopo = '<div class="etichette"><a href="../territori/">I territori del Lazio →</a><a href="../prova.html">Sei pronto? Fai la prova →</a>' + ('<a href="../per-le-cucine/">Per chi cucina →</a>' if STATO['cucine'] else '') + '</div>'
    indice('guide/', 'Guide', 'Guide per produttori: vendere a ristoranti e hotel | Filo Corto',
           'Guide pratiche per piccoli produttori che vogliono vendere alla ristorazione: come proporsi, documenti e requisiti, listino, cosa chiede uno chef, prodotto per prodotto.',
           'Vendere alla ristorazione, <em>senza giri di parole.</em>', 'Guide gratuite per i piccoli produttori, scritte da chi sta in cucina. Cosa serve, in che ordine.',
           ''.join(voce(s + '.html', t, b) for s, t, b in tutte), cta('../'), menu='guide/', banda=foto_banda('../', 'legumi', 'Legumi secchi al mercato'), dopo=dopo)


# ---------- Pagine di territorio ----------
# Intestazione di src/territori/<slug>.html: titolo, h1, desc, breve, intro, zona (es. Provincia di Viterbo), data; facoltativi: foto, foto_alt.

def territori(elenco):
    if not elenco:
        return
    utili = altre('Prima di proporti', 'Le guide utili',
                  voce('../guide/vendere-ai-ristoranti.html', 'Come vendere ai ristoranti', 'I passi concreti, dal prodotto al pagamento.')
                  + voce('../guide/documenti-per-vendere-ai-ristoranti.html', 'Documenti e requisiti', 'Cosa serve per vendere a ristoranti e hotel.')
                  + voce('../guide/listino-per-ristoranti.html', 'Il listino per ristoranti', 'Cosa scriverci e in quale forma.'))
    for d in elenco:
        vicini = ''.join(voce(t['slug'] + '.html', t['h1'], t['breve']) for t in elenco if t['slug'] != d['slug'])
        articolo(d, 'Territori', 'territori/', 'DOP, IGP e DOC si possono scrivere su etichetta, listino e menu solo per il prodotto certificato secondo il disciplinare. In caso di dubbio fa fede il consorzio di tutela o l\'organismo di controllo.',
                 utili + altre('Altri territori', 'Il resto del Lazio', vicini) + cta('../'), occhiello=d.get('zona', ''), luogo=d.get('zona', ''))
    indice('territori/', 'Territori', 'Produttori del Lazio per territorio: cosa cerca la ristorazione | Filo Corto',
           'Tuscia, Sabina, Castelli Romani, Ciociaria, Agro Pontino: cosa si produce nelle zone del Lazio e come proporsi a ristoranti, bar e hotel.',
           'I territori <em>del Lazio.</em>', 'Cosa si produce zona per zona, e cosa cerca la ristorazione. Per i piccoli produttori che vogliono arrivare nelle cucine.',
           ''.join(voce(d['slug'] + '.html', d['h1'], d['breve']) for d in elenco), cta('../'), banda=foto_banda('../', 'civita', 'Civita di Bagnoregio, in provincia di Viterbo'))


# ---------- Prodotti del Lazio, per chi cucina ----------
# Intestazione di src/cucine/<slug>.html: titolo, h1, desc, breve, intro, data; facoltativi: foto, foto_alt.
# Nessun nome di azienda e nessun prezzo: cosa esiste, come riconoscerlo, cosa chiedere a chi lo vende.

def per_le_cucine(elenco):
    if not elenco:
        return
    for d in elenco:
        vicini = ''.join(voce(t['slug'] + '.html', t['h1'], t['breve']) for t in elenco if t['slug'] != d['slug'])
        articolo(d, 'Per le cucine', 'per-le-cucine/', 'DOP, IGP e biologico si scrivono nel menu solo per il prodotto certificato. Le informazioni di questa pagina sono generali: per ogni prodotto fanno fede il disciplinare e l\'etichetta.',
                 altre('Sul menu', 'Racconta chi c\'è dietro il piatto', voce('../riga-menu.html', 'La riga per il menu', 'Nome e luogo del produttore, pronti da copiare.'))
                 + altre('Altri prodotti', 'Dal Lazio alla cucina', vicini) + cta_cucine('../'), menu='cucine.html')
    indice('per-le-cucine/', 'Per le cucine', 'Prodotti del Lazio per ristoranti: cosa c\'è e cosa chiedere | Filo Corto',
           'I prodotti del Lazio visti da chi cucina: denominazioni, stagioni, formati, cosa chiedere a chi li vende. Per ristoranti, bar e hotel.',
           'Il Lazio, <em>prodotto per prodotto.</em>', 'Cosa c\'è, quando c\'è, come riconoscerlo e cosa chiedere a chi lo vende. Scritto per chi cucina.',
           ''.join(voce(d['slug'] + '.html', d['h1'], d['breve']) for d in elenco), cta_cucine('../'), menu='cucine.html')


# ---------- Pagine dei produttori della rete ----------
# Intestazione di src/produttori/<slug>.html (vedi esempi/produttore-modello.html):
# nome, categoria (es. Olio extravergine), zona (es. Sabina, provincia di Rieti), comune,
# prodotti (separati da ;), stagione, consegne, certificazioni (solo con certificato, altrimenti vuoto),
# foto (nomi dei file in site/produttori/foto/, separati da ;), breve, desc, consenso (data del consenso scritto).

def produttori(elenco):
    if not elenco:
        return
    cartella = RADICE / 'site/produttori'
    (cartella / 'qr').mkdir(parents=True, exist_ok=True)
    for d in elenco:
        url = URL + 'produttori/' + d['slug'] + '.html'
        lista = [x.strip() for x in d.get('prodotti', '').split(';') if x.strip()]
        foto = [x.strip() for x in d.get('foto', '').split(';') if x.strip()]
        schemi = [{'@context': 'https://schema.org', '@type': 'LocalBusiness', 'name': d['nome'], 'description': d['desc'], 'url': url,
                   'address': {'@type': 'PostalAddress', 'addressLocality': d.get('comune', ''), 'addressRegion': 'Lazio', 'addressCountry': 'IT'},
                   'areaServed': 'Lazio', 'makesOffer': [{'@type': 'Offer', 'itemOffered': {'@type': 'Product', 'name': x}} for x in lista],
                   **({'image': [URL + 'produttori/foto/' + f for f in foto]} if foto else {})},
                  briciole_schema(('Filo Corto', URL), ('I produttori della rete', URL + 'produttori/'), (d['nome'], url))]
        fatti = [('Zona', d.get('zona', '')), ('Prodotti', ', '.join(lista)), ('Stagione', d.get('stagione', '')), ('Consegne', d.get('consegne', '')), ('Certificazioni', d.get('certificazioni', ''))]
        scheda = ''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in fatti if v)
        galleria = ('<div class="foto-p">' + ''.join(f'<img src="foto/{f}" alt="{d["nome"]}: foto {i + 1}" loading="lazy">' for i, f in enumerate(foto)) + '</div>') if foto else ''
        (cartella / 'qr' / (d['slug'] + '.svg')).write_text(qr.svg(url), encoding='utf-8')   # il QR porta a questa pagina
        codice = (f'<div class="qr-p"><img src="qr/{d["slug"]}.svg" alt="Codice QR della pagina di {d["nome"]}" width="112" height="112">'
                  f'<p><b>Il QR di questa pagina</b>Per etichette, cassette e menu: chi inquadra arriva qui. <a href="qr/{d["slug"]}.svg" download>Scarica il QR</a></p></div>')
        corpo = (f'<div class="wrap"><div class="capo"><p class="briciole"><a href="../">Filo Corto</a> / <a href="./">I produttori della rete</a></p>'
                 f'<p class="occhiello">{d.get("categoria", "")} · {d.get("zona", "")}</p><h1>{d["nome"]}</h1><p class="grande">{d["breve"]}</p></div></div><div class="filo"></div>'
                 f'<section class="sez bianca" style="border-top:0"><div class="wrap due"><article class="prosa">{d["corpo"]}</article>'
                 f'<aside><dl class="scheda-p">{scheda}</dl>'
                 '<p class="piccolo">I prezzi per la ristorazione si chiedono con il modulo: rispondiamo per email con listino, ordine minimo e giorni di consegna.</p>'
                 f'<a class="btn miele" href="../cucine.html#richiesta">Chiedi un campione →</a>{codice}</aside></div>'
                 f'<div class="wrap">{galleria}<div class="nota"><p><strong>Nota.</strong> Le informazioni su questa pagina sono fornite dal produttore e pubblicate con il suo consenso. '
                 'Filo Corto non vende al posto del produttore: mette in contatto, e il produttore fattura direttamente alla cucina.</p></div></div></section>' + cta('../'))
        (cartella / (d['slug'] + '.html')).write_text(pagina('produttori/' + d['slug'] + '.html', f'{d["nome"]} – {d.get("categoria", "")} dal Lazio per ristoranti | Filo Corto', d['desc'], corpo, r='../', schemi=schemi), encoding='utf-8')
    voci = ''.join(voce(d['slug'] + '.html', d['nome'], f'{d.get("categoria", "")} · {d.get("zona", "")}. {d["breve"]}') for d in elenco)
    indice('produttori/', 'I produttori della rete', 'I produttori della rete: piccoli produttori del Lazio per ristoranti | Filo Corto',
           'I piccoli produttori del Lazio che hanno aderito a Filo Corto: chi sono, cosa producono, dove si trovano. Per ristoranti, bar e hotel del Lazio.',
           'I produttori <em>della rete.</em>', 'Piccoli produttori del Lazio che hanno aderito a Filo Corto. Ogni pagina è scritta con il produttore e pubblicata con il suo consenso.',
           voci, cta('../'), menu='produttori/')


# ---------- Controlli prima di pubblicare ----------

def controlla():
    sito = RADICE / 'site'
    esistono = {str(p.relative_to(sito)).replace('\\', '/') for p in sito.rglob('*') if p.is_file()} | SOLO_SERVER
    errori = []
    for f in sorted(sito.rglob('*.html')):
        testo = f.read_text(encoding='utf-8')
        qui = str(f.relative_to(sito)).replace('\\', '/')
        if re.search(r'\bverificat[oaie]\b', testo, re.I):
            errori.append(f'{qui}: contiene la parola «verificato» (vietata)')
        if re.search(r'(?<![\d/.-])(?:\+39[ .]?)?3\d{2}[ .]?\d{3}[ .]?\d{3,4}(?![\d/.-])', re.sub(r'<script.*?</script>|<svg.*?</svg>', '', testo, flags=re.S)):
            errori.append(f'{qui}: sembra contenere un numero di telefono (vietato)')
        for m in re.finditer(r'(?:href|src|action)="([^"]+)"', re.sub(r'<script.*?</script>', '', testo, flags=re.S)):
            u = m.group(1)
            if re.match(r'(https?:|mailto:|tel:|data:|#|javascript:)', u):
                continue
            u = u.split('#')[0].split('?')[0]
            if not u:
                continue
            parti = []
            for p in (u if u.startswith('/') else str(pathlib.PurePosixPath(qui).parent / u)).split('/'):
                if p == '..':
                    if parti:
                        parti.pop()
                elif p not in ('', '.'):
                    parti.append(p)
            dest = '/'.join(parti)
            if u.endswith('/') or u in ('.', '..') or dest == '':
                dest = (dest + '/' if dest else '') + 'index.html'
            if dest not in esistono:
                errori.append(f'{qui}: collegamento rotto verso «{m.group(1)}»')
    return errori


def costruisci():
    runpy.run_path(str(RADICE / 'strumenti/pagine.py'))   # riscrive src/pagine/ dalle pagine principali
    nuove = carica('guide', lambda g: g.get('data', ''))[::-1]
    zone = carica('territori', lambda d: d['h1'])
    piatti = carica('cucine', lambda d: d['h1'])
    rete = carica('produttori', lambda d: d['nome'].lower())
    for d in rete:
        for campo, cosa in (('campione', 'del campione approvato da Val'), ('consenso', 'del consenso scritto')):
            if not re.match(r'\d{4}-\d{2}-\d{2}$', d.get(campo, '')):
                raise SystemExit(f'Manca la data {cosa} per {d["slug"]}: la pagina non si pubblica.')
    STATO['rete'], STATO['cucine'] = bool(rete), bool(piatti)

    guide(nuove)
    territori(zone)
    per_le_cucine(piatti)
    produttori(rete)

    # In home: le ultime uscite (si aggiornano da sole) e, quando ci sono, i produttori della rete.
    uscite = sorted([('guide/', g) for g in nuove] + [('territori/', d) for d in zone] + [('per-le-cucine/', d) for d in piatti], key=lambda t: t[1].get('data', ''), reverse=True)[:2]
    ultime = (voce('guide/vendere-ai-ristoranti.html', 'Come vendere ai ristoranti', 'La guida da cui partire.')
              + ''.join(voce(base + d['slug'] + '.html', d['h1'], d['breve']) for base, d in uscite)
              + voce('prova.html', 'Sei pronto? Fai la prova', 'Dieci domande, due minuti.'))
    in_rete = ''
    if rete:
        in_rete = ('<section class="sez bianca"><div class="wrap"><div class="testa"><p class="occhiello">La rete</p><h2>I produttori che puoi già conoscere</h2></div><div class="elenco-guide">'
                   + ''.join(voce('produttori/' + d['slug'] + '.html', d['nome'], f'{d.get("categoria", "")} · {d.get("zona", "")}') for d in rete[:6])
                   + '</div><p style="margin-top:22px"><a href="produttori/">Tutti i produttori della rete →</a></p></div></section>')
    for p in (RADICE / 'src/pagine').glob('*.html'):
        d = leggi(p)
        schemi = [json.loads(d['schema'])] if d.get('schema') else []
        corpo = d['corpo'].replace('<!--ULTIME-->', ultime).replace('<!--RETE-->', in_rete).replace('<!--CUCINE-->', '<a href="per-le-cucine/">Il Lazio, prodotto per prodotto →</a>' if piatti else '')
        (RADICE / 'site' / (d['slug'] + '.html')).write_text(pagina(d['slug'] + '.html', d['titolo'], d['desc'], corpo, r=d.get('radice', ''), menu=d.get('menu') or None, noindex=d.get('noindex') == 'si', schemi=schemi), encoding='utf-8')

    righe = [f'<url><loc>{URL}{u}</loc></url>' for u in PAGINE_FISSE] + [f'<url><loc>{URL}guide/{s}.html</loc></url>' for s, _, _ in STORICHE] + [f'<url><loc>{URL}guide/{g["slug"]}.html</loc><lastmod>{g["data"]}</lastmod></url>' for g in nuove]
    if zone:
        righe += [f'<url><loc>{URL}territori/</loc></url>'] + [f'<url><loc>{URL}territori/{d["slug"]}.html</loc><lastmod>{d["data"]}</lastmod></url>' for d in zone]
    if piatti:
        righe += [f'<url><loc>{URL}per-le-cucine/</loc></url>'] + [f'<url><loc>{URL}per-le-cucine/{d["slug"]}.html</loc><lastmod>{d["data"]}</lastmod></url>' for d in piatti]
    if rete:
        righe += [f'<url><loc>{URL}produttori/</loc></url>'] + [f'<url><loc>{URL}produttori/{d["slug"]}.html</loc></url>' for d in rete]
    (RADICE / 'site/sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + '\n'.join(righe) + '\n</urlset>\n', encoding='utf-8')

    errori = controlla()
    print(f'Costruite {len(nuove)} guide nuove ({len(nuove) + len(STORICHE)} in indice), {len(zone)} territori, {len(piatti)} pagine per le cucine, {len(rete)} produttori ({datetime.date.today().isoformat()}).')
    if errori:
        print('\nERRORI: non pubblicare finché non sono corretti.\n- ' + '\n- '.join(errori))
        raise SystemExit(1)
    print('Controlli: collegamenti a posto, nessuna parola vietata.')


if __name__ == '__main__':
    costruisci()
