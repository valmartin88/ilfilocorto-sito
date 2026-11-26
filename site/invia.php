<?php
// Filo Corto – riceve i moduli del sito, li inoltra a info@ilfilocorto.it
// e manda a chi ha scritto un'email di conferma con i prossimi passi.
// Nessun dato salvato sul server: solo email.

declare(strict_types=1);

const DESTINATARIO = 'info@ilfilocorto.it';
const MITTENTE = 'Filo Corto <info@ilfilocorto.it>';

function torna(string $pagina): void {
    header('Location: ' . $pagina, true, 303);
    exit;
}

// Pulisce un campo: niente a capo nei campi brevi (evita intestazioni email false), lunghezza massima.
function campo(string $nome, int $max = 200, bool $multiriga = false): string {
    $v = isset($_POST[$nome]) && is_string($_POST[$nome]) ? trim($_POST[$nome]) : '';
    if (!$multiriga) {
        $v = preg_replace('/[\r\n]+/', ' ', $v);
    }
    return mb_substr($v, 0, $max);
}

function spedisci(string $a, string $oggetto, string $testo, string $rispondiA): bool {
    $intestazioni = implode("\r\n", [
        'From: ' . MITTENTE,
        'Reply-To: ' . $rispondiA,
        'MIME-Version: 1.0',
        'Content-Type: text/plain; charset=UTF-8',
        'Content-Transfer-Encoding: 8bit',
    ]);
    return mail($a, '=?UTF-8?B?' . base64_encode($oggetto) . '?=', $testo, $intestazioni, '-f info@ilfilocorto.it');
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    torna('./');
}
// Trappola per i robot: il campo nascosto deve restare vuoto.
if (campo('sito_web') !== '') {
    torna('grazie.html');
}

$tipo = campo('tipo', 20);
$tipi = [
    'campione'   => 'Cucina – richiesta campione',
    'ordine'     => 'Cucina – richiesta ordine',
    'produttore' => 'Produttore – candidatura',
    'scheda'     => 'Produttore – scheda di adesione',
];
if (!isset($tipi[$tipo]) || campo('consenso', 5) !== 'si') {
    torna('errore.html');
}
$email = campo('email', 160);
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    torna('errore.html');
}

if ($tipo === 'scheda') {
    if (campo('patti', 5) !== 'si') {
        torna('errore.html');
    }
    $righe = [
        'Azienda'                  => campo('azienda', 120),
        'Referente'                => campo('referente', 120),
        'Email'                    => $email,
        'Comune e provincia'       => campo('comune', 120),
        'Registrazione sanitaria'  => campo('registrazione', 20),
        'Prodotti, formati, prezzi' => "\n" . campo('prodotti', 3000, true),
        'Ordine minimo'            => campo('ordine_minimo', 120),
        'Validità dei prezzi'      => campo('validita', 120),
        'Giorni di consegna'       => campo('giorni', 160),
        'Tempo ordine-consegna'    => campo('tempi', 120),
        'Come consegna oggi'       => campo('consegna', 120),
        'Quantità a settimana'     => campo('quantita', 200),
        'Mesi di disponibilità'    => campo('mesi', 160),
        'Note'                     => campo('note', 1500, true),
        'Patti chiari accettati'   => 'sì',
    ];
    $obbligatori = ['Azienda', 'Referente', 'Comune e provincia', 'Giorni di consegna', 'Quantità a settimana'];
    if (trim($righe['Prodotti, formati, prezzi']) === '') {
        torna('errore.html');
    }
} elseif ($tipo === 'produttore') {
    $righe = [
        'Azienda'            => campo('azienda', 120),
        'Referente'          => campo('referente', 120),
        'Email'              => $email,
        'Comune'             => campo('comune', 120),
        'Cosa produce'       => campo('prodotti', 2000, true),
        'Come consegna oggi' => campo('consegna', 120),
    ];
    $obbligatori = ['Azienda', 'Referente', 'Comune', 'Cosa produce'];
} else {
    $righe = [
        'Locale'           => campo('nome_locale', 120),
        'Tipo di locale'   => campo('tipo_locale', 40),
        'Referente'        => campo('referente', 120),
        'Email'            => $email,
        'Prodotti'         => campo('prodotti', 2000, true),
        'Zona di consegna' => campo('zona', 160),
    ];
    $obbligatori = ['Locale', 'Referente', 'Prodotti', 'Zona di consegna'];
}
foreach ($obbligatori as $k) {
    if ($righe[$k] === '') {
        torna('errore.html');
    }
}

$testo = $tipi[$tipo] . "\n\n";
foreach ($righe as $k => $v) {
    $testo .= $k . ': ' . $v . "\n";
}
$testo .= "\nConsenso privacy: sì\nInviato il: " . date('d/m/Y H:i') . "\n";
$nome = $righe['Locale'] ?? $righe['Azienda'];

$ok = spedisci(DESTINATARIO, 'Filo Corto – ' . $tipi[$tipo] . ' – ' . $nome, $testo, $email);

// Email di conferma a chi ha scritto: testo fisso, senza riportare i dati inviati.
if ($ok) {
    $firma = "\n\nValerio Semeraro\nFilo Corto – dal produttore alla cucina\nhttps://ilfilocorto.it\n\nQuesta è un'email automatica di conferma. Per qualsiasi domanda puoi rispondere a questo messaggio.";
    if ($tipo === 'produttore') {
        $conferma = "Buongiorno,\n\ngrazie per la candidatura a Filo Corto: l'abbiamo ricevuta.\n\nIl prossimo passo è la scheda di adesione. Servono circa dieci minuti: ci dici quali prodotti proponi, a che prezzo, in quali giorni puoi consegnare e quanta merce puoi garantire ogni settimana.\n\nLa trovi qui: https://ilfilocorto.it/scheda.html\n\nTi ricordiamo i patti chiari della rete: aderire è gratuito, non ti impegna e non promette vendite. Fatturi tu, direttamente alla cucina, e il margine di Filo Corto ti viene comunicato per iscritto prima di qualsiasi ordine.\n\nOggi raccogliamo le adesioni. Quando partiamo con i check-up in azienda e con la prova con le prime cucine, ti scriviamo noi.\n\nSe intanto vuoi capire a che punto sei, c'è una prova di dieci domande: https://ilfilocorto.it/prova.html";
        $oggettoConferma = 'Filo Corto – candidatura ricevuta: il prossimo passo';
    } elseif ($tipo === 'scheda') {
        $conferma = "Buongiorno,\n\ngrazie: abbiamo ricevuto la tua scheda di adesione a Filo Corto.\n\nOggi raccogliamo le adesioni dei produttori del Lazio. Quando partiamo con i check-up in azienda e con la prova con le prime cucine, ti scriviamo noi per fissare la visita.\n\nSe nel frattempo cambiano prodotti, prezzi o giorni di consegna, basta rispondere a questa email.";
        $oggettoConferma = 'Filo Corto – scheda di adesione ricevuta';
    } else {
        $conferma = "Buongiorno,\n\ngrazie: abbiamo ricevuto la tua richiesta.\n\nFilo Corto è una rete in costruzione: oggi raccogliamo le adesioni dei produttori del Lazio e le richieste delle cucine. Nessun prodotto è ancora in vendita. Ti scriviamo appena ci sono produttori pronti per i prodotti e per la zona che ci hai indicato.\n\nIntanto, se vuoi scrivere il nome dei tuoi fornitori nel menu, c'è uno strumento gratuito: https://ilfilocorto.it/riga-menu.html";
        $oggettoConferma = 'Filo Corto – richiesta ricevuta';
    }
    spedisci($email, $oggettoConferma, $conferma . $firma, DESTINATARIO);
}
torna($ok ? 'grazie.html' : 'errore.html');
