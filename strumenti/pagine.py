# Filo Corto – sorgenti delle pagine principali (src/pagine/*.html). Uso: python3 strumenti/pagine.py && python3 build.py
import pathlib, json
P = pathlib.Path(__file__).resolve().parent.parent / 'src' / 'pagine'

def cerchio(x, y, R, cls=''):  # proporzioni identiche all'icona di SicuroFood (178/56/52)
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

def foto(f, alt, cls='', testo=''):
    t = f'<figcaption>{testo}</figcaption>' if testo else ''
    return f'<figure class="foto {cls}"><img src="foto.php?f={f}" alt="{alt}" loading="lazy" decoding="async">{t}</figure>'

def fascia_foto(f, alt):
    return '<div class="wrap">' + foto(f, alt, 'larga') + '</div>'

MOSAICO = ('<div class="mosaico">' + foto('uliveto', 'Rami di ulivo con olive', 'a', 'La terra')
           + foto('mani', 'Mani di un contadino con patate appena raccolte', 'b', 'Le mani')
           + foto('chef', 'Uno chef che impiatta', 'c', 'La cucina') + '</div>')

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
 '<h1>Il prodotto vero, dal campo alla cucina.</h1>'
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
 + sez(stagione() + '<p class="piccolo" style="margin-top:18px">Cosa offre la terra in questo periodo. Il listino della rete arriverà con i primi produttori.</p>',
       occhiello='In stagione ora', h2='Il calendario delle nostre terre')
 + sez(FILI, cls='bianca', occhiello='La differenza', h2='Meno passaggi, più valore')
 + sez('<div class="passi-h">'
       '<div><i>1</i><b>Il produttore si candida</b><span>Due minuti, poi scheda e check-up.</span></div>'
       '<div><i>2</i><b>La cucina assaggia</b><span>Il campione è gratis.</span></div>'
       '<div><i>3</i><b>Ordine e fattura diretta</b><span>Dal produttore alla cucina.</span></div></div>' + PATTI,
       occhiello='Come funziona', h2='Tre passi, patti chiari')
 + sez('<div class="cat">' + ''.join(f'<div>{I[k]}<span>{n}</span></div>' for k, n in [('formaggio', 'Formaggi'), ('olio', 'Olio'), ('conserve', 'Conserve'), ('legumi', 'Legumi e cereali'), ('miele', 'Miele'), ('vino', 'Vino e birra'), ('farine', 'Farine e pasta'), ('salumi', 'Salumi')]) + '</div>'
       + '<p style="margin-top:26px">' + btn('produttori.html#candidati', 'Produci uno di questi? Candidati') + '</p>', cls='bianca', occhiello='Chi cerchiamo', h2='Per cominciare: prodotti che viaggiano bene')
 + sez('<div class="tappe"><div class="ora"><b>Oggi</b><span>Raccogliamo le adesioni</span></div><div><b>Poi</b><span>Prova con le prime cucine</span></div><div><b>Infine</b><span>Ordini online</span></div></div>'
       '<p class="piccolo" style="margin-top:16px">Nessun prodotto è ancora in vendita.</p>', occhiello='A che punto siamo', h2='Rete in costruzione')
 + sez('<div class="elenco-guide">'
       '<a href="guide/vendere-ai-ristoranti.html"><b>Come vendere ai ristoranti</b><span>I passi concreti.</span><i>→</i></a>'
       '<a href="guide/documenti-per-vendere-ai-ristoranti.html"><b>Documenti e requisiti</b><span>Cosa serve davvero.</span><i>→</i></a>'
       '<a href="prova.html"><b>Sei pronto? Fai la prova</b><span>Dieci domande.</span><i>→</i></a></div>'
       '<p style="margin-top:22px"><a href="guide/">Tutte le guide →</a> · <a href="territori/">I territori →</a></p>', cls='bianca', occhiello='Gratis', h2='Guide per i produttori')
 + CTA)
scrivi('index', 'Filo Corto | Piccoli produttori italiani per ristoranti, bar e hotel',
       'Filo Corto dà visibilità ai piccoli produttori e porta il prodotto vero delle nostre terre in ristoranti, bar e hotel. Solo materie prime italiane. Si parte dal Lazio.', home)

# ---------------- PRODUTTORI ----------------
prod = (capo('Produttori', 'Fai un prodotto vero? Fatti trovare.',
             'C\'è chi ti cerca da una vita: chef, ristoratori, hotel, appassionati. Ti diamo una vetrina dove trovarti. Gratis.',
             '<div class="btns" style="margin-top:24px">' + btn('#candidati', 'Candidati') + btn('prova.html', 'Sei pronto? Fai la prova', '') + '</div>')
 + fascia_foto('mani', 'Mani di un contadino con patate appena raccolte')
 + sez('<div class="due"><div class="riquadro"><h3>Ti diamo</h3>' + punti('Una pagina tutta tua, visibile a tutti', 'Il listino davanti alle cucine', 'Il check-up gratis (per i primi)', 'Un solo interlocutore') +
       '</div><div class="riquadro m"><h3>Ti chiediamo</h3>' + punti('Materie prime italiane', 'Giorni di consegna fissi', 'Prezzi e quantità per iscritto', 'Documenti e lotti in ordine') + '</div></div>' + PATTI, cls='bianca')
 + sez(passi(('Ti candidi', '2 minuti, qui sotto.'), ('Scheda e check-up', 'Prodotti, prezzi, consegne. Poi la visita.'), ('Entri nel listino', 'E nella prova con le prime cucine.')), cls='scura', occhiello='Come si entra', h2='Tre passi')
 + sez('<div class="due"><div><p class="grande">Ti rispondiamo per email con la scheda di adesione.</p><p>Oppure scrivi a <a href="mailto:info@ilfilocorto.it">info@ilfilocorto.it</a></p></div>'
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
       '<p style="margin-top:20px"><a href="domande.html">Tutte le domande →</a></p>', occhiello='Domande', h2='In breve'))
scrivi('produttori', 'Vendere ai ristoranti: la rete dei piccoli produttori | Filo Corto',
       'Sei un piccolo produttore? Con Filo Corto il tuo prodotto arriva a ristoranti, bar e hotel. Pagina gratuita, check-up gratuito per i primi. Si parte dal Lazio.', prod, menu='produttori.html')

# ---------------- CUCINE ----------------
cuc = (capo('Cucine', 'Prodotti veri per la tua cucina.',
            'Da piccoli produttori, con materie prime italiane. E con le regole che servono a una cucina.',
            '<div class="btns" style="margin-top:24px">' + btn('#richiesta', 'Chiedi un campione') + '</div>')
 + fascia_foto('chef', 'Uno chef che impiatta')
 + sez(tessere(('Quando arriva?', 'Giorni e orari d\'ordine scritti.', False),
               ('Quanto costa?', 'Listino unico, al kg o al pezzo.', True),
               ('Ci sarà sempre?', 'Quantità settimanale scritta.', False), cls='tre')
       + gettoni('Solo materie prime italiane', 'Campione gratis', 'Fattura diretta del produttore', 'Accanto al tuo distributore', '<a href="riga-menu.html">Riga per il menu</a>'),
       cls='bianca', occhiello='Le tue tre domande', h2='Tre risposte scritte')
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
           ('Vendete ai privati?', 'La vetrina dei produttori è aperta a tutti. Gli ordini, per ora, sono per ristoranti, bar e hotel.')), occhiello='Domande', h2='In breve'))
scrivi('cucine', 'Prodotti italiani per ristoranti, bar e hotel | Filo Corto',
       'Formaggi, olio, conserve, legumi e miele da piccoli produttori, con materie prime italiane, per ristoranti, bar e hotel. Campione gratis, prezzi e consegne per iscritto.', cuc, menu='cucine.html')

# ---------------- CHECK-UP ----------------
chk = (capo('Check-up', 'Sei pronto per le cucine?',
            'Una visita, una lista uguale per tutti, un rapporto scritto. Gratis per i primi produttori.',
            '<div class="btns" style="margin-top:24px">' + btn('produttori.html#candidati', 'Candidati') + '</div>')
 + fascia_foto('formaggi', 'Forme di formaggio in stagionatura')
 + sez(tessere(('Documenti', 'Registrazione, autocontrollo, registri, formazione.', False),
               ('Prodotto', 'Origine delle materie prime, lotti, etichette, allergeni.', True),
               ('Consegne e prezzi', 'Trasporto, tempi, listino, quantità.', False), cls='tre'),
       cls='bianca', occhiello='Cosa guardiamo', h2='Tre aree, 14 punti')
 + sez(passi(('La visita', 'In azienda, con la lista.'), ('La prova del lotto', 'Da un prodotto venduto, carte alla mano, fino alle materie prime.'), ('Il rapporto', 'Esito: pronto, quasi pronto, da preparare.')), cls='scura', occhiello='Come funziona', h2='Tre passi')
 + sez('<p class="grande">Ristoranti e hotel devono qualificare i fornitori nel loro piano HACCP: il check-up ti prepara a questo. Lo fa Valerio Semeraro, Food Specialist e consulente HACCP.</p>'
       + gettoni('Non è una certificazione', 'Non sostituisce i controlli ufficiali', 'Non garantisce vendite'), occhiello='Perché serve', h2='Patti chiari')
 + CTA)
scrivi('check-up', 'Check-up per piccoli produttori: pronto per ristoranti e hotel? | Filo Corto',
       'Visita in azienda, lista uguale per tutti, rapporto scritto: documenti, origine, lotti, etichette, consegne. Gratis per i primi produttori.', chk, menu='check-up.html')

# ---------------- COME FUNZIONA ----------------
cf = (capo('Come funziona', 'Come funziona',
           'Niente magazzino, niente rivendita. Mettiamo in contatto chi produce e chi cucina, con le stesse regole per tutti.')
 + fascia_foto('legumi', 'Legumi secchi al mercato')
 + sez('<div class="due"><div class="riquadro"><h3>Se produci</h3>' + passi(('Ti candidi', '2 minuti.'), ('Scheda e check-up', 'Poi la visita.'), ('Entri nel listino', 'E nella prova.')) +
       '</div><div class="riquadro m"><h3>Se cucini</h3>' + passi(('Scegli', 'Dal listino.'), ('Assaggi', 'Campione gratis.'), ('Ordini', 'Fattura diretta.')) + '</div></div>', cls='bianca')
 + sez(PATTI + '<p class="grande" style="margin-top:28px">Consegne: le definiamo con i primi produttori. L\'obiettivo è una consegna unica in giorni fissi.</p>'
       '<p class="piccolo" style="margin-top:12px">Non siamo un e-commerce per privati, né un grossista, né un ente di certificazione.</p>', cls='scura', occhiello='Le regole', h2='Uguali per tutti')
 + CTA)
scrivi('come-funziona', 'Come funziona Filo Corto | Filo Corto',
       'Il produttore si candida e fa il check-up, la cucina assaggia e ordina, il produttore consegna e fattura. Regole uguali per tutti, solo materie prime italiane.', cf, menu='come-funziona.html')

# ---------------- CHI SIAMO ----------------
cs = (capo('Chi siamo', 'Appassionati del cibo vero.',
           'Veniamo dalle cucine. Vogliamo che il prodotto delle nostre terre torni nei piatti.')
 + fascia_foto('uliveto', 'Rami di ulivo con olive')
 + sez('<div class="manifesto"><p>Da una parte ottimi piccoli produttori. Dall\'altra cucine che comprano solo dai grandi distributori.<br><em>Filo Corto accorcia questa distanza.</em></p></div>'
       + tessere(('Si sa chi lo fa', 'Nome e indirizzo.', False), ('È italiano', 'Materie prime italiane.', True),
                 ('Si racconta', 'Una storia vera, per il menu.', False), ('È in regola', 'Documenti e lotti.', True)), cls='scura', occhiello='Cibo vero', h2='Cosa intendiamo')
 + sez('<p class="grande">Valerio Semeraro, Food Specialist e consulente HACCP, segue le adesioni e fa i check-up. <a href="mailto:info@ilfilocorto.it">info@ilfilocorto.it</a></p>', cls='bianca', occhiello='Chi cura il progetto', h2='Valerio Semeraro')
 + CTA)
scrivi('chi-siamo', 'Chi siamo: appassionati del cibo vero | Filo Corto',
       'Filo Corto nasce dalle cucine: appassionati del cibo vero che vogliono riportare il prodotto delle nostre terre in ristoranti, bar e hotel.', cs, menu='chi-siamo.html')

# ---------------- DOMANDE ----------------
FP = [('Aderire costa?', 'No. Gratis, senza impegno. Esci quando vuoi.'),
      ('Mi garantite vendite?', 'No. Scelgono le cucine.'),
      ('Quanto guadagna Filo Corto?', 'Un margine sulle vendite, scritto nella scheda prima di ogni ordine e dichiarato anche alle cucine.'),
      ('Chi fattura?', 'Tu, il produttore. La cucina paga te.'),
      ('Devo consegnare io?', 'Lo decidiamo con i primi produttori. L\'obiettivo è una consegna unica.'),
      ('Cos\'è il check-up?', 'Una visita con una lista uguale per tutti: documenti, origine, lotti, etichette, consegne. Gratis per i primi. Non è una certificazione.'),
      ('Materie prime estere?', 'No. Solo materie prime coltivate o allevate in Italia, niente import UE o extra UE. Lo guardiamo al check-up.'),
      ('Produco fuori dal Lazio.', 'Partiamo dal Lazio. Scrivici lo stesso: ti ricontattiamo quando la rete si allarga.'),
      ('Quali prodotti cercate?', 'Per iniziare, quelli che si conservano: formaggi stagionati, olio, conserve, legumi, miele, vino e birra, farine, pasta, salumi.')]
FC = [('Posso già ordinare?', 'Non ancora: chiedi un campione e ti scriviamo quando c\'è un produttore pronto.'),
      ('Da dove vengono i prodotti?', 'Da piccoli produttori, con materie prime italiane. Su ogni prodotto: chi e dove.'),
      ('Devo lasciare il distributore?', 'No. Ti diamo quello che lui non ha.'),
      ('Come si paga?', 'A fattura, al produttore.'),
      ('Vendete ai privati?', 'La vetrina dei produttori è aperta a tutti. Gli ordini, per ora, sono per ristoranti, bar e hotel.')]
dom = (capo('Domande', 'Domande frequenti', 'Risposte brevi.')
 + sez(faq(*FP), cls='bianca', occhiello='Se produci', h2='Produttori')
 + sez(faq(*FC), occhiello='Se cucini', h2='Cucine') + CTA)
faqjson = json.dumps({'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in FP + FC]}, ensure_ascii=False)
scrivi('domande', 'Domande frequenti: produttori e cucine | Filo Corto',
       'Quanto costa aderire, chi fattura, cos\'è il check-up, materie prime italiane, si può già ordinare: le risposte brevi per produttori e cucine.', dom, extra=f'schema: {faqjson}\n')
print('pagine scritte')
