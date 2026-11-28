<?php
// Filo Corto – foto del sito.
// Le foto stanno nella cartella foto/ come file <nome>-<formato>.jpg, messi a mano nell'archivio (vedi README).
// Questo file le serve; se una foto non c'è ancora, al suo posto esce un disegno del sito.
// Non scarica niente e non si collega a siti esterni.
//
//   foto.php?f=ulivo&v=banda   -> la foto, oppure il disegno
//   foto.php?stato=1           -> elenco di cosa c'è e cosa manca (solo testo)

$FORMATI = ['banda' => [1600, 640], 'alto' => [900, 1000], 'largo' => [900, 600]];
// Le combinazioni usate dalle pagine (nome, formato). Gli autori delle foto sono in strumenti/pagine.py (FOTO_CREDITI).
$IN_USO = [['ulivo', 'alto'], ['mani', 'largo'], ['chef', 'largo'], ['olive', 'banda'], ['chef', 'banda'], ['barattoli', 'banda'],
           ['cassette', 'banda'], ['mercato', 'banda'], ['civita', 'banda'], ['legumi', 'banda']];
// Colori del disegno che esce quando la foto non c'è (fondo, onde): uno per foto, così tre riquadri vicini non sono uguali.
$TINTE = [['#2f5d3a', '#477a52'], ['#12302b', '#1f4a42'], ['#e9b565', '#d9a04e']];
$TINTA = ['ulivo' => 0, 'mani' => 2, 'chef' => 1, 'olive' => 0, 'barattoli' => 2, 'cassette' => 1, 'mercato' => 0, 'civita' => 1, 'legumi' => 2];
$DIR = __DIR__ . '/foto';

function pronta(string $nome, string $v): bool {
    global $DIR;
    $f = $DIR . '/' . $nome . '-' . $v . '.jpg';
    return is_file($f) && filesize($f) > 8000;
}

if (isset($_GET['stato']) || isset($_GET['prepara'])) {
    header('Content-Type: text/plain; charset=utf-8'); header('X-Robots-Tag: noindex'); header('Cache-Control: no-store');
    echo "Filo Corto – foto\n\n";
    foreach ($IN_USO as [$nome, $v]) {
        echo pronta($nome, $v) ? "ok      $nome ($v) " . round(filesize("$DIR/$nome-$v.jpg") / 1024) . " KB\n" : "manca   $nome ($v)\n";
    }
    echo "\nLe foto si aggiungono a mano nell'archivio (cartella site/foto/). Dove manca la foto il sito mostra un disegno.\n";
    exit;
}

$nome = (string)($_GET['f'] ?? ''); $v = (string)($_GET['v'] ?? 'banda');
if (!isset($TINTA[$nome]) || !isset($FORMATI[$v])) { http_response_code(404); exit; }
if (pronta($nome, $v)) {
    header('Content-Type: image/jpeg'); header('Cache-Control: public, max-age=2592000');
    header('Content-Length: ' . filesize("$DIR/$nome-$v.jpg"));
    readfile("$DIR/$nome-$v.jpg");
    exit;
}
// La foto non c'è: disegno del sito, che copre qualsiasi riquadro.
[$w, $h] = $FORMATI[$v];
[$fondo, $onde] = $TINTE[$TINTA[$nome]];
$chiaro = $fondo === '#e9b565';
header('Content-Type: image/svg+xml; charset=utf-8'); header('Cache-Control: public, max-age=900');
echo '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ' . $w . ' ' . $h . '" preserveAspectRatio="xMidYMid slice">'
   . '<rect width="' . $w . '" height="' . $h . '" fill="' . $fondo . '"/>'
   . '<g fill="none" stroke="' . $onde . '" stroke-width="14"><path d="M-50 ' . ($h * .78) . ' C ' . ($w * .2) . ' ' . ($h * .7) . ', ' . ($w * .4) . ' ' . ($h * .9) . ', ' . ($w * .62) . ' ' . ($h * .8) . ' S ' . ($w * .9) . ' ' . ($h * .7) . ', ' . ($w + 50) . ' ' . ($h * .76) . '"/>'
   . '<path d="M-50 ' . ($h * .92) . ' C ' . ($w * .25) . ' ' . ($h * .84) . ', ' . ($w * .45) . ' ' . ($h * 1.0) . ', ' . ($w * .66) . ' ' . ($h * .92) . ' S ' . ($w * .9) . ' ' . ($h * .86) . ', ' . ($w + 50) . ' ' . ($h * .9) . '"/></g>'
   . '<g transform="translate(' . ($w * .5 - 150) . ' ' . ($h * .5 - 150) . ')">'
   . '<path d="M96 60 C 150 60, 200 96, 214 170" fill="none" stroke="' . ($chiaro ? '#1f2420' : '#e9b565') . '" stroke-width="10" stroke-linecap="round" stroke-dasharray="0.1 22"/>'
   . '<path d="M0 110 C 0 50, 38 10, 104 8 C 104 70, 64 110, 0 110 Z" fill="' . ($chiaro ? '#2f5d3a' : '#8fc49a') . '" stroke="#1f2420" stroke-width="4"/><path d="M12 100 L 92 22" stroke="#1f2420" stroke-width="4" stroke-linecap="round"/>'
   . '<circle cx="236" cy="236" r="50.5" fill="#F2F4F0" stroke="#E8692C" stroke-width="18.9"/><circle cx="236" cy="236" r="17.5" fill="#12302B"/></g></svg>';
