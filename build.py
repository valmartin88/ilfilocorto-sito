#!/usr/bin/env python3
"""Filo Corto – genera le pagine del sito a partire dai testi in src/.

Uso: python3 build.py
- src/guide/<slug>.html  -> site/guide/<slug>.html (+ indice guide e sitemap)
- src/pagine/<nome>.html -> site/<nome>.html
Ogni file in src/ comincia con righe "chiave: valore", poi una riga "---", poi il corpo HTML.
La cartella site/ viene copiata sopra public_html dal server (vedi README).
"""
import json, pathlib, datetime

RADICE = pathlib.Path(__file__).parent
URL = 'https://ilfilocorto.it/'
CSS_V = '3'

# Guide pubblicate prima di questo sistema: i file restano sul server, qui servono per indice e sitemap.
STORICHE = [
    ('vendere-ai-ristoranti', 'Come vendere ai ristoranti: la guida per piccoli produttori', 'I passi concreti: prodotti, listino, documenti, campione, consegne, pagamenti.'),
    ('documenti-per-vendere-ai-ristoranti', 'Documenti e requisiti per vendere a ristoranti e hotel', 'Registrazione, autocontrollo, lotti, etichette, imballaggi, trasporto.'),
    ('cosa-chiede-uno-chef', 'Cosa chiede uno chef a un fornitore', 'Le tre domande di ogni cucina, viste da dentro.'),
    ('listino-per-ristoranti', 'Come preparare un listino per ristoranti', 'Cosa scriverci, in quale forma, con un esempio.'),
    ('filiera-corta-km-0', 'Filiera corta e chilometro zero: cosa dice la legge', 'Le definizioni della legge 61/2022, in parole semplici.'),
]
PAGINE_FISSE = ['', 'produttori.html', 'cucine.html', 'come-funziona.html', 'prova.html', 'riga-menu.html', 'check-up.html', 'guide/', 'domande.html', 'chi-siamo.html', 'privacy.html']

LOGO = '<svg width="46" height="46" viewBox="0 0 60 60" fill="none" aria-hidden="true"><circle cx="30" cy="38" r="17" stroke="#c9862b" stroke-width="6"/><circle cx="30" cy="38" r="5" fill="#1f2420"/><path d="M30 21 C 30 11, 37 5, 48 5 C 48 15, 41 21, 30 21 Z" fill="#2f5d3a"/></svg>'
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
              '<section class="sez bianca"><div class="wrap"><div class="elenco-guide">' + ''.join(voce(*t) for t in tutte) + '</div></div></section>' + cta('../'))
    (RADICE / 'site/guide/index.html').write_text(pagina('guide/index.html', 'Guide per produttori: vendere a ristoranti e hotel | Filo Corto', 'Guide pratiche per piccoli produttori che vogliono vendere alla ristorazione: come proporsi, documenti e requisiti, listino, cosa chiede uno chef, prodotto per prodotto.', indice, r='../', menu='guide/'), encoding='utf-8')
    for p in (RADICE / 'src/pagine').glob('*.html'):
        d = leggi(p)
        (RADICE / 'site' / (d['slug'] + '.html')).write_text(pagina(d['slug'] + '.html', d['titolo'], d['desc'], d['corpo'], menu=d.get('menu'), noindex=d.get('noindex') == 'si'), encoding='utf-8')
    oggi = datetime.date.today().isoformat()
    righe = [f'<url><loc>{URL}{u}</loc></url>' for u in PAGINE_FISSE] + [f'<url><loc>{URL}guide/{s}.html</loc></url>' for s, _, _ in STORICHE] + [f'<url><loc>{URL}guide/{g["slug"]}.html</loc><lastmod>{g["data"]}</lastmod></url>' for g in nuove]
    (RADICE / 'site/sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + '\n'.join(righe) + '\n</urlset>\n', encoding='utf-8')
    print(f'Costruite {len(nuove)} guide nuove, {len(tutte)} in indice ({oggi}).')


if __name__ == '__main__':
    costruisci()
