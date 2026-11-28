# Filo Corto – le pagine principali del sito. Questo file scrive src/pagine/*.html; lo esegue build.py.
# Per cambiare un testo: modificare qui, poi `python3 build.py`.
# Le pagine scheda.html e privacy.html sono scritte a mano in src/pagine/ e non passano da qui.
import pathlib, json, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import qr  # noqa: E402

P = pathlib.Path(__file__).resolve().parent.parent / 'src' / 'pagine'
SITO = 'https://ilfilocorto.it/'


def cerchio(x, y, R, cls=''):  # proporzioni identiche al cerchio del marchio (178/56/52)
    w = round(R * 56 / 178, 2)
    return (f'<g class="{cls}"><circle cx="{x}" cy="{y}" r="{round(R - w / 2, 2)}" fill="#F2F4F0" stroke="#E8692C" stroke-width="{w}"/>'
            f'<circle cx="{x}" cy="{y}" r="{round(R * 52 / 178, 2)}" fill="#12302B"/></g>')


ARTE = ('<svg class="arte" viewBox="0 0 440 440" role="img" aria-label="Dal campo alla cucina">'
        '<rect width="440" height="440" fill="#2f5d3a"/>'
        '<path class="onda" d="M-40 360 C 60 340, 150 380, 250 362 S 400 340, 480 352" stroke="#477a52" stroke-width="10" fill="none"/>'
        '<path class="onda o2" d="M-40 396 C 70 380, 170 410, 270 396 S 400 384, 480 390" stroke="#477a52" stroke-width="10" fill="none"/>'
        '<path d="M188 92 C 250 92, 300 140, 312 236" stroke="#e9b565" stroke-width="11" stroke-linecap="round" stroke-dasharray="0.1 24" fill="none"/>'
        '<g class="foglia"><path d="M44 196 C 44 120, 92 70, 176 66 C 176 146, 126 196, 44 196 Z" fill="#8fc49a" stroke="#1f2420" stroke-width="4"/>'
        '<path d="M58 184 L 160 84" stroke="#1f2420" stroke-width="4" stroke-linecap="round"/></g>'
        '<g transform="rotate(6 344 76)"><rect x="276" y="56" width="140" height="44" fill="#e9b565" stroke="#1f2420" stroke-width="4"/>'
        '<text x="346" y="86" text-anchor="middle" class="et">ITALIA</text></g>'
        + cerchio(330, 318, 74, 'bersaglio') +
        '<text x="44" y="246" class="lab">DAL CAMPO</text><text x="408" y="424" text-anchor="end" class="lab">ALLA CUCINA</text></svg>')

CERCHIONE = ('<svg class="cerchione" viewBox="0 0 200 200" aria-hidden="true"><path d="M100 62 C 100 30, 122 10, 158 10 C 158 42, 136 62, 100 62 Z" fill="#2f5d3a"/>'
             + cerchio(100, 128, 62) + '</svg>')


# Icone a linea (64x64), tratto inchiostro, accento arancione
def ico(corpo):
    return f'<svg class="ico" viewBox="0 0 64 64" fill="none" stroke="#1f2420" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{corpo}</svg>'


I = {
 'olio': ico('<path d="M27 8h10v8l4 6v30a4 4 0 0 1-4 4H27a4 4 0 0 1-4-4V22l4-6z"/><path d="M23 34h18" stroke="#E8692C"/><path d="M32 40c-3 4-3 7 0 8 3-1 3-4 0-8z" fill="#E8692C" stroke="#E8692C"/>'),
 'formaggio': ico('<path d="M8 40l28-22 20 12v14H8z"/><path d="M8 40h48"/><circle cx="22" cy="48" r="3" stroke="#E8692C"/><circle cx="40" cy="36" r="3" stroke="#E8692C"/>'),
 'conserve': ico('<rect x="16" y="20" width="32" height="36" rx="4"/><path d="M18 12h28v8H18z"/><path d="M22 36h20M22 44h14" stroke="#E8692C"/>'),
 'legumi': ico('<ellipse cx="22" cy="26" rx="8" ry="6"/><ellipse cx="42" cy="24" rx="8" ry="6"/><ellipse cx="32" cy="42" rx="8" ry="6"/><path d="M19 26h6M39 24h6M29 42h6" stroke="#E8692C"/>'),
 'miele': ico('<path d="M18 22h28l-2 32H20z"/><path d="M22 14h20v8H22z"/><path d="M32 30v10m-5-5h10" stroke="#E8692C"/>'),
 'vino': ico('<path d="M22 8h20v14a10 10 0 0 1-20 0z"/><path d="M32 32v18M24 56h16"/><path d="M23 16h18" stroke="#E8692C"/>'),
 'farine': ico('<path d="M32 56V14"/><path d="M32 22c-6-2-8-7-8-10 5 1 8 4 8 10zM32 22c6-2 8-7 8-10-5 1-8 4-8 10zM32 34c-6-2-8-7-8-10 5 1 8 4 8 10zM32 34c6-2 8-7 8-10-5 1-8 4-8 10zM32 46c-6-2-8-7-8-10 5 1 8 4 8 10zM32 46c6-2 8-7 8-10-5 1-8 4-8 10z" stroke="#E8692C"/>'),
 'salumi': ico('<path d="M14 40c0-14 12-26 26-26 6 0 10 4 10 10 0 14-12 26-26 26-6 0-10-4-10-10z"/><circle cx="28" cy="34" r="2.5" stroke="#E8692C"/><circle cx="38" cy="26" r="2.5" stroke="#E8692C"/><circle cx="34" cy="40" r="2.5" stroke="#E8692C"/>'),
 'occhio': ico('<path d="M6 32s10-16 26-16 26 16 26 16-10 16-26 16S6 32 6 32z"/><circle cx="32" cy="32" r="7" stroke="#E8692C"/>'),
 'bandiera': ico('<path d="M14 56V10"/><path d="M14 12h34l-6 9 6 9H14" /><path d="M14 30h34" stroke="#E8692C"/>'),
 'casa': ico('<path d="M10 30L32 12l22 18"/><path d="M16 26v28h32V26"/><path d="M27 54V40h10v14" stroke="#E8692C"/>'),
}

# Foto: i nomi e i formati sono quelli di site/foto.php. I file stanno in site/foto/<nome>-<formato>.jpg;
# dove il file manca, foto.php mostra un disegno del sito.
FORMATI = {'banda': (1600, 640), 'alto': (900, 1000), 'largo': (900, 600)}


def foto(f, alt, v='banda', cls='', testo='', r=''):
    w, h = FORMATI[v]
    if not (P.parent.parent / 'site' / 'foto' / f'{f}-{v}.jpg').exists():
        alt = ''   # finché la foto non c'è esce un disegno decorativo: nessuna descrizione
    t = f'<figcaption>{testo}</figcaption>' if testo else ''
    return f'<figure class="foto {cls}"><img src="{r}foto.php?f={f}&amp;v={v}" alt="{alt}" width="{w}" height="{h}" decoding="async">{t}</figure>'


def fascia_foto(f, alt):
    return '<div class="wrap">' + foto(f, alt, 'banda', 'larga') + '</div>'


MOSAICO = ('<div class="mosaico">' + foto('ulivo', 'Olive sul ramo dopo la pioggia', 'alto', 'a', 'La terra')
           + foto('mani', 'Mani di un contadino con patate appena raccolte', 'largo', 'b', 'Le mani')
           + foto('chef', 'Uno chef che impiatta', 'largo', 'c', 'La cucina') + '</div>')


def scrivi(slug, titolo, desc, corpo, menu='', extra=''):
    testa = f'titolo: {titolo}\ndesc: {desc}\n' + (f'menu: {menu}\n' if menu else '') + extra + '---\n'
    (P / f'{slug}.html').write_text(testa + corpo.strip() + '\n', encoding='utf-8')


def capo(briciola, h1, grande, bottoni=''):
    return (f'<div class="wrap"><div class="capo"><p class="briciole"><a href="./">Filo Corto</a> / {briciola}</p>'
            f'<h1>{h1}</h1><p class="grande">{grande}</p>{bottoni}</div></div>')


def btn(href, testo, cls='verde'):
    return f'<a class="btn {cls}" href="{href}">{testo} →</a>'


def sez(contenuto, cls='', occhiello='', h2='', ident=''):
    t = f'<div class="testa"><p class="occhiello">{occhiello}</p><h2>{h2}</h2></div>' if h2 else ''
    i = f' id="{ident}"' if ident else ''
    return f'<section class="sez {cls}"{i}><div class="wrap">{t}{contenuto}</div></section>'


def passi(*voci):
    return '<ol class="passi">' + ''.join(f'<li><b>{t}</b><span>{s}</span></li>' for t, s in voci) + '</ol>'


def punti(*voci):
    return '<ul class="punti">' + ''.join(f'<li>{v}</li>' for v in voci) + '</ul>'


def tessere(*voci, cls=''):
    return f'<div class="tessere {cls}">' + ''.join(f'<div class="tessera{" m" if m else ""}"><p class="domanda">{t}</p><p>{s}</p></div>' for t, s, m in voci) + '</div>'


def faq(*voci):
    return '<div class="faq">' + ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in voci) + '</div>'


def gettoni(*voci):
    return '<ul class="gettoni">' + ''.join(f'<li>{v}</li>' for v in voci) + '</ul>'


PATTI = gettoni('Adesione gratuita', 'Fatturi tu', 'Margine dichiarato', 'Nessuna vendita promessa', 'Solo materie prime italiane')

CTA = ('<section class="sez verde-b"><div class="wrap fascia"><h2>Produci in Italia? Partiamo dal Lazio.</h2>'
       + btn('produttori.html#candidati', 'Candidati in 2 minuti', 'miele') + '</div></section>')

NASTRO = ('<div class="nastro" aria-hidden="true"><div>' + ''.join(f'<span>{x}</span><i></i>' for x in
          ['Formaggi', 'Olio extravergine', 'Conserve', 'Legumi', 'Miele', 'Vino', 'Birra artigianale', 'Farine', 'Pasta secca', 'Salumi'] * 2) + '</div></div>')

FILI = ('<div class="fili"><div class="lungo"><h3>Filo lungo</h3><ol class="catena">'
        '<li class="f"><span>Produttore</span></li><li><span>Grossista</span></li><li><span>Piattaforma</span></li><li><span>Distributore</span></li><li class="f"><span>Cucina</span></li></ol></div>'
        '<div class="corto"><h3>Filo corto</h3><ol class="catena"><li><span>Produttore</span></li><li><span>Cucina</span></li></ol></div></div>')

# La pagina del produttore con il suo QR: qui un esempio dichiarato (il QR porta alla pagina «Produttori»).
PASSAPORTO = ('<div class="passaporto"><span class="es">Esempio</span><div class="sx"><p class="occhiello">Olio extravergine · Sabina</p><b>Azienda agricola Esempio</b>'
              '<dl><dt>Dove</dt><dd>Un paese della Sabina (RI)</dd><dt>Cosa</dt><dd>Olio extravergine, in latta e in bottiglia</dd>'
              '<dt>Quando</dt><dd>Olio nuovo da novembre</dd><dt>Consegne</dt><dd>Martedì e venerdì</dd></dl></div>'
              '<div class="dx">' + qr.svg(SITO + 'produttori.html') + '<span>Inquadra: ecco chi lo fa</span></div></div>')

DIVERSI = ('<div class="diversi">'
           '<div class="diverso"><h3>Entriamo in azienda</h3><p>Un check-up vero: una visita, una lista uguale per tutti, un rapporto scritto.</p><a class="et" href="check-up.html">Il check-up →</a></div>'
           '<div class="diverso"><h3>Il prodotto ha un nome</h3><p>Ogni produttore ha la sua pagina e il suo QR. Dal campo al menu.</p><a class="et" href="#nome">La pagina del produttore →</a></div>'
           '<div class="diverso"><h3>Parliamo da cucina</h3><p>Listino, lotti, allergeni, giorni di consegna: scritti come servono a chi ordina ogni giorno.</p><a class="et" href="cucine.html">Per le cucine →</a></div></div>')


STAGIONI = [
 ('12,1,2', 'Inverno', [('Puntarelle', 'Il simbolo dell\'inverno romano.'), ('Broccolo romanesco', 'Cime verdi, sapore deciso.'), ('Olio nuovo', 'L\'olio dell\'ultima raccolta.'), ('Legumi secchi', 'Lenticchie, ceci, fagioli.')]),
 ('3,4,5', 'Primavera', [('Carciofo romanesco', 'IGP del Lazio.'), ('Fave', 'Con il pecorino, a maggio.'), ('Asparagi', 'Verdi e selvatici.'), ('Abbacchio', 'Abbacchio Romano IGP.')]),
 ('6,7,8', 'Estate', [('Pomodori', 'Da sugo e da insalata.'), ('Zucchine romanesche', 'Con il fiore.'), ('Miele', 'Millefiori e di castagno.'), ('Peperoni', 'Per conserve e forno.')]),
 ('9,10,11', 'Autunno', [('Olio nuovo', 'Il frantoio riparte.'), ('Castagne', 'Dai Cimini e dalla Ciociaria.'), ('Nocciole', 'Tonda gentile romana.'), ('Broccolo romanesco', 'Arriva con il freddo.')]),
]


def stagione():
    blocchi = ''
    for mesi, nome, voci in STAGIONI:
        carte = ''.join(f'<div class="carta-s"><span class="pallino"></span><b>{t}</b><span>{d}</span></div>' for t, d in voci)
        blocchi += f'<div class="stag" data-mesi="{mesi}" hidden><p class="nome-s">{nome} nel Lazio</p><div class="carte-s">{carte}</div></div>'
    js = ('<script>(function(){var m=new Date().getMonth()+1;document.querySelectorAll(".stag").forEach(function(b){'
          'if(b.dataset.mesi.split(",").indexOf(String(m))>-1)b.hidden=false})})();</script>')
    return blocchi + js


# ---------------- HOME ----------------
home = (
 '<div class="wrap"><div class="eroe"><div class="testo"><p class="occhiello">Rete in costruzione · si parte dal Lazio</p>'
 '<h1>Il prodotto vero,<br><em>dal campo<br>alla cucina.</em></h1>'
 '<p class="grande">Gli chef chiedono: «Cosa hanno i produttori?» I produttori chiedono: «Cosa vogliono gli chef?» Filo Corto mette insieme le due risposte.</p>'
 '<div class="btns">' + btn('produttori.html', 'Sono un produttore') + btn('cucine.html', 'Ho una cucina', '') + '</div>'
 '<ul class="fiducia"><li>Solo materie prime italiane</li><li>Fattura diretta</li><li>Adesione gratuita</li></ul></div>'
 + ARTE + '</div></div>' + NASTRO
 + sez('<div class="due-porte">'
       '<a class="porta2" href="produttori.html"><p class="occhiello">Se produci</p><h2>Fatti trovare da chi ti cerca da una vita.</h2><p>Chef, ristoratori, hotel. E chiunque cerchi il prodotto vero. Una pagina tua, gratis.</p><span class="vai">Entra nella rete →</span></a>'
       '<a class="porta2 v" href="cucine.html"><p class="occhiello">Se cucini</p><h2>Prodotti veri, regole da cucina.</h2><p>Campione prima di ordinare. Prezzi, consegne e quantità per iscritto.</p><span class="vai">Chiedi un campione →</span></a>'
       '</div>', cls='bianca')
 + sez(MOSAICO)
 + sez('<p class="occhiello">Perché esistiamo</p><div class="manifesto"><p>Migliaia di piccoli produttori fanno cose straordinarie.<br><em>E nessuno li vede.</em></p><p>Il made in Italy vive solo se arriva in tavola.</p></div>'
       '<div class="pilastri">'
       f'<div>{I["occhio"]}<h3>Visibili</h3><p>Ogni produttore con nome, luogo e una pagina sua.</p></div>'
       f'<div>{I["bandiera"]}<h3>Italiani</h3><p>Solo materie prime italiane. Niente import, né UE né extra UE.</p></div>'
       f'<div>{I["casa"]}<h3>Vicini</h3><p>Dal territorio alle sue cucine. Si parte dal Lazio.</p></div></div>',
       cls='scura')
 + sez(FILI, cls='bianca', occhiello='La differenza', h2='Meno passaggi, più valore')
 + sez(DIVERSI, occhiello='Il nostro metodo', h2='Prima la visita, poi la vetrina')
 + sez('<div class="due" style="align-items:center"><div class="testa" style="margin:0"><p class="occhiello">Il nome in tavola</p><h2>Chi mangia scopre chi l\'ha fatto.</h2>'
       '<p class="grande">La cucina mette il QR nel menu. Chi inquadra trova il produttore: chi è, dov\'è, cosa fa.</p>'
       '<p class="piccolo" style="margin-top:14px">Le prime pagine escono con i primi produttori.</p></div>' + PASSAPORTO + '</div>', cls='bianca', ident='nome')
 + '<!--RETE-->'
 + sez(stagione() + '<p class="piccolo" style="margin-top:18px">Cosa offre la terra in questo periodo. Il listino della rete arriverà con i primi produttori.</p>',
       occhiello='In stagione ora', h2='Il calendario delle nostre terre')
 + sez('<div class="passi-h">'
       '<div><i>1</i><b>Il produttore si candida</b><span>Due minuti, poi scheda e check-up.</span></div>'
       '<div><i>2</i><b>La cucina assaggia</b><span>Il campione è gratis.</span></div>'
       '<div><i>3</i><b>Ordine e fattura diretta</b><span>Dal produttore alla cucina.</span></div></div>' + PATTI,
       cls='bianca', occhiello='Come funziona', h2='Tre passi, patti chiari')
 + sez('<div class="cat">' + ''.join(f'<div>{I[k]}<span>{n}</span></div>' for k, n in [('formaggio', 'Formaggi'), ('olio', 'Olio'), ('conserve', 'Conserve'), ('legumi', 'Legumi e cereali'), ('miele', 'Miele'), ('vino', 'Vino e birra'), ('farine', 'Farine e pasta'), ('salumi', 'Salumi')]) + '</div>'
       + '<p style="margin-top:26px">' + btn('produttori.html#candidati', 'Produci uno di questi? Candidati') + '</p>', occhiello='Chi cerchiamo', h2='Per cominciare: prodotti che viaggiano bene')
 + sez('<div class="tappe"><div class="ora"><b>Oggi</b><span>Raccogliamo le adesioni</span></div><div><b>Poi</b><span>Check-up e prime pagine dei produttori</span></div><div><b>Infine</b><span>Ordini dalle cucine</span></div></div>'
       '<p class="piccolo" style="margin-top:16px">Nessun prodotto è ancora in vendita.</p>', cls='bianca', occhiello='A che punto siamo', h2='Rete in costruzione')
 + sez('<div class="elenco-guide"><!--ULTIME--></div>'
       '<div class="etichette"><a href="guide/">Tutte le guide →</a><a href="territori/">I territori del Lazio →</a><!--CUCINE--></div>', occhiello='Gratis', h2='Da leggere: le ultime uscite')
 + CTA)
scrivi('index', 'Filo Corto | Piccoli produttori italiani per ristoranti, bar e hotel',
       'Filo Corto dà visibilità ai piccoli produttori e porta il prodotto vero delle nostre terre in ristoranti, bar e hotel. Solo materie prime italiane. Si parte dal Lazio.', home,
       extra='schema: ' + json.dumps({'@context': 'https://schema.org', '@type': 'WebSite', 'name': 'Filo Corto', 'url': SITO, 'inLanguage': 'it'}, ensure_ascii=False) + '\n')

# ---------------- PRODUTTORI ----------------
prod = (capo('Produttori', 'Fai un prodotto vero? <em>Fatti trovare.</em>',
             'C\'è chi ti cerca da una vita: chef, ristoratori, hotel, appassionati. Ti diamo una vetrina dove trovarti. Gratis.',
             '<div class="btns" style="margin-top:8px">' + btn('#candidati', 'Candidati') + btn('prova.html', 'Sei pronto? Fai la prova', '') + '</div>')
 + fascia_foto('cassette', 'Verdure in cassette di legno al mercato')
 + sez('<div class="due"><div class="riquadro"><h3>Ti diamo</h3>' + punti('Una pagina tutta tua, visibile a tutti', 'Il listino davanti alle cucine', 'Il check-up gratis (per i primi)', 'Un solo interlocutore') +
       '</div><div class="riquadro m"><h3>Ti chiediamo</h3>' + punti('Materie prime italiane', 'Giorni di consegna fissi', 'Prezzi e quantità per iscritto', 'Documenti e lotti in ordine') + '</div></div>' + PATTI, cls='bianca')
 + sez('<div class="due" style="align-items:center"><div class="testa" style="margin:0"><p class="occhiello">La tua vetrina</p><h2>Una pagina tua. Un QR tuo.</h2>'
       '<p class="grande">Chi sei, cosa fai, dove sei. E un QR da mettere su etichette, cassette e menu.</p>'
       + gettoni('La scriviamo insieme', 'Esce dopo il check-up', 'Solo se la approvi', 'La togli quando vuoi') + '</div>' + PASSAPORTO + '</div>')
 + sez(passi(('Ti candidi', '2 minuti, qui sotto.'), ('Scheda e check-up', 'Prodotti, prezzi, consegne. Poi la visita.'), ('Entri nel listino', 'E hai la tua pagina.')), cls='scura', occhiello='Come si entra', h2='Tre passi')
 + sez('<div class="due"><div><p class="grande">Ti rispondiamo per email con la scheda di adesione.</p><p style="margin-top:12px">Oppure scrivi a <a href="mailto:info@ilfilocorto.it">info@ilfilocorto.it</a></p></div>'
   '<div class="modulo"><form class="form" action="invia.php" method="post"><input type="hidden" name="tipo" value="produttore">'
   '<div class="hp" aria-hidden="true"><label>Lascia vuoto<input type="text" name="sito_web" tabindex="-1" autocomplete="off"></label></div>'
   '<label>Azienda<input type="text" name="azienda" required maxlength="120" autocomplete="organization"></label>'
   '<label>Referente<input type="text" name="referente" required maxlength="120" autocomplete="name"></label>'
   '<label>Email<input type="email" name="email" required maxlength="160" autocomplete="email"></label>'
   '<label>Comune<input type="text" name="comune" required maxlength="120"></label>'
   '<label class="full">Cosa produci<textarea name="prodotti" rows="3" required maxlength="2000" placeholder="Es. pecorino stagionato, ricotta"></textarea></label>'
   '<label class="full">Come consegni oggi<select name="consegna"><option>Consegno io, con mezzo mio</option><option>Uso un corriere</option><option>Vendo solo in azienda o al mercato</option></select></label>'
   '<label class="full check"><input type="checkbox" name="consenso" value="si" required><span>Aderire è gratuito, non mi impegna e non promette vendite. Ho letto l\'<a href="privacy.html">informativa privacy</a>.</span></label>'
   '<button class="btn verde full" type="submit">Invia la candidatura →</button></form></div></div>', cls='verde-b', occhiello='Candidatura', h2='Candidati alla rete', ident='candidati')
 + sez(faq(('Quanto costa?', 'Niente. Esci quando vuoi.'),
           ('Mi garantite vendite?', 'No. Scelgono le cucine: noi ti presentiamo bene.'),
           ('Come guadagnate?', 'Con un margine sulle vendite, scritto prima di ogni ordine.'),
           ('Il check-up è una certificazione?', 'No. È una valutazione per la rete. Non sostituisce i controlli ufficiali.')) +
       '<div class="etichette"><a href="domande.html">Tutte le domande →</a><a href="guide/">Le guide →</a></div>', occhiello='Domande', h2='In breve'))
scrivi('produttori', 'Vendere ai ristoranti: la rete dei piccoli produttori | Filo Corto',
       'Sei un piccolo produttore? Con Filo Corto ti fai trovare da ristoranti, bar e hotel: una pagina tua con il tuo QR, check-up gratuito per i primi. Si parte dal Lazio.', prod, menu='produttori.html')

# ---------------- CUCINE ----------------
cuc = (capo('Cucine', 'Prodotti veri per la <em>tua cucina.</em>',
            'Da piccoli produttori, con materie prime italiane. E con le regole che servono a una cucina.',
            '<div class="btns" style="margin-top:8px">' + btn('#richiesta', 'Chiedi un campione') + '</div>')
 + fascia_foto('chef', 'Uno chef che impiatta')
 + sez(tessere(('Quando arriva?', 'Giorni e orari d\'ordine scritti.', False),
               ('Quanto costa?', 'Listino unico, al kg o al pezzo.', True),
               ('Ci sarà sempre?', 'Quantità settimanale scritta.', False), cls='tre')
       + gettoni('Solo materie prime italiane', 'Campione gratis', 'Fattura diretta del produttore', 'Accanto al tuo distributore'),
       cls='bianca', occhiello='Le tue tre domande', h2='Tre risposte scritte')
 + sez('<div class="due" style="align-items:center"><div class="testa" style="margin:0"><p class="occhiello">Sul menu</p><h2>Racconta chi c\'è dietro il piatto.</h2>'
       '<p class="grande">Una riga con nome e luogo del produttore. Per i produttori della rete, anche il QR della loro pagina.</p>'
       '<p style="margin-top:22px">' + btn('riga-menu.html', 'Scrivi la riga per il menu', '') + '</p></div>'
       '<div class="carta-menu"><b>Sul menu</b><p>Tonnarelli cacio e pepe</p><small>Pecorino: Azienda agricola Esempio, Sabina (RI)</small></div></div>')
 + sez(passi(('Dicci cosa cerchi', 'Con il modulo qui sotto.'), ('Assaggi', 'Il campione è gratis.'), ('Ordini', 'Ogni produttore consegna e fattura.')), cls='scura', occhiello='Come funziona', h2='Tre passi')
 + sez('<div class="due"><div><p class="grande">Nessun prodotto è ancora in vendita: raccogliamo le richieste e ti scriviamo quando c\'è un produttore pronto per te.</p></div>'
   '<div class="modulo"><form class="form" action="invia.php" method="post">'
   '<div class="hp" aria-hidden="true"><label>Lascia vuoto<input type="text" name="sito_web" tabindex="-1" autocomplete="off"></label></div>'
   '<fieldset class="full radio"><legend>Vorrei</legend><label><input type="radio" name="tipo" value="campione" checked> un campione</label><label><input type="radio" name="tipo" value="ordine"> ordinare</label></fieldset>'
   '<label>Locale<input type="text" name="nome_locale" required maxlength="120"></label>'
   '<label>Tipo<select name="tipo_locale"><option>Ristorante</option><option>Bar</option><option>Hotel</option><option>Altro</option></select></label>'
   '<label>Referente<input type="text" name="referente" required maxlength="120" autocomplete="name"></label>'
   '<label>Email<input type="email" name="email" required maxlength="160" autocomplete="email"></label>'
   '<label class="full">Prodotti che cerchi<textarea name="prodotti" rows="3" required maxlength="2000" placeholder="Es. olio in latta, pecorino, legumi"></textarea></label>'
   '<label class="full">Zona di consegna<input type="text" name="zona" required maxlength="160" placeholder="Es. Roma, Trastevere"></label>'
   '<label class="full check"><input type="checkbox" name="consenso" value="si" required><span>Ho letto l\'<a href="privacy.html">informativa privacy</a>.</span></label>'
   '<button class="btn verde full" type="submit">Invia la richiesta →</button></form></div></div>', cls='verde-b', occhiello='Richiesta', h2='Dicci cosa ti serve', ident='richiesta')
 + sez(faq(('Posso già ordinare?', 'Non ancora: ti scriviamo quando c\'è un produttore pronto nella tua zona.'),
           ('Devo lasciare il mio distributore?', 'No. Ti diamo quello che lui non ha.'),
           ('Come si paga?', 'A fattura, al produttore.'),
           ('Vendete ai privati?', 'La vetrina dei produttori è aperta a tutti. Gli ordini, per ora, sono per ristoranti, bar e hotel.'))
       + '<div class="etichette"><a href="riga-menu.html">La riga per il menu →</a><!--CUCINE--></div>', occhiello='Domande', h2='In breve'))
scrivi('cucine', 'Prodotti italiani per ristoranti, bar e hotel | Filo Corto',
       'Formaggi, olio, conserve, legumi e miele da piccoli produttori, con materie prime italiane, per ristoranti, bar e hotel. Campione gratis, prezzi e consegne per iscritto.', cuc, menu='cucine.html')

# ---------------- CHECK-UP ----------------
chk = (capo('Check-up', 'Sei pronto <em>per le cucine?</em>',
            'Una visita, una lista uguale per tutti, un rapporto scritto. Gratis per i primi produttori.',
            '<div class="btns" style="margin-top:8px">' + btn('produttori.html#candidati', 'Candidati') + btn('prova.html', 'Intanto, fai la prova', '') + '</div>')
 + fascia_foto('barattoli', 'Barattoli di conserve su uno scaffale')
 + sez(tessere(('Documenti', 'Registrazione, autocontrollo, registri, formazione.', False),
               ('Prodotto', 'Origine delle materie prime, lotti, etichette, allergeni.', True),
               ('Consegne e prezzi', 'Trasporto, tempi, listino, quantità.', False), cls='tre'),
       cls='bianca', occhiello='Cosa guardiamo', h2='Tre aree, 14 punti')
 + sez(passi(('La visita', 'In azienda, con la lista.'), ('La prova del lotto', 'Da un prodotto venduto, carte alla mano, fino alle materie prime.'), ('Il rapporto', 'Esito: pronto, quasi pronto, da preparare.'), ('La pagina', 'Se vuoi, con il tuo QR.')), cls='scura', occhiello='Come funziona', h2='Quattro passi')
 + sez('<p class="grande">Ristoranti e hotel devono qualificare i fornitori nel loro piano HACCP: il check-up ti prepara a questo. Lo fa Valerio Semeraro, Food Specialist e consulente HACCP.</p>'
       + gettoni('Non è una certificazione', 'Non sostituisce i controlli ufficiali', 'Non garantisce vendite'), occhiello='Perché serve', h2='Patti chiari')
 + CTA)
scrivi('check-up', 'Check-up per piccoli produttori: pronto per ristoranti e hotel? | Filo Corto',
       'Visita in azienda, lista uguale per tutti, rapporto scritto: documenti, origine, lotti, etichette, consegne. Gratis per i primi produttori.', chk, menu='check-up.html')

# ---------------- COME FUNZIONA ----------------
cf = (capo('Come funziona', 'Chi produce, chi cucina. <em>Niente in mezzo.</em>',
           'Niente magazzino, niente rivendita. Mettiamo in contatto chi produce e chi cucina, con le stesse regole per tutti.')
 + fascia_foto('mercato', 'Il banco di un mercato rionale a Roma')
 + sez('<div class="due"><div class="riquadro"><h3>Se produci</h3>' + passi(('Ti candidi', '2 minuti.'), ('Scheda e check-up', 'Poi la visita.'), ('Entri nel listino', 'E hai la tua pagina.')) +
       '</div><div class="riquadro m"><h3>Se cucini</h3>' + passi(('Scegli', 'Dal listino.'), ('Assaggi', 'Campione gratis.'), ('Ordini', 'Fattura diretta.')) + '</div></div>', cls='bianca')
 + sez(FILI, occhiello='La differenza', h2='Meno passaggi, più valore')
 + sez(PATTI + '<p class="grande" style="margin-top:28px">Consegne: le definiamo con i primi produttori. L\'obiettivo è una consegna unica in giorni fissi.</p>'
       '<p class="piccolo" style="margin-top:12px">Non siamo un e-commerce per privati, né un grossista, né un ente di certificazione.</p>', cls='scura', occhiello='Le regole', h2='Uguali per tutti')
 + CTA)
scrivi('come-funziona', 'Come funziona Filo Corto | Filo Corto',
       'Il produttore si candida e fa il check-up, la cucina assaggia e ordina, il produttore consegna e fattura. Regole uguali per tutti, solo materie prime italiane.', cf, menu='come-funziona.html')

# ---------------- CHI SIAMO ----------------
cs = (capo('Chi siamo', 'Appassionati <em>del cibo vero.</em>',
           'Veniamo dalle cucine. Vogliamo che il prodotto delle nostre terre torni nei piatti.')
 + fascia_foto('olive', 'Olive verdi sul ramo')
 + sez('<div class="manifesto"><p>Da una parte ottimi piccoli produttori. Dall\'altra cucine che comprano solo dai grandi distributori.<br><em>Filo Corto accorcia questa distanza.</em></p>'
       '<p>Tra chi produce e chi cucina, oggi, ci sono troppi passaggi. Noi ne lasciamo uno.</p></div>'
       + tessere(('Si sa chi lo fa', 'Nome e indirizzo.', False), ('È italiano', 'Materie prime italiane.', True),
                 ('Si racconta', 'Una storia vera, per il menu.', False), ('È in regola', 'Documenti e lotti.', True)), cls='scura', occhiello='Cibo vero', h2='Cosa intendiamo')
 + sez('<p class="grande">Valerio Semeraro, Food Specialist e consulente HACCP, segue le adesioni e fa i check-up. <a href="mailto:info@ilfilocorto.it">info@ilfilocorto.it</a></p>', cls='bianca', occhiello='Chi cura il progetto', h2='Valerio Semeraro')
 + CTA)
scrivi('chi-siamo', 'Chi siamo: appassionati del cibo vero | Filo Corto',
       'Filo Corto nasce dalle cucine: appassionati del cibo vero che vogliono riportare il prodotto delle nostre terre in ristoranti, bar e hotel.', cs, menu='chi-siamo.html')

# ---------------- PER CONSORZI E TERRITORI ----------------
enti = (capo('Per i territori', 'Portiamo i vostri produttori <em>nelle cucine.</em>',
             'Consorzi, GAL, biodistretti, comuni, mercati contadini: se rappresentate piccoli produttori, possiamo lavorare insieme. Senza costi.',
             '<div class="btns" style="margin-top:8px"><a class="btn verde" href="mailto:info@ilfilocorto.it?subject=Filo%20Corto%20e%20il%20nostro%20territorio">Scriveteci →</a></div>')
 + fascia_foto('civita', 'Civita di Bagnoregio, in provincia di Viterbo')
 + sez('<div class="due"><div class="riquadro"><h3>Cosa mettiamo noi</h3>' + punti('Una pagina per ogni produttore, con il suo QR', 'Il check-up in azienda, gratuito per i primi produttori', '<a href="territori/">Una pagina dedicata al territorio</a>', '<a href="guide/">Guide gratuite</a> per vendere alla ristorazione') +
       '</div><div class="riquadro m"><h3>Cosa chiediamo</h3>' + punti('Far conoscere la rete ai vostri produttori', 'Dirci quali prodotti raccontano il territorio', 'Nessun contributo economico') + '</div></div>'
       + gettoni('Nessun costo', 'Fattura diretta del produttore', 'Nessuna vendita promessa', 'Solo materie prime italiane'), cls='bianca')
 + sez('<div class="tappe"><div class="ora"><b>Oggi</b><span>Raccogliamo le adesioni nel Lazio</span></div><div><b>Cerchiamo</b><span>Un primo territorio con cui partire</span></div><div><b>Poi</b><span>Check-up, pagine dei produttori, cucine</span></div></div>'
       '<p class="piccolo" style="margin-top:16px">Siamo all\'inizio e lo diciamo. Nessun prodotto è ancora in vendita.</p>', occhiello='A che punto siamo', h2='Un territorio per cominciare')
 + sez('<div class="fascia"><h2>Parliamone.</h2><a class="btn miele" href="mailto:info@ilfilocorto.it?subject=Filo%20Corto%20e%20il%20nostro%20territorio">info@ilfilocorto.it →</a></div>', cls='verde-b'))
scrivi('enti', 'Per consorzi, GAL e territori del Lazio | Filo Corto',
       'Consorzi, GAL, biodistretti, comuni e mercati contadini: Filo Corto porta i piccoli produttori del territorio nelle cucine di ristoranti, bar e hotel. Senza costi.', enti)

# ---------------- DOMANDE ----------------
FP = [('Aderire costa?', 'No. Gratis, senza impegno. Esci quando vuoi.'),
      ('Mi garantite vendite?', 'No. Scelgono le cucine.'),
      ('Quanto guadagna Filo Corto?', 'Un margine sulle vendite, scritto nella scheda prima di ogni ordine e dichiarato anche alle cucine.'),
      ('Chi fattura?', 'Tu, il produttore. La cucina paga te.'),
      ('Devo consegnare io?', 'Lo decidiamo con i primi produttori. L\'obiettivo è una consegna unica.'),
      ('Cos\'è il check-up?', 'Una visita con una lista uguale per tutti: documenti, origine, lotti, etichette, consegne. Gratis per i primi. Non è una certificazione.'),
      ('Cos\'è la pagina con il QR?', 'Ogni produttore della rete può avere una pagina sul sito e un QR che porta lì: si mette su etichette, cassette e menu. Esce dopo il check-up e solo se la approvi.'),
      ('Materie prime estere?', 'No. Solo materie prime coltivate o allevate in Italia, niente import UE o extra UE. Lo guardiamo al check-up.'),
      ('Produco fuori dal Lazio.', 'Partiamo dal Lazio. Scrivici lo stesso: ti ricontattiamo quando la rete si allarga.'),
      ('Quali prodotti cercate?', 'Per iniziare, quelli che si conservano: formaggi stagionati, olio, conserve, legumi, miele, vino e birra, farine, pasta, salumi.')]
FC = [('Posso già ordinare?', 'Non ancora: chiedi un campione e ti scriviamo quando c\'è un produttore pronto.'),
      ('Da dove vengono i prodotti?', 'Da piccoli produttori, con materie prime italiane. Su ogni prodotto: chi e dove.'),
      ('Devo lasciare il distributore?', 'No. Ti diamo quello che lui non ha.'),
      ('Come si paga?', 'A fattura, al produttore.'),
      ('Posso scrivere il produttore nel menu?', 'Sì: c\'è uno strumento gratuito per la riga del menu. Per i produttori della rete puoi aggiungere il QR della loro pagina.'),
      ('Vendete ai privati?', 'La vetrina dei produttori è aperta a tutti. Gli ordini, per ora, sono per ristoranti, bar e hotel.')]
dom = (capo('Domande', 'Domande <em>frequenti.</em>', 'Risposte brevi.')
 + sez(faq(*FP), cls='bianca', occhiello='Se produci', h2='Produttori')
 + sez(faq(*FC), occhiello='Se cucini', h2='Cucine') + CTA)
faqjson = json.dumps({'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in FP + FC]}, ensure_ascii=False)
scrivi('domande', 'Domande frequenti: produttori e cucine | Filo Corto',
       'Quanto costa aderire, chi fattura, cos\'è il check-up, materie prime italiane, si può già ordinare: le risposte brevi per produttori e cucine.', dom, extra=f'schema: {faqjson}\n')

# ---------------- LA PROVA (dieci domande) ----------------
# Ogni voce: domanda, titolo della cosa da sistemare, cosa fare, guida da leggere (facoltativa).
PROVA = [
 ('La tua attività è registrata presso l\'autorità sanitaria?', 'Registrazione sanitaria', 'È il primo documento che una cucina può chiederti. Si chiede con una notifica allo sportello unico (SUAP) del tuo Comune.', 'guide/documenti-per-vendere-ai-ristoranti.html'),
 ('Hai un piano di autocontrollo scritto e aggiornato?', 'Autocontrollo', 'Se trasformi, serve un piano scritto basato sui principi HACCP. Se fai solo produzione primaria, tieni in ordine registri e buone pratiche.', 'guide/haccp-piccoli-produttori.html'),
 ('Ogni confezione ha un lotto, e sai a chi l\'hai venduta?', 'Lotti e rintracciabilità', 'Un numero di lotto su ogni confezione e un registro delle vendite: se c\'è un problema, ritiri solo quello.', ''),
 ('Le tue etichette sono complete, con gli allergeni in evidenza?', 'Etichette', 'Le voci principali: nome del prodotto, ingredienti con allergeni evidenziati, quantità, scadenza, lotto, il tuo nome e indirizzo.', 'guide/documenti-per-vendere-ai-ristoranti.html'),
 ('Le tue materie prime sono coltivate o allevate in Italia?', 'Origine italiana', 'Nella rete entrano solo prodotti fatti con materie prime italiane. Tieni fatture e documenti dei tuoi fornitori.', ''),
 ('Hai un listino per la ristorazione, con prezzi senza IVA?', 'Listino', 'Una pagina: prodotto, formato da cucina, prezzo senza IVA, ordine minimo, fino a quando vale.', 'guide/listino-per-ristoranti.html'),
 ('Puoi consegnare in giorni fissi, ogni settimana?', 'Consegne', 'Scegli uno o due giorni fissi e un orario limite per gli ordini. Per una cucina la puntualità vale quanto il prodotto.', 'guide/cosa-chiede-uno-chef.html'),
 ('Sai quanta merce puoi garantire ogni settimana?', 'Quantità', 'Scrivi una quantità settimanale che puoi mantenere. Meglio poca e sicura.', ''),
 ('Puoi lasciare un campione gratuito a una cucina?', 'Campione', 'Lo chef decide assaggiando. Prepara un formato piccolo da lasciare, con la scheda del prodotto.', ''),
 ('Hai deciso come farti pagare: fattura e tempi?', 'Pagamenti', 'Scrivi nel listino i tempi di pagamento e le coordinate. Patti chiari dal primo ordine.', 'guide/vendere-ai-ristoranti.html'),
]
FRASI = ['Hai le carte in regola per presentarti. Candidati: il prossimo passo è la scheda di adesione.',
         'Ti manca poco. Sistema i punti qui sotto e candidati: il check-up serve anche a questo.',
         'C\'è da lavorare, ed è normale. Parti dai punti qui sotto: sono in ordine di importanza.']
prova_js = ('<script>(function(){var D=' + json.dumps([list(v) for v in PROVA], ensure_ascii=False) + ',F=' + json.dumps(FRASI, ensure_ascii=False) + ';'
 'var n=0,r=[],el=function(i){return document.getElementById(i)},P=el("prova"),E=el("esito");'
 'function disegna(){var h="";for(var i=0;i<D.length;i++)h+=\'<i class="\'+(i<n?"f":i===n?"o":"")+\'"></i>\';'
 'el("pallini").innerHTML=h+"<span>"+(n+1)+" di "+D.length+"</span>";el("q").textContent=D[n][0];el("indietro").hidden=n===0}'
 'function fine(){var tot=0,h="",i;for(i=0;i<r.length;i++)tot+=r[i];var liv=tot>=16?0:tot>=10?1:2;'
 'el("punti").textContent=tot;el("livello").textContent=["Pronto","Quasi pronto","Da preparare"][liv];el("frase").textContent=F[liv];'
 'for(i=0;i<D.length;i++)if(r[i]<2)h+="<li><b>"+D[i][1]+"</b><span>"+D[i][2]+(D[i][3]?\' <a href="\'+D[i][3]+\'">Leggi la guida →</a>\':"")+"</span></li>";'
 'el("fare").innerHTML=h;el("blocco-fare").hidden=!h;P.hidden=true;E.hidden=false;setTimeout(function(){el("barra").style.width=(tot*5)+"%"},80);E.focus()}'
 'P.querySelectorAll(".risposte button").forEach(function(b){b.addEventListener("click",function(){r[n]=+b.getAttribute("data-p");n++;if(n<D.length)disegna();else fine()})});'
 'el("indietro").addEventListener("click",function(){if(n>0){n--;disegna()}});'
 'el("rifai").addEventListener("click",function(){n=0;r=[];E.hidden=true;P.hidden=false;el("barra").style.width="0";disegna();P.scrollIntoView({block:"center"})});'
 'P.hidden=false;disegna()})();</script>')
prova = (capo('<a href="produttori.html">Produttori</a> / La prova', 'Dieci domande, <em>due minuti.</em>',
              'Scopri se sei pronto per vendere a ristoranti e hotel. Nessuna registrazione: le risposte restano sul tuo dispositivo.')
 + '<section class="sez bianca stretta"><div class="wrap">'
   '<div class="prova" id="prova" hidden><div class="pallini" id="pallini" aria-hidden="true"></div><p class="q" id="q" aria-live="polite"></p>'
   '<div class="risposte"><button type="button" class="si" data-p="2">Sì</button><button type="button" data-p="1">In parte</button><button type="button" data-p="0">No</button></div>'
   '<button type="button" class="indietro" id="indietro" hidden>← Domanda precedente</button></div>'
   '<div class="esito" id="esito" hidden tabindex="-1"><p class="occhiello" style="margin:0">Il tuo risultato</p>'
   '<div class="punteggio"><span class="cifra-g"><span id="punti">0</span><small>/20</small></span><span class="livello" id="livello"></span></div>'
   '<div class="barra-p"><i id="barra"></i></div><p class="grande" id="frase"></p>'
   '<div id="blocco-fare"><h3 style="margin-bottom:14px">Da sistemare, in ordine</h3><ul class="da-fare" id="fare"></ul></div>'
   '<div class="btns">' + btn('produttori.html#candidati', 'Candidati alla rete') + '<button type="button" class="btn" id="rifai">Rifai la prova</button></div>'
   '<p class="piccolo">Questa prova è un orientamento: non è il check-up e non è una certificazione. Le risposte non vengono inviate a nessuno.</p></div>'
   '<noscript><p class="grande">Per fare la prova serve JavaScript. In alternativa leggi la guida <a href="guide/documenti-per-vendere-ai-ristoranti.html">Documenti e requisiti</a>.</p></noscript>'
   '</div></section>' + prova_js
 + sez(tessere(('Documenti', 'Registrazione, autocontrollo, lotti, etichette.', False), ('Prodotto', 'Origine italiana, listino, campione.', True), ('Servizio', 'Consegne, quantità, pagamenti.', False), cls='tre')
       + '<div class="etichette"><a href="check-up.html">Il check-up in azienda →</a><a href="guide/">Le guide →</a></div>', occhiello='Cosa misura', h2='Le stesse cose che guarda una cucina')
 + CTA)
scrivi('prova', 'Sei pronto per vendere ai ristoranti? La prova in 10 domande | Filo Corto',
       'Dieci domande per i piccoli produttori: documenti, lotti, etichette, listino, consegne. In due minuti sai cosa ti manca per vendere a ristoranti e hotel.', prova, menu='produttori.html')

# ---------------- LA RIGA PER IL MENU ----------------
riga_js = ('<script>(function(){var el=function(i){return document.getElementById(i)},c=["rp","rn","rl","rd"].map(el),es=["Pecorino stagionato","Azienda agricola Rossi","Amatrice (RI)",""];'
 'function testo(){var v=c.map(function(x){return x.value.trim()}),vuoto=!(v[0]||v[1]||v[2]);if(vuoto)v=es.slice(0,3).concat(c[3].value.trim());'
 'var t=v[0]+(v[1]?(v[0]?" – ":"")+v[1]:"")+(v[2]?", "+v[2]:"");if(t)t+=".";return{riga:t,det:v[3],vuoto:vuoto}}'
 'function disegna(){var t=testo();el("riga").textContent=t.riga;el("riga").style.opacity=t.vuoto?".45":"1";el("det").textContent=t.det;el("copiato").textContent=""}'
 'c.forEach(function(x){x.addEventListener("input",disegna)});'
 'el("copia").addEventListener("click",function(){var t=testo(),s=t.riga+(t.det?" "+t.det.charAt(0).toUpperCase()+t.det.slice(1)+".":"");'
 'function fatto(){el("copiato").textContent="Copiata. Incollala nel tuo menu."}'
 'if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(s).then(fatto,vecchio)}else vecchio();'
 'function vecchio(){var a=document.createElement("textarea");a.value=s;a.style.position="fixed";a.style.opacity="0";document.body.appendChild(a);a.select();try{document.execCommand("copy");fatto()}catch(e){el("copiato").textContent="Seleziona la riga e copiala a mano."}document.body.removeChild(a)}});'
 'disegna()})();</script>')
riga = (capo('<a href="cucine.html">Cucine</a> / La riga per il menu', 'Il produttore, <em>nel tuo menu.</em>',
             'Scrivi prodotto, produttore e luogo: la riga è pronta da copiare. Gratis, per qualsiasi fornitore.')
 + '<section class="sez bianca stretta"><div class="wrap due" style="align-items:center">'
   '<div class="modulo"><div class="form">'
   '<label class="full">Prodotto<input id="rp" type="text" maxlength="80" placeholder="Es. Pecorino stagionato" autocomplete="off"></label>'
   '<label class="full">Produttore<input id="rn" type="text" maxlength="80" placeholder="Es. Azienda agricola Rossi" autocomplete="off"></label>'
   '<label>Luogo<input id="rl" type="text" maxlength="60" placeholder="Es. Amatrice (RI)" autocomplete="off"></label>'
   '<label>Dettaglio (facoltativo)<input id="rd" type="text" maxlength="80" placeholder="Es. latte crudo, 12 mesi" autocomplete="off"></label></div></div>'
   '<div><div class="carta-menu"><b>Sul menu</b><p id="riga">Pecorino stagionato – Azienda agricola Rossi, Amatrice (RI).</p><small id="det"></small></div>'
   '<div class="btns" style="margin-top:24px"><button type="button" class="btn verde" id="copia">Copia la riga</button></div><p class="copiato" id="copiato" aria-live="polite"></p></div>'
   '</div></section>' + riga_js
 + sez(tessere(('Solo cose vere', 'Scrivi ciò che il produttore conferma.', False), ('DOP, IGP, bio', 'Solo per il prodotto certificato.', True), ('Tienila aggiornata', 'Cambi fornitore? Cambia la riga.', False), cls='tre'),
       occhiello='Tre regole', h2='Il menu è un\'informazione al cliente')
 + '<section class="sez miele-b"><div class="wrap fascia"><h2>Cerchi produttori da raccontare?</h2>' + btn('cucine.html#richiesta', 'Chiedi un campione', '') + '</div></section>')
scrivi('riga-menu', 'La riga per il menu: scrivi il nome del produttore | Filo Corto',
       'Strumento gratuito per ristoranti, bar e hotel: scrivi prodotto, produttore e luogo e copia la riga pronta per il menu.', riga, menu='cucine.html')


# ---------------- GRAZIE, ERRORE, PAGINA NON TROVATA ----------------
def avviso(h1, grande, bottoni):
    return f'<div class="wrap"><div class="avviso">{CERCHIONE}<h1>{h1}</h1><p class="grande">{grande}</p><div class="btns">{bottoni}</div></div></div>'


scrivi('grazie', 'Ricevuto, grazie | Filo Corto', 'Abbiamo ricevuto il tuo messaggio.',
       avviso('Ricevuto. <em>Grazie.</em>', 'Ti abbiamo mandato un\'email di conferma con i prossimi passi. Se non la vedi, guarda nella posta indesiderata.',
              btn('./', 'Torna alla pagina iniziale') + btn('guide/', 'Leggi le guide', '')), extra='noindex: si\n')
scrivi('errore', 'Il messaggio non è partito | Filo Corto', 'Il messaggio non è partito: riprova o scrivici per email.',
       avviso('Qualcosa non ha <em>funzionato.</em>', 'Il messaggio non è partito. Controlla di aver compilato tutti i campi e riprova, oppure scrivi a <a href="mailto:info@ilfilocorto.it">info@ilfilocorto.it</a>.',
              '<a class="btn verde" href="javascript:history.back()">← Torna al modulo</a>' + btn('./', 'Pagina iniziale', '')), extra='noindex: si\n')
scrivi('404', 'Pagina non trovata | Filo Corto', 'Questa pagina non c\'è.',
       avviso('Questa pagina <em>non c\'è.</em>', 'Forse l\'indirizzo è cambiato. Riparti da qui.',
              btn('/', 'Pagina iniziale') + btn('/produttori.html', 'Sono un produttore', '') + btn('/cucine.html', 'Ho una cucina', '') + btn('/guide/', 'Le guide', '')), extra='noindex: si\nradice: /\n')

# ---------------- CREDITI DELLE FOTO ----------------
# Le foto scelte (licenza Unsplash, uso libero): nome del file, soggetto, autore, codice della pagina su Unsplash.
# La pagina dei crediti elenca solo quelle che sono davvero nel sito (file presenti in site/foto/).
FOTO_CREDITI = [('ulivo', 'Olive sul ramo dopo la pioggia', 'The Now Time', 'hnkdeJJoY-A'), ('olive', 'Olive verdi sul ramo', 'Janine Joles', '-8nbY8W2YEE'),
                ('mani', 'Mani con patate appena raccolte', 'JESHOOTS.COM', 'fp1x-X7DwDs'), ('chef', 'Chef che impiatta', 'Urban Gyllström', 'MaWMfm-HCqQ'),
                ('barattoli', 'Barattoli su uno scaffale', 'Artem Kostelnyuk', 'NrqKwJ1KPo8'), ('cassette', 'Verdure in cassette di legno', 'Noah Buisson', 'XPltBlxfChk'),
                ('mercato', 'Banco di un mercato rionale a Roma', 'Ágatha Depiné', 'sgQTbIU43Mg'), ('civita', 'Civita di Bagnoregio', 'Pablo Allendes', 'aVWzRGYLjZI'),
                ('legumi', 'Legumi secchi al mercato', 'Shelley Pauls', 't4X660oKiYs')]
CARTELLA_FOTO = P.parent.parent / 'site' / 'foto'
presenti = [c for c in FOTO_CREDITI if any(CARTELLA_FOTO.glob(c[0] + '-*.jpg'))] if CARTELLA_FOTO.exists() else []
if presenti:
    elenco_foto = ('<div class="scorri-x"><table><thead><tr><th>Foto</th><th>Autore</th><th>Fonte</th></tr></thead><tbody>'
                   + ''.join(f'<tr><td>{t}</td><td>{a}</td><td><a href="https://unsplash.com/photos/{c}" rel="noopener">Unsplash</a></td></tr>' for _, t, a, c in presenti)
                   + '</tbody></table></div><p>Le foto hanno licenza libera (licenza Unsplash) e sono salvate sul nostro server: chi visita il sito non si collega a servizi esterni.</p>')
    sotto = 'Grazie a chi ha scattato le foto di questo sito.'
else:
    elenco_foto = '<p>Per ora il sito usa solo disegni nostri. Quando aggiungeremo delle fotografie, qui troverai i nomi di chi le ha scattate.</p>'
    sotto = 'Chi ha fatto le immagini di questo sito.'
cred = (capo('Crediti', 'Crediti <em>delle immagini.</em>', sotto)
 + '<section class="sez bianca"><div class="wrap prosa">' + elenco_foto
 + '<p>Disegni e icone: Filo Corto. Caratteri: Archivo e Manrope (licenza SIL Open Font).</p>'
   '<p>Le foto delle pagine dei produttori sono dei produttori, pubblicate con il loro permesso.</p></div></section>')
scrivi('crediti', 'Crediti delle immagini | Filo Corto', 'Gli autori delle immagini usate sul sito di Filo Corto.', cred, extra='noindex: si\n')

print('pagine scritte')
