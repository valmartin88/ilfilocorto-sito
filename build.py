#!/usr/bin/env python3
"""Filo Corto – genera le pagine del sito a partire dai testi in src/.

Uso: python3 build.py
- src/guide/<slug>.html  -> site/guide/<slug>.html (+ indice guide e sitemap)
- src/pagine/<nome>.html -> site/<nome>.html
- src/territori/<slug>.html -> site/territori/<slug>.html (+ indice /territori/)
- src/produttori/<slug>.html -> site/produttori/<slug>.html (+ pagina «I produttori della rete», solo se ce n'è almeno uno)
  Si pubblica un produttore SOLO dopo scheda di adesione, check-up e consenso scritto alla pubblicazione (vedi README).
Ogni file in src/ comincia con righe "chiave: valore", poi una riga "---", poi il corpo HTML.
La cartella site/ viene copiata sopra public_html dal server (vedi README).
"""
import json, pathlib, datetime

RADICE = pathlib.Path(__file__).parent
URL = 'https://ilfilocorto.it/'
CSS_V = '5'

# Guide pubblicate prima di questo sistema: i file restano sul server, qui servono per indice e sitemap.
STORICHE = [
    ('vendere-ai-ristoranti', 'Come vendere ai ristoranti: la guida per piccoli produttori', 'I passi concreti: prodotti, listino, documenti, campione, consegne, pagamenti.'),
    ('documenti-per-vendere-ai-ristoranti', 'Documenti e requisiti per vendere a ristoranti e hotel', 'Registrazione, autocontrollo, lotti, etichette, imballaggi, trasporto.'),
    ('cosa-chiede-uno-chef', 'Cosa chiede uno chef a un fornitore', 'Le tre domande di ogni cucina, viste da dentro.'),
    ('listino-per-ristoranti', 'Come preparare un listino per ristoranti', 'Cosa scriverci, in quale forma, con un esempio.'),
    ('filiera-corta-km-0', 'Filiera corta e chilometro zero: cosa dice la legge', 'Le definizioni della legge 61/2022, in parole semplici.'),
]
PAGINE_FISSE = ['', 'produttori.html', 'cucine.html', 'come-funziona.html', 'prova.html', 'riga-menu.html', 'check-up.html', 'guide/', 'domande.html', 'chi-siamo.html', 'privacy.html']

LOGO = '<svg width="46" height="46" viewBox="0 0 60 60" fill="none" aria-hidden="true"><circle cx="30" cy="38" r="16.85" fill="#F2F4F0" stroke="#E8692C" stroke-width="6.3"/><circle cx="30" cy="38" r="5.85" fill="#12302B"/><path d="M30 21 C 30 11, 37 5, 48 5 C 48 15, 41 21, 30 21 Z" fill="#2f5d3a"/></svg>'
ORG = {'@context': 'https://schema.org', '@type': 'Organization', 'name': 'Filo Corto', 'url': URL, 'logo': URL + 'icona.png', 'email': 'info@ilfilocorto.it', 'areaServed': 'Lazio', 'description': 'Rete di piccoli produttori del Lazio per ristoranti, bar e hotel. Rete in costruzione.', 'founder': {'@type': 'Person', 'name': 'Valerio Semeraro'}}
MENU = [('produttori.html', 'Produttori'), ('cucine.html', 'Cucine'), ('come-funziona.html', 'Come funziona'), ('check-up.html', 'Check-up'), ('guide/', 'Guide'), ('chi-siamo.html', 'Chi siamo')]


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


def cta(r):
    return ('<section class="sez verde-b"><div class="wrap due" style="align-items:center"><div><p class="occhiello">Per i produttori</p><h2>Produci nel Lazio?</h2></div>'
            '<div style="display:flex;flex-direction:column;gap:22px;align-items:flex-start"><p class="grande">Candidati alla rete. È gratuito, non ti impegna e ti rispondiamo per email con la scheda di adesione.</p>'
            f'<a class="btn miele" href="{r}produttori.html#candidati">Candidati adesso →</a></div></div></section>')


def pagina(percorso, titolo, desc, corpo, r='', menu=None, schemi=(), articolo=False, noindex=False, script=''):
    url = URL + percorso.replace('index.html', '')
    h = ['<!doctype html>', '<html lang="it">', '<head>', '<meta charset="utf-8">', '<meta name="viewport" content="width=device-width, initial-scale=1">',
         f'<title>{titolo}</title>', f'<meta name="description" content="{desc}">']
    h.append('<meta name="robots" content="noindex">' if noindex else f'<link rel="canonical" href="{url}">')
    h += [f'<meta property="og:type" content="{"article" if articolo else "website"}">', '<meta property="og:site_name" content="Filo Corto">',
          f'<meta property="og:title" content="{titolo}">', f'<meta property="og:description" content="{desc}">', f'<meta property="og:url" content="{url}">',
          f'<meta property="og:image" content="{URL}og.png">', '<meta property="og:locale" content="it_IT">', '<meta name="twitter:card" content="summary_large_image">',
          '<meta name="theme-color" content="#2f5d3a">', f'<link rel="icon" href="{r}favicon.svg" type="image/svg+xml">', f'<link rel="apple-touch-icon" href="{r}icona.png">',
          f'<link rel="preload" href="{r}fonts/archivo.woff2" as="font" type="font/woff2" crossorigin>', f'<link rel="stylesheet" href="{r}style.css?v={CSS_V}">']
    for s in (ORG, *schemi):
        h.append('<script type="application/ld+json">' + json.dumps(s, ensure_ascii=False) + '</script>')
    h += ['</head>', '<body>',
          f'<div class="barra"><div class="wrap">Lazio · Rete in costruzione · <a href="{r}produttori.html#candidati">Raccogliamo le adesioni dei produttori</a></div></div>',
          '<header class="testata"><div class="wrap">',
          f'<a class="marchio" href="{r or "./"}" aria-label="Filo Corto, pagina iniziale">{LOGO}<span><b>filo corto</b><small>Dal produttore alla cucina</small></span></a>',
          '<nav class="menu" aria-label="Menu principale">']
    for href, nome in MENU:
        h.append(f'<a href="{r}{href}"' + (' aria-current="page"' if menu == href else '') + f'>{nome}</a>')
    h += [f'<a class="btn verde" href="{r}produttori.html#candidati">Candidati</a>', '</nav>', '</div></header>', '<main>', corpo, '</main>',
          '<footer class="piede"><div class="wrap">', '<div class="col">',
          '<div><b class="w">filo corto</b><p>Dal produttore alla cucina.<br>Lazio.<br>Rete in costruzione: oggi raccogliamo le adesioni.</p></div>',
          f'<div><h3>Produttori</h3><a href="{r}produttori.html">Entra nella rete</a><a href="{r}check-up.html">Il check-up</a><a href="{r}guide/">Guide per vendere ai ristoranti</a><a href="{r}prova.html">Sei pronto? Fai la prova</a><a href="{r}domande.html">Domande frequenti</a></div>',
          f'<div><h3>Cucine</h3><a href="{r}cucine.html">Ristoranti, bar e hotel</a><a href="{r}come-funziona.html">Come funziona</a><a href="{r}riga-menu.html">La riga per il menu</a><a href="{r}chi-siamo.html">Chi siamo</a></div>',
          f'<div><h3>Contatti</h3><a href="mailto:info@ilfilocorto.it">info@ilfilocorto.it</a><a href="{r}privacy.html">Informativa privacy</a></div>', '</div>',
          '<div class="fine"><span>Un progetto di Valerio Semeraro, Food Specialist e consulente HACCP – Roma</span><span>© 2026 Filo Corto</span></div>',
          '</div></footer>', script + '</body>', '</html>', '']
    return '\n'.join(h)


def voce(slug, h1, breve):
    return f'<a href="{slug}.html"><b>{h1}</b><span>{breve}</span><i>→</i></a>'


# ---------- Pagine dei produttori della rete ----------
# Intestazione di src/produttori/<slug>.html (vedi esempi/produttore-modello.html):
# nome, categoria (es. Olio extravergine), zona (es. Sabina, provincia di Rieti), comune,
# prodotti (separati da ;), stagione, consegne, certificazioni (solo con certificato, altrimenti vuoto),
# foto (nomi dei file in site/produttori/foto/, separati da ;), breve, desc, consenso (data del consenso scritto).

def produttori():
    elenco = sorted((leggi(p) for p in (RADICE / 'src/produttori').glob('*.html')), key=lambda d: d['nome'].lower()) if (RADICE / 'src/produttori').exists() else []
    cartella = RADICE / 'site/produttori'
    for d in elenco:
        if not d.get('consenso'):
            raise SystemExit(f'Manca la data del consenso scritto per {d["slug"]}: la pagina non si pubblica.')
        cartella.mkdir(parents=True, exist_ok=True)
        url = URL + 'produttori/' + d['slug'] + '.html'
        lista = [x.strip() for x in d.get('prodotti', '').split(';') if x.strip()]
        foto = [x.strip() for x in d.get('foto', '').split(';') if x.strip()]
        schemi = [{'@context': 'https://schema.org', '@type': 'LocalBusiness', 'name': d['nome'], 'description': d['desc'], 'url': url,
                   'address': {'@type': 'PostalAddress', 'addressLocality': d.get('comune', ''), 'addressRegion': 'Lazio', 'addressCountry': 'IT'},
                   'areaServed': 'Lazio', 'makesOffer': [{'@type': 'Offer', 'itemOffered': {'@type': 'Product', 'name': x}} for x in lista],
                   **({'image': [URL + 'produttori/foto/' + f for f in foto]} if foto else {})},
                  {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': 1, 'name': 'Filo Corto', 'item': URL}, {'@type': 'ListItem', 'position': 2, 'name': 'I produttori della rete', 'item': URL + 'produttori/'}, {'@type': 'ListItem', 'position': 3, 'name': d['nome'], 'item': url}]}]
        fatti = [('Zona', d.get('zona', '')), ('Prodotti', ', '.join(lista)), ('Stagione', d.get('stagione', '')), ('Consegne', d.get('consegne', '')), ('Certificazioni', d.get('certificazioni', ''))]
        scheda = ''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in fatti if v)
        galleria = ('<div class="foto-p">' + ''.join(f'<img src="foto/{f}" alt="{d["nome"]}: foto {i + 1}" loading="lazy">' for i, f in enumerate(foto)) + '</div>') if foto else ''
        corpo = (f'<div class="wrap"><div class="capo"><p class="briciole"><a href="../">Filo Corto</a> / <a href="./">I produttori della rete</a></p>'
                 f'<p class="occhiello">{d.get("categoria", "")} · {d.get("zona", "")}</p><h1>{d["nome"]}</h1><p class="grande">{d["breve"]}</p></div></div><div class="filo"></div>'
                 f'<section class="sez bianca" style="border-top:0"><div class="wrap due"><article class="prosa">{d["corpo"]}</article>'
                 f'<aside><dl class="scheda-p">{scheda}</dl>'
                 '<p class="piccolo">I prezzi per la ristorazione si chiedono con il modulo: rispondiamo per email con listino, ordine minimo e giorni di consegna.</p>'
                 '<a class="btn miele" href="../cucine.html">Chiedi un campione →</a></aside></div>'
                 f'<div class="wrap">{galleria}<div class="nota"><p><strong>Nota.</strong> Le informazioni su questa pagina sono fornite dal produttore e pubblicate con il suo consenso. '
                 'Filo Corto non vende al posto del produttore: mette in contatto, e il produttore fattura direttamente alla cucina.</p></div></div></section>' + cta('../'))
        (cartella / (d['slug'] + '.html')).write_text(pagina('produttori/' + d['slug'] + '.html', f'{d["nome"]} – {d.get("categoria", "")} dal Lazio per ristoranti | Filo Corto', d['desc'], corpo, r='../', schemi=schemi), encoding='utf-8')
    if elenco:
        voci = ''.join(f'<a href="{d["slug"]}.html"><b>{d["nome"]}</b><span>{d.get("categoria", "")} · {d.get("zona", "")}. {d["breve"]}</span><i>→</i></a>' for d in elenco)
        indice = ('<div class="wrap"><div class="capo"><p class="briciole"><a href="../">Filo Corto</a> / I produttori della rete</p><h1>I produttori della rete</h1>'
                  '<p class="grande">Piccoli produttori del Lazio che hanno aderito a Filo Corto. Ogni pagina è scritta con il produttore e pubblicata con il suo consenso.</p></div></div>'
                  f'<section class="sez bianca"><div class="wrap"><div class="elenco-guide">{voci}</div></div></section>' + cta('../'))
        (cartella / 'index.html').write_text(pagina('produttori/index.html', 'I produttori della rete: piccoli produttori del Lazio per ristoranti | Filo Corto',
                                                    'I piccoli produttori del Lazio che hanno aderito a Filo Corto: chi sono, cosa producono, dove si trovano. Per ristoranti, bar e hotel del Lazio.', indice, r='../'), encoding='utf-8')
    return elenco


# ---------- Pagine di territorio ----------
# Intestazione di src/territori/<slug>.html: titolo, h1, desc, breve, intro, zona (es. Provincia di Viterbo), data.

def territori():
    if not (RADICE / 'src/territori').exists():
        return []
    elenco = sorted((leggi(p) for p in (RADICE / 'src/territori').glob('*.html')), key=lambda d: d['h1'])
    if not elenco:
        return []
    cartella = RADICE / 'site/territori'
    cartella.mkdir(parents=True, exist_ok=True)
    for d in elenco:
        url = URL + 'territori/' + d['slug'] + '.html'
        schemi = [{'@context': 'https://schema.org', '@type': 'Article', 'headline': d['h1'], 'description': d['desc'], 'inLanguage': 'it', 'datePublished': d['data'], 'dateModified': d['data'], 'mainEntityOfPage': url, 'image': URL + 'og.png',
                   'about': {'@type': 'Place', 'name': d.get('zona', ''), 'containedInPlace': {'@type': 'AdministrativeArea', 'name': 'Lazio'}},
                   'author': {'@type': 'Person', 'name': 'Valerio Semeraro', 'jobTitle': 'Food Specialist e consulente HACCP'}, 'publisher': {'@type': 'Organization', 'name': 'Filo Corto', 'logo': {'@type': 'ImageObject', 'url': URL + 'icona.png'}}},
                  {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': 1, 'name': 'Filo Corto', 'item': URL}, {'@type': 'ListItem', 'position': 2, 'name': 'Territori', 'item': URL + 'territori/'}, {'@type': 'ListItem', 'position': 3, 'name': d['h1'], 'item': url}]}]
        altri = ''.join(f'<a href="{t["slug"]}.html"><b>{t["h1"]}</b><span>{t["breve"]}</span><i>→</i></a>' for t in elenco if t['slug'] != d['slug'])
        altri_sez = f'<section class="sez"><div class="wrap"><div class="testa"><p class="occhiello">Altri territori</p><h2>Il resto del Lazio</h2></div><div class="elenco-guide">{altri}</div></div></section>' if altri else ''
        corpo = (f'<div class="wrap"><div class="capo"><p class="briciole"><a href="../">Filo Corto</a> / <a href="./">Territori</a></p><p class="occhiello">{d.get("zona", "")}</p><h1>{d["h1"]}</h1><p class="grande">{d["intro"]}</p>'
                 '<p class="piccolo">Di Valerio Semeraro, Food Specialist e consulente HACCP</p></div></div><div class="filo"></div>'
                 f'<section class="sez bianca" style="border-top:0"><div class="wrap"><article class="prosa">{d["corpo"]}'
                 '<div class="nota"><p><strong>Nota.</strong> DOP, IGP e DOC si possono scrivere su etichetta, listino e menu solo per il prodotto certificato secondo il disciplinare. In caso di dubbio fa fede il consorzio di tutela o l\'organismo di controllo.</p></div></article></div></section>'
                 f'<section class="sez"><div class="wrap"><div class="testa"><p class="occhiello">Prima di proporti</p><h2>Le guide utili</h2></div><div class="elenco-guide">'
                 + voce('../guide/vendere-ai-ristoranti', 'Come vendere ai ristoranti', 'I passi concreti, dal prodotto al pagamento.')
                 + voce('../guide/documenti-per-vendere-ai-ristoranti', 'Documenti e requisiti', 'Cosa serve per vendere a ristoranti e hotel.')
                 + voce('../guide/listino-per-ristoranti', 'Il listino per ristoranti', 'Cosa scriverci e in quale forma.')
                 + '</div></div></section>' + altri_sez + cta('../'))
        (cartella / (d['slug'] + '.html')).write_text(pagina('territori/' + d['slug'] + '.html', d['titolo'], d['desc'], corpo, r='../', schemi=schemi, articolo=True), encoding='utf-8')
    voci = ''.join(f'<a href="{d["slug"]}.html"><b>{d["h1"]}</b><span>{d["breve"]}</span><i>→</i></a>' for d in elenco)
    indice = ('<div class="wrap"><div class="capo"><p class="briciole"><a href="../">Filo Corto</a> / Territori</p><h1>I territori del Lazio</h1>'
              '<p class="grande">Cosa si produce nelle diverse zone del Lazio e cosa cerca la ristorazione. Per i piccoli produttori che vogliono arrivare nelle cucine di ristoranti, bar e hotel.</p></div></div>'
              f'<section class="sez bianca"><div class="wrap"><div class="elenco-guide">{voci}</div></div></section>' + cta('../'))
    (cartella / 'index.html').write_text(pagina('territori/index.html', 'Produttori del Lazio per territorio: cosa cerca la ristorazione | Filo Corto',
                                                'Tuscia, Sabina, Castelli Romani, Ciociaria, Agro Pontino: cosa si produce nelle zone del Lazio e come proporsi a ristoranti, bar e hotel.', indice, r='../'), encoding='utf-8')
    return elenco


def costruisci():
    nuove = sorted((leggi(p) for p in (RADICE / 'src/guide').glob('*.html')), key=lambda g: g.get('data', ''), reverse=True)
    tutte = [(g['slug'], g['h1'], g['breve']) for g in nuove] + STORICHE
    for g in nuove:
        url = URL + 'guide/' + g['slug'] + '.html'
        schemi = [{'@context': 'https://schema.org', '@type': 'Article', 'headline': g['h1'], 'description': g['desc'], 'inLanguage': 'it', 'datePublished': g['data'], 'dateModified': g['data'], 'mainEntityOfPage': url, 'image': URL + 'og.png',
                   'author': {'@type': 'Person', 'name': 'Valerio Semeraro', 'jobTitle': 'Food Specialist e consulente HACCP'}, 'publisher': {'@type': 'Organization', 'name': 'Filo Corto', 'logo': {'@type': 'ImageObject', 'url': URL + 'icona.png'}}},
                  {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': 1, 'name': 'Filo Corto', 'item': URL}, {'@type': 'ListItem', 'position': 2, 'name': 'Guide', 'item': URL + 'guide/'}, {'@type': 'ListItem', 'position': 3, 'name': g['h1'], 'item': url}]}]
        altre = ''.join(voce(*t) for t in [t for t in tutte if t[0] != g['slug']][:3])
        mese = ['gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno', 'luglio', 'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre'][int(g['data'][5:7]) - 1] + ' ' + g['data'][:4]
        corpo = (f'<div class="wrap"><div class="capo"><p class="briciole"><a href="../">Filo Corto</a> / <a href="./">Guide</a></p><h1>{g["h1"]}</h1><p class="grande">{g["intro"]}</p>'
                 f'<p class="piccolo">Di Valerio Semeraro, Food Specialist e consulente HACCP · Aggiornata a {mese}</p></div></div><div class="filo"></div>'
                 f'<section class="sez bianca" style="border-top:0"><div class="wrap"><article class="prosa">{g["corpo"]}'
                 '<div class="nota"><p><strong>Nota.</strong> Questa guida è informativa e riassume le regole generali. Per i casi particolari fa fede la norma, e l\'ufficio a cui chiedere è la ASL del tuo territorio.</p></div></article></div></section>'
                 f'<section class="sez"><div class="wrap"><div class="testa"><p class="occhiello">Continua a leggere</p><h2>Altre guide</h2></div><div class="elenco-guide">{altre}</div></div></section>' + cta('../'))
        (RADICE / 'site/guide' / (g['slug'] + '.html')).write_text(pagina('guide/' + g['slug'] + '.html', g['titolo'], g['desc'], corpo, r='../', menu='guide/', schemi=schemi, articolo=True), encoding='utf-8')
    indice = ('<div class="wrap"><div class="capo"><p class="briciole"><a href="../">Filo Corto</a> / Guide</p><h1>Guide per chi vuole vendere alla ristorazione</h1>'
              '<p class="grande">Scritte per i piccoli produttori, da chi lavora in cucina da 25 anni. Niente giri di parole: cosa serve, in che ordine.</p></div></div>'
              '<section class="sez bianca"><div class="wrap"><div class="elenco-guide">' + ''.join(voce(*t) for t in tutte) + '</div>'
              + ('<p class="grande" style="margin-top:34px">Cerchi il tuo territorio? <a href="../territori/">Leggi le pagine sulle zone del Lazio →</a></p>' if (RADICE / 'src/territori').exists() and any((RADICE / 'src/territori').glob('*.html')) else '')
              + '</div></section>' + cta('../'))
    (RADICE / 'site/guide/index.html').write_text(pagina('guide/index.html', 'Guide per produttori: vendere a ristoranti e hotel | Filo Corto', 'Guide pratiche per piccoli produttori che vogliono vendere alla ristorazione: come proporsi, documenti e requisiti, listino, cosa chiede uno chef, prodotto per prodotto.', indice, r='../', menu='guide/'), encoding='utf-8')
    for p in (RADICE / 'src/pagine').glob('*.html'):
        d = leggi(p)
        schemi = [json.loads(d['schema'])] if d.get('schema') else []
        (RADICE / 'site' / (d['slug'] + '.html')).write_text(pagina(d['slug'] + '.html', d['titolo'], d['desc'], d['corpo'], menu=d.get('menu') or None, noindex=d.get('noindex') == 'si', schemi=schemi), encoding='utf-8')
    rete = produttori()
    zone = territori()
    oggi = datetime.date.today().isoformat()
    righe = [f'<url><loc>{URL}{u}</loc></url>' for u in PAGINE_FISSE] + [f'<url><loc>{URL}guide/{s}.html</loc></url>' for s, _, _ in STORICHE] + [f'<url><loc>{URL}guide/{g["slug"]}.html</loc><lastmod>{g["data"]}</lastmod></url>' for g in nuove]
    if zone:
        righe += [f'<url><loc>{URL}territori/</loc></url>'] + [f'<url><loc>{URL}territori/{d["slug"]}.html</loc><lastmod>{d["data"]}</lastmod></url>' for d in zone]
    if rete:
        righe += [f'<url><loc>{URL}produttori/</loc></url>'] + [f'<url><loc>{URL}produttori/{d["slug"]}.html</loc></url>' for d in rete]
    (RADICE / 'site/sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + '\n'.join(righe) + '\n</urlset>\n', encoding='utf-8')
    print(f'Costruite {len(nuove)} guide nuove, {len(tutte)} in indice, {len(zone)} territori, {len(rete)} produttori ({oggi}).')


if __name__ == '__main__':
    costruisci()
