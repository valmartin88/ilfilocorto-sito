# Genera i sorgenti delle pagine principali di Filo Corto (src/pagine/*.html)
import pathlib
P = pathlib.Path('/home/claude/ilfilocorto-sito/src/pagine')

CERCHIO = '<circle cx="{x}" cy="{y}" r="{r}" fill="#F2F4F0" stroke="#E8692C" stroke-width="{w}"/><circle cx="{x}" cy="{y}" r="{d}" fill="#12302B"/>'
def cerchio(x, y, R):  # R = raggio esterno; proporzioni identiche all'icona di SicuroFood (178/56/52)
    w = round(R * 56 / 178, 2); return CERCHIO.format(x=x, y=y, r=round(R - w / 2, 2), w=w, d=round(R * 52 / 178, 2))

ARTE = ('<svg class="arte" viewBox="0 0 440 440" role="img" aria-label="Dal campo alla cucina, nel Lazio">'
        '<rect width="440" height="440" fill="#2f5d3a"/>'
        '<path d="M0 360 C 90 340, 170 380, 260 362 S 400 340, 440 352" stroke="#477a52" stroke-width="10" fill="none"/>'
        '<path d="M0 396 C 100 380, 180 410, 280 396 S 400 384, 440 390" stroke="#477a52" stroke-width="10" fill="none"/>'
        '<path d="M188 92 C 250 92, 300 140, 312 236" stroke="#e9b565" stroke-width="11" stroke-linecap="round" stroke-dasharray="0.1 24" fill="none"/>'
        '<path d="M44 196 C 44 120, 92 70, 176 66 C 176 146, 126 196, 44 196 Z" fill="#8fc49a" stroke="#1f2420" stroke-width="4"/>'
        '<path d="M58 184 L 160 84" stroke="#1f2420" stroke-width="4" stroke-linecap="round"/>'
        '<g transform="rotate(6 344 76)"><rect x="276" y="56" width="140" height="44" fill="#e9b565" stroke="#1f2420" stroke-width="4"/>'
        '<text x="346" y="86" text-anchor="middle" class="et">LAZIO</text></g>'
        + cerchio(330, 318, 74) +
        '<text x="44" y="246" class="lab">DAL CAMPO</text><text x="408" y="424" text-anchor="end" class="lab">ALLA CUCINA</text></svg>')

def scrivi(slug, titolo, desc, corpo, menu='', extra=''):
    testa = f'titolo: {titolo}\ndesc: {desc}\n' + (f'menu: {menu}\n' if menu else '') + extra + '---\n'
    (P / f'{slug}.html').write_text(testa + corpo.strip() + '\n', encoding='utf-8')

def capo(briciola, h1, grande, bottoni='', occhiello=''):
    b = f'<p class="briciole"><a href="./">Filo Corto</a> / {briciola}</p>' if briciola else ''
    o = f'<p class="occhiello">{occhiello}</p>' if occhiello else ''
    return f'<div class="wrap"><div class="capo">{b}{o}<h1>{h1}</h1><p class="grande">{grande}</p>{bottoni}</div></div>'

def passi(*voci):
    return '<ol class="passi">' + ''.join(f'<li><b>{t}</b><span>{s}</span></li>' for t, s in voci) + '</ol>'

def punti(*voci):
    return '<ul class="punti">' + ''.join(f'<li>{v}</li>' for v in voci) + '</ul>'

def tessere(*voci, cls=''):
    return f'<div class="tessere {cls}">' + ''.join(f'<div class="tessera{" m" if m else ""}"><p class="domanda">{t}</p><p>{s}</p></div>' for t, s, m in voci) + '</div>'

def sez(contenuto, cls='', occhiello='', h2='', intro=''):
    t = ''
    if h2:
        t = '<div class="testa">' + (f'<p class="occhiello">{occhiello}</p>' if occhiello else '') + f'<h2>{h2}</h2>' + (f'<p class="grande">{intro}</p>' if intro else '') + '</div>'
    return f'<section class="sez {cls}"><div class="wrap">{t}{contenuto}</div></section>'

def faq(*voci):
    return '<div class="faq">' + ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in voci) + '</div>'

PATTI = tessere(('Gratis', 'Aderire non costa e non ti impegna. Esci quando vuoi.', False),
                ('Fatturi tu', 'La cucina paga te, direttamente.', True),
                ('Margine chiaro', 'Il nostro margine è scritto prima di ogni ordine.', False),
                ('Niente promesse', 'Nessuna vendita garantita: scelgono le cucine.', True))

CTA = ('<section class="sez verde-b"><div class="wrap due" style="align-items:center"><div><p class="occhiello">Per i produttori</p><h2>Produci nel Lazio?</h2></div>'
       '<div style="display:flex;flex-direction:column;gap:22px;align-items:flex-start"><p class="grande">Candidati in due minuti. Gratis, senza impegno.</p>'
       '<a class="btn miele" href="produttori.html#candidati">Candidati adesso →</a></div></div></section>')

NASTRO = ('<div class="nastro" aria-hidden="true"><div>' + ''.join(f'<span>{x}</span><i></i>' for x in
          ['Formaggi', 'Olio extravergine', 'Conserve', 'Legumi', 'Miele', 'Vino', 'Birra artigianale', 'Farine', 'Pasta secca', 'Salumi'] * 2) + '</div></div>')

FILI = ('<div class="fili"><div class="lungo"><h3>Filo lungo</h3><ol class="catena">'
        '<li class="f"><span>Produttore</span></li><li><span>Grossista</span></li><li><span>Piattaforma</span></li><li><span>Distributore</span></li><li class="f"><span>Cucina</span></li></ol></div>'
        '<div class="corto"><h3>Filo corto</h3><ol class="catena"><li><span>Produttore</span></li><li><span>Cucina</span></li></ol></div></div>')

MISSIONE = sez('<div class="due" style="align-items:start"><div><p class="grande" style="font-size:clamp(20px,2.2vw,25px)">In tutta Italia ci sono piccoli produttori che fanno cose straordinarie e restano invisibili: troppo piccoli per i grandi distributori, troppo lontani dalle cucine. Intanto nei piatti arriva merce che viene da fuori.</p>'
 '<p class="grande" style="margin-top:18px;font-size:clamp(20px,2.2vw,25px)">Filo Corto nasce per cambiare le cose: dare voce a chi produce davvero e tenere sulle nostre tavole il prodotto vero delle nostre terre. Perché il made in Italy continui a vivere nei piatti, non solo nelle parole.</p></div>'
 + tessere(('Visibili', 'Ogni produttore con un nome, un luogo, una pagina sua.', False),
           ('Italiani', 'Solo materie prime coltivate e allevate in Italia. Niente prodotti importati, né UE né extra UE.', True),
           ('Vicini', 'Dal territorio alle cucine del territorio. Partiamo dal Lazio.', False), cls='uno') + '</div>',
 cls='scura', occhiello='Perché esistiamo', h2='Il prodotto vero delle nostre terre')

# ---------------- HOME ----------------
home = (
 '<div class="wrap"><div class="eroe"><div class="testo"><p class="occhiello">Lazio · Rete in costruzione</p>'
 '<h1>Dal produttore alla cucina. Senza giri lunghi.</h1>'
 '<p class="grande">Diamo visibilità ai piccoli produttori italiani e portiamo il loro prodotto vero nelle cucine di ristoranti, bar e hotel. Solo materie prime italiane. Partiamo dal Lazio.</p>'
 '<div class="btns"><a class="btn verde" href="produttori.html">Sono un produttore →</a><a class="btn" href="cucine.html">Ho una cucina →</a></div></div>'
 + ARTE + '</div></div>' + NASTRO + MISSIONE +
 sez('<div class="porte">'
     '<div class="porta"><span class="timbro">Check-up gratis per i primi produttori</span><p class="occhiello">Se produci</p><h2>Vendi alle cucine, senza inseguirle.</h2>'
     + punti('Esci dall\'invisibilità: una pagina tutta tua, gratis', 'Il tuo listino davanti a ristoranti, bar e hotel', 'Un check-up per presentarti in regola') +
     '<a class="btn verde" href="produttori.html">Entra nella rete →</a></div>'
     '<div class="porta v"><p class="occhiello">Se cucini</p><h2>Prodotti veri, con regole da cucina.</h2>'
     + punti('Solo materie prime italiane', 'Il campione prima dell\'ordine', 'Prezzi, consegne e quantità per iscritto', 'La storia del prodotto, pronta per il menu') +
     '<a class="btn miele" href="cucine.html">Chiedi un campione →</a></div></div>', cls='bianca')
 + sez(FILI, occhiello='La differenza', h2='Filo lungo, filo corto', intro='Meno passaggi: più margine a chi produce, più freschezza e una storia vera per chi cucina.')
 + sez(passi(('Il produttore si candida', 'Due minuti online, poi la scheda e il check-up in azienda.'),
             ('La cucina assaggia', 'Sceglie dal listino e prova un campione prima di ordinare.'),
             ('Il produttore consegna e fattura', 'Direttamente alla cucina. Il nostro margine è dichiarato prima.')),
       cls='bianca', occhiello='Come funziona', h2='Tre passi') 
 + sez(PATTI, occhiello='Patti chiari', h2='Le regole, subito')
 + sez('<div class="tessere"><div class="tessera m"><p class="domanda">Oggi</p><p>Raccogliamo le adesioni dei produttori e facciamo i primi check-up.</p></div>'
       '<div class="tessera"><p class="domanda">Poi</p><p>Una prova con i primi produttori e le prime cucine.</p></div>'
       '<div class="tessera"><p class="domanda">Infine</p><p>La rete si allarga e le cucine ordinano online.</p></div></div>'
       '<p style="margin-top:22px">Nessun prodotto è ancora in vendita: lo diciamo chiaro.</p>', cls='bianca', occhiello='A che punto siamo', h2='Rete in costruzione')
 + sez('<div class="elenco-guide">'
       '<a href="guide/vendere-ai-ristoranti.html"><b>Come vendere ai ristoranti</b><span>I passi concreti, dal prodotto al pagamento.</span><i>→</i></a>'
       '<a href="guide/documenti-per-vendere-ai-ristoranti.html"><b>Documenti e requisiti</b><span>Cosa serve per vendere a ristoranti e hotel.</span><i>→</i></a>'
       '<a href="prova.html"><b>Sei pronto? Fai la prova</b><span>Dieci domande, due minuti.</span><i>→</i></a>'
       '</div><p style="margin-top:26px"><a href="guide/">Tutte le guide →</a> · <a href="territori/">I territori del Lazio →</a></p>',
       occhiello='Per i produttori', h2='Guide gratuite')
 + CTA)
scrivi('index', 'Filo Corto | Piccoli produttori del Lazio per ristoranti, bar e hotel',
       'Filo Corto dà visibilità ai piccoli produttori e porta il prodotto vero delle nostre terre in ristoranti, bar e hotel. Solo materie prime italiane. Si parte dal Lazio.', home)

# ---------------- PRODUTTORI ----------------
prod = (capo('Produttori', 'Porta i tuoi prodotti nelle cucine del Lazio.',
             'Fai un prodotto vero e nessuno lo sa? Da soli è difficile arrivare alle cucine: vogliono consegne puntuali, prezzi chiari e merce sempre disponibile. Insieme, con regole comuni, si può.',
             '<div class="btns" style="margin-top:26px"><a class="btn verde" href="#candidati">Candidati →</a><a class="btn" href="prova.html">Sei pronto? Fai la prova →</a></div>')
 + sez('<div class="due"><div><h2 style="margin-bottom:18px">Cosa ottieni</h2>'
       + punti('Il listino davanti a ristoranti, bar e hotel del Lazio', 'Una pagina tutta tua sul sito, gratis', 'Il check-up gratuito, per i primi produttori', 'Un solo interlocutore, invece di cento trattative') +
       '</div><div><h2 style="margin-bottom:18px">Cosa ti chiediamo</h2>'
       + punti('Materie prime italiane: niente prodotti importati, né UE né extra UE', 'Giorni di consegna fissi', 'Prezzi dichiarati e stabili per un periodo', 'Quantità settimanali scritte', 'Documenti, etichette e lotti in ordine') +
       '</div></div>', cls='bianca')
 + sez(PATTI, occhiello='Patti chiari', h2='Gratis. E senza giri di parole.')
 + sez(passi(('Ti candidi', 'Due minuti, con il modulo qui sotto.'),
             ('Scheda e check-up', 'Ci dici prodotti, prezzi e consegne; poi una visita in azienda.'),
             ('Entri nel listino', 'E partecipi alla prova con le prime cucine.')), cls='scura', occhiello='Come si entra', h2='Tre passi')
 + '<section class="sez verde-b" id="candidati"><div class="wrap due"><div><p class="occhiello">Candidatura</p><h2>Candidati alla rete</h2>'
   '<p class="grande">Ti rispondiamo per email con la scheda di adesione. Gratis, senza impegno.</p><p>Preferisci scrivere? <a href="mailto:info@ilfilocorto.it" style="color:var(--miele-chiaro)">info@ilfilocorto.it</a></p></div>'
   '<div class="modulo"><form class="form" action="invia.php" method="post"><input type="hidden" name="tipo" value="produttore">'
   '<div class="hp" aria-hidden="true"><label>Lascia vuoto<input type="text" name="sito_web" tabindex="-1" autocomplete="off"></label></div>'
   '<label>Nome dell\'azienda<input type="text" name="azienda" required maxlength="120" autocomplete="organization"></label>'
   '<label>Referente<input type="text" name="referente" required maxlength="120" autocomplete="name"></label>'
   '<label>Email<input type="email" name="email" required maxlength="160" autocomplete="email"></label>'
   '<label>Comune<input type="text" name="comune" required maxlength="120"></label>'
   '<label class="full">Cosa produci<textarea name="prodotti" rows="3" required maxlength="2000" placeholder="Es. pecorino stagionato, ricotta"></textarea></label>'
   '<label class="full">Come consegni oggi<select name="consegna"><option>Consegno io, con mezzo mio</option><option>Uso un corriere</option><option>Vendo solo in azienda o al mercato</option></select></label>'
   '<label class="full check"><input type="checkbox" name="consenso" value="si" required><span>Ho capito che aderire è gratuito, non mi impegna e non promette vendite. Ho letto l\'<a href="privacy.html">informativa privacy</a>.</span></label>'
   '<button class="btn miele full" type="submit">Invia la candidatura →</button></form></div></div></section>'
 + sez(faq(('Quanto costa?', 'Niente. Aderire è gratuito e puoi uscire quando vuoi.'),
           ('Mi garantite delle vendite?', 'No. Le cucine scelgono liberamente: noi ti presentiamo nel modo giusto.'),
           ('Come guadagna Filo Corto?', 'Con un margine sulle vendite, scritto nella scheda prima di qualsiasi ordine.'),
           ('Il check-up è una certificazione?', 'No. È una valutazione per la rete, gratuita per i primi produttori. Non sostituisce i controlli ufficiali.')) +
       '<p style="margin-top:22px"><a href="domande.html">Tutte le domande →</a></p>', occhiello='Domande', h2='In breve'))
scrivi('produttori', 'Vendere ai ristoranti: la rete dei produttori del Lazio | Filo Corto',
       'Sei un piccolo produttore del Lazio? Con Filo Corto il tuo listino arriva a ristoranti, bar e hotel. Adesione gratuita, check-up gratuito per i primi.', prod, menu='produttori.html')

# ---------------- CUCINE ----------------
cuc = (capo('Cucine', 'Prodotti del Lazio per la tua cucina.',
            'Formaggi, olio, conserve, legumi, miele e altro, da piccoli produttori della regione, con materie prime italiane. E con le regole che servono a una cucina professionale.',
            '<div class="btns" style="margin-top:26px"><a class="btn verde" href="#richiesta">Chiedi un campione →</a></div>')
 + sez(tessere(('Quando arriva?', 'Giorni di consegna e orari d\'ordine scritti, produttore per produttore.', False),
               ('Quanto costa?', 'Un listino unico, al chilo o al pezzo, da confrontare con il tuo.', True),
               ('Ci sarà sempre?', 'Quantità settimanale scritta e mesi di disponibilità.', False)), cls='bianca', occhiello='Le tue tre domande', h2='Tre risposte scritte')
 + sez(passi(('Dicci cosa cerchi', 'Prodotti e zona di consegna, con il modulo qui sotto.'),
             ('Assaggi il campione', 'Gratis e senza impegno.'),
             ('Ordini', 'Anche da più produttori insieme. Ognuno ti fattura direttamente.')), cls='scura', occhiello='Come funziona', h2='Tre passi')
 + sez(punti('Solo materie prime italiane: niente prodotti importati', 'Accanto al tuo distributore, non al suo posto', 'Produttori con un check-up su documenti, etichette e lotti: utile per la tua qualifica fornitori', 'Una <a href="riga-menu.html">riga per il menu</a> pronta, con nome e luogo del produttore', 'Il nostro margine è dichiarato'),
       occhiello='In più', h2='Pensato per chi cucina')
 + '<section class="sez verde-b" id="richiesta"><div class="wrap due"><div><p class="occhiello">Richiesta</p><h2>Dicci cosa ti serve</h2>'
   '<p class="grande">La rete è in costruzione: nessun prodotto è ancora in vendita. Raccogliamo le richieste e ti scriviamo quando ci sono produttori pronti per te.</p></div>'
   '<div class="modulo"><form class="form" action="invia.php" method="post">'
   '<div class="hp" aria-hidden="true"><label>Lascia vuoto<input type="text" name="sito_web" tabindex="-1" autocomplete="off"></label></div>'
   '<fieldset class="full radio"><legend>Vorrei</legend><label><input type="radio" name="tipo" value="campione" checked> un campione</label><label><input type="radio" name="tipo" value="ordine"> ordinare</label></fieldset>'
   '<label>Nome del locale<input type="text" name="nome_locale" required maxlength="120"></label>'
   '<label>Tipo di locale<select name="tipo_locale"><option>Ristorante</option><option>Bar</option><option>Hotel</option><option>Altro</option></select></label>'
   '<label>Referente<input type="text" name="referente" required maxlength="120" autocomplete="name"></label>'
   '<label>Email<input type="email" name="email" required maxlength="160" autocomplete="email"></label>'
   '<label class="full">Prodotti che ti interessano<textarea name="prodotti" rows="3" required maxlength="2000" placeholder="Es. olio in latta, pecorino, legumi"></textarea></label>'
   '<label class="full">Zona di consegna<input type="text" name="zona" required maxlength="160" placeholder="Es. Roma, Trastevere"></label>'
   '<label class="full check"><input type="checkbox" name="consenso" value="si" required><span>Ho letto l\'<a href="privacy.html">informativa privacy</a>.</span></label>'
   '<button class="btn miele full" type="submit">Invia la richiesta →</button><p class="full piccolo" style="margin:0">Rispondiamo per email. Nessun pagamento online.</p></form></div></div></section>'
 + sez(faq(('Posso già ordinare?', 'Non ancora. Puoi dirci cosa cerchi e chiedere un campione: ti scriviamo appena ci sono produttori pronti nella tua zona.'),
           ('Devo lasciare il mio distributore?', 'No. Filo Corto lo affianca, per i prodotti che il distributore non ha.'),
           ('Come si paga?', 'A fattura, direttamente al produttore.'),
           ('Vendete ai privati?', 'No: solo a ristoranti, bar e hotel.')), occhiello='Domande', h2='In breve'))
scrivi('cucine', 'Prodotti del Lazio per ristoranti, bar e hotel | Filo Corto',
       'Formaggi, olio, conserve, legumi e miele da piccoli produttori del Lazio, per ristoranti, bar e hotel. Campione gratuito, prezzi e consegne per iscritto.', cuc, menu='cucine.html')

# ---------------- CHECK-UP ----------------
chk = (capo('Check-up', 'Il check-up: sei pronto per le cucine?',
            'Una visita in azienda, la stessa lista di controllo per tutti, un rapporto scritto. Gratis per i primi produttori.',
            '<div class="btns" style="margin-top:26px"><a class="btn verde" href="produttori.html#candidati">Candidati →</a></div>')
 + sez('<p class="grande" style="max-width:820px;margin-bottom:30px">Ristoranti e hotel devono qualificare i fornitori nel loro piano HACCP. Prima di comprare controllano documenti, etichette e rintracciabilità. Il check-up ti prepara a questo.</p>'
       + tessere(('Documenti', 'Registrazione sanitaria, piano di autocontrollo, registri, formazione.', False),
                 ('Prodotto', 'Origine delle materie prime, lotti, etichette, allergeni, imballaggi, rintracciabilità.', True),
                 ('Consegne e prezzi', 'Trasporto, giorni e tempi, listino, quantità garantite.', False)),
       cls='bianca', occhiello='Cosa guardiamo', h2='Tre aree, quattordici punti')
 + sez(passi(('La visita', 'In azienda, con la lista di controllo.'),
             ('La prova del lotto', 'Scegliamo un prodotto venduto e risaliamo, carte alla mano, a lotto, materie prime e clienti.'),
             ('Il rapporto', 'Scritto, con le priorità e un esito: pronto, quasi pronto, da preparare.')), cls='scura', occhiello='Come funziona', h2='Tre passi')
 + sez('<p class="grande" style="max-width:820px">Lo fa Valerio Semeraro, Food Specialist e consulente HACCP. Il check-up è una valutazione per la rete: non è una certificazione, non sostituisce i controlli ufficiali e non garantisce vendite.</p>'
       '<p style="margin-top:20px"><a href="guide/documenti-per-vendere-ai-ristoranti.html">Intanto leggi la guida ai documenti →</a></p>', occhiello='Chi lo fa', h2='Patti chiari anche qui')
 + CTA)
scrivi('check-up', 'Check-up per piccoli produttori: pronto per ristoranti e hotel? | Filo Corto',
       'Visita in azienda, lista di controllo uguale per tutti e rapporto scritto: documenti, lotti, etichette, consegne. Gratis per i primi produttori del Lazio.', chk, menu='check-up.html')

# ---------------- COME FUNZIONA ----------------
cf = (capo('Come funziona', 'Come funziona',
           'Niente magazzino, niente acquisti per rivendere. Mettiamo in contatto chi produce e chi cucina, con le stesse regole per tutti.')
 + sez('<div class="due"><div><h2 style="margin-bottom:18px">Se produci</h2>' + passi(('Ti candidi', 'Due minuti online.'), ('Scheda e check-up', 'Prodotti, prezzi, consegne; poi la visita.'), ('Entri nel listino', 'E partecipi alla prova con le prime cucine.')) +
       '</div><div><h2 style="margin-bottom:18px">Se cucini</h2>' + passi(('Scegli', 'Dal listino unico.'), ('Assaggi', 'Un campione, gratis.'), ('Ordini', 'Ogni produttore consegna e ti fattura.')) + '</div></div>', cls='bianca')
 + sez(PATTI, occhiello='Le regole', h2='Uguali per tutti')
 + sez('<p class="grande" style="max-width:820px">Le consegne sono il punto più delicato. Le definiamo con i primi produttori durante la prova: l\'obiettivo è una consegna unica in giorni fissi, partendo dai prodotti che non hanno bisogno del freddo.</p>'
       '<p style="margin-top:20px">Filo Corto non è un e-commerce per privati, non è un grossista e non è un ente di certificazione. Lavoriamo solo nel Lazio.</p>', cls='scura', occhiello='Consegne', h2='Il punto più delicato')
 + CTA)
scrivi('come-funziona', 'Come funziona Filo Corto: produttori del Lazio e cucine | Filo Corto',
       'Come funziona Filo Corto: il produttore si candida e fa il check-up, la cucina assaggia e ordina, il produttore consegna e fattura. Regole uguali per tutti.', cf, menu='come-funziona.html')

# ---------------- CHI SIAMO ----------------
cs = (capo('Chi siamo', 'Un gruppo di appassionati del cibo vero.',
           'Cibo che ha un nome, un luogo e il volto di chi lo fa. Vogliamo portarlo nelle cucine del Lazio.')
 + sez('<p class="grande" style="max-width:820px">Lavoriamo in cucina, in sala e nella scelta dei fornitori. Da anni vediamo lo stesso problema: ottimi piccoli produttori da una parte, cucine che comprano solo dai grandi distributori dall\'altra. Non è la qualità che manca: sono consegne puntuali, prezzi chiari, merce sempre disponibile. Filo Corto nasce per accorciare questa distanza.</p>'
       '<p class="grande" style="max-width:820px;margin-top:18px">E per difendere una cosa semplice: il prodotto vero delle nostre terre. Materie prime italiane, fatte da persone che si possono conoscere. Il made in Italy vive se arriva sulle tavole. Partiamo dal Lazio, guardando a tutta Italia.</p>'
       '<p class="grande" style="max-width:820px;margin-top:18px">E per difendere una cosa semplice: il prodotto vero delle nostre terre. Materie prime italiane, fatte da persone che si possono conoscere. Il made in Italy vive se arriva sulle tavole. Partiamo dal Lazio, guardando a tutta Italia.</p>', cls='bianca', occhiello='Dalle cucine', h2='Non da un ufficio')
 + sez(tessere(('Si sa chi lo fa', 'Un\'azienda con nome e indirizzo, che puoi visitare.', False),
               ('È italiano', 'Materie prime italiane, niente prodotti importati.', True),
               ('Si può raccontare', 'Una storia vera, da scrivere nel menu.', False),
               ('È in regola', 'Documenti, etichette e lotti in ordine.', True)), occhiello='Cibo vero', h2='Cosa intendiamo')
 + sez('<p class="grande" style="max-width:820px">Il progetto è curato da Valerio Semeraro, Food Specialist e consulente HACCP: segue le adesioni dei produttori e fa i check-up in azienda. Scrivici a <a href="mailto:info@ilfilocorto.it" style="color:var(--miele-chiaro)">info@ilfilocorto.it</a>.</p>', cls='scura', occhiello='Chi cura il progetto', h2='Valerio Semeraro')
 + CTA)
scrivi('chi-siamo', 'Chi siamo: appassionati del cibo vero | Filo Corto',
       'Filo Corto nasce dalle cucine: un gruppo di appassionati del cibo vero che vuole portare i piccoli produttori del Lazio in ristoranti, bar e hotel.', cs, menu='chi-siamo.html')

# ---------------- DOMANDE ----------------
FP = [('Aderire costa qualcosa?', 'No. Candidatura e adesione sono gratuite, senza impegno. Esci quando vuoi.'),
      ('Mi garantite delle vendite?', 'No. Oggi raccogliamo le adesioni. Quando la rete parte lavoriamo perché le cucine provino e riordinino, ma la scelta è loro.'),
      ('Quanto guadagna Filo Corto?', 'Se la rete vende, un margine. È scritto nella scheda di adesione prima di qualsiasi ordine, ed è dichiarato anche alle cucine.'),
      ('Chi fattura alla cucina?', 'Tu, il produttore. E la cucina paga te.'),
      ('Devo consegnare io?', 'Giorni e modi si decidono con i primi produttori durante la prova. L\'obiettivo è una consegna unica alle cucine.'),
      ('Cos\'è il check-up?', 'Una visita in azienda con una lista di controllo su documenti, etichette, lotti, trasporto, prezzi e continuità. Gratis per i primi produttori. Non è una certificazione né un controllo ufficiale.'),
      ('Produco fuori dal Lazio: posso candidarmi?', 'Per ora lavoriamo solo nel Lazio. Scrivici comunque: teniamo il tuo contatto per quando la rete si allarga.'),
      ('Accettate prodotti con materie prime estere?', 'No. Nella rete entrano solo prodotti fatti con materie prime coltivate o allevate in Italia, senza prodotti importati da altri Paesi, UE o extra UE. Lo guardiamo insieme durante il check-up.'),
      ('Quali prodotti cercate?', 'Per iniziare, prodotti che si conservano e viaggiano bene: formaggi stagionati, olio, conserve, legumi e cereali, miele, vino e birra, farine e pasta secca, salumi stagionati.')]
FC = [('Posso già ordinare?', 'Non ancora. Dicci cosa cerchi e chiedi un campione: ti scriviamo quando ci sono produttori pronti nella tua zona.'),
      ('Devo lasciare il mio distributore?', 'No. Filo Corto lo affianca, per i prodotti dei piccoli produttori che il distributore non ha.'),
      ('Da dove vengono i prodotti?', 'Da piccoli produttori del Lazio, con materie prime italiane. Su ogni prodotto trovi chi lo fa e dove.'),
      ('Come si paga?', 'A fattura, direttamente al produttore. Nessun pagamento online.'),
      ('Vendete ai privati?', 'No: solo a ristoranti, bar e hotel.')]
dom = (capo('Domande', 'Domande frequenti', 'Le risposte brevi a quello che ci chiedono di più.')
 + sez(faq(*FP), cls='bianca', occhiello='Se produci', h2='Per i produttori')
 + sez(faq(*FC), occhiello='Se cucini', h2='Per le cucine') + CTA)
import json
faqjson = json.dumps({'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in FP + FC]}, ensure_ascii=False)
scrivi('domande', 'Domande frequenti: produttori e cucine | Filo Corto',
       'Quanto costa aderire, chi fattura, cos\'è il check-up, si può già ordinare: le risposte brevi per produttori del Lazio e per ristoranti, bar e hotel.', dom, menu='', extra=f'schema: {faqjson}\n')
print('ok')
