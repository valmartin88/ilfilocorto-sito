<?php
// Filo Corto – foto del sito.
// Il server scarica ogni foto una volta sola (foto con licenza libera: vedi crediti.html) e poi la serve dalla cartella foto/.
// I visitatori non si collegano mai a siti esterni. Se una foto non è disponibile, al suo posto esce un disegno del sito.
//
//   foto.php?f=ulivo&v=banda   -> la foto, nel formato chiesto
//   foto.php?stato=1           -> elenco di cosa c'è e cosa manca (solo testo)
//   foto.php?prepara=1         -> scarica quelle che mancano (poche per volta) e mostra l'elenco

$FOTO = [               // nome => codice della foto su Unsplash (licenza Unsplash: uso libero, anche commerciale)
    'ulivo'     => 'hnkdeJJoY-A',   // olive sul ramo dopo la pioggia, Toscana – The Now Time
    'olive'     => '-8nbY8W2YEE',   // olive verdi sul ramo – Janine Joles
    'mani'      => 'fp1x-X7DwDs',   // mani con patate appena raccolte – JESHOOTS.COM
    'chef'      => 'MaWMfm-HCqQ',   // chef che impiatta – Urban Gyllström
    'barattoli' => 'NrqKwJ1KPo8',   // barattoli su uno scaffale, Firenze – Artem Kostelnyuk
    'cassette'  => 'XPltBlxfChk',   // verdure in cassette di legno al mercato – Noah Buisson
    'mercato'   => 'sgQTbIU43Mg',   // banco di un mercato rionale, Roma San Giovanni – Ágatha Depiné
    'civita'    => 'aVWzRGYLjZI',   // Civita di Bagnoregio (VT) – Pablo Allendes
    'legumi'    => 't4X660oKiYs',   // legumi secchi al mercato – Shelley Pauls
];
$FORMATI = ['banda' => [1600, 640], 'alto' => [900, 1000], 'largo' => [900, 600]];
// Le combinazioni usate dalle pagine: «prepara» scarica queste.
$IN_USO = [['ulivo', 'alto'], ['mani', 'largo'], ['chef', 'largo'], ['olive', 'banda'], ['chef', 'banda'], ['barattoli', 'banda'],
           ['cassette', 'banda'], ['mercato', 'banda'], ['civita', 'banda'], ['legumi', 'banda']];

$DIR = __DIR__ . '/foto';
const RIPROVA_DOPO = 6 * 3600;   // dopo un errore, si riprova dopo sei ore
const UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36';

function chiedi(string $url, bool $segui): array {
    if (function_exists('curl_init')) {
        $ch = curl_init($url);
        curl_setopt_array($ch, [CURLOPT_RETURNTRANSFER => true, CURLOPT_HEADER => true, CURLOPT_FOLLOWLOCATION => $segui, CURLOPT_MAXREDIRS => 5,
            CURLOPT_CONNECTTIMEOUT => 8, CURLOPT_TIMEOUT => 25, CURLOPT_USERAGENT => UA,
            CURLOPT_HTTPHEADER => ['Accept: text/html,image/jpeg,image/*;q=0.9,*/*;q=0.8', 'Accept-Language: it-IT,it;q=0.9,en;q=0.6']]);
        $r = curl_exec($ch);
        if ($r === false) { $e = curl_error($ch); curl_close($ch); return [0, '', '', 'curl: ' . $e]; }
        $stato = (int)curl_getinfo($ch, CURLINFO_RESPONSE_CODE); $n = (int)curl_getinfo($ch, CURLINFO_HEADER_SIZE); curl_close($ch);
        return [$stato, substr($r, 0, $n), substr($r, $n), ''];
    }
    $ctx = stream_context_create(['http' => ['follow_location' => $segui ? 1 : 0, 'max_redirects' => 5, 'ignore_errors' => true, 'timeout' => 25, 'header' => "User-Agent: " . UA . "\r\nAccept: */*\r\n"]]);
    $corpo = @file_get_contents($url, false, $ctx);
    $testa = implode("\n", $http_response_header ?? []);
    if ($corpo === false && $testa === '') return [0, '', '', 'rete non raggiungibile'];
    preg_match_all('/^HTTP\/\S+\s+(\d+)/m', $testa, $m);
    return [(int)(end($m[1]) ?: 0), $testa, (string)$corpo, ''];
}

// Trova l'indirizzo dell'immagine originale: prima dalla pagina di download, poi dalla pagina della foto.
function origine(string $codice): array {
    [$s, $testa, , $err] = chiedi('https://unsplash.com/photos/' . $codice . '/download?force=true', false);
    if (preg_match('/^location:\s*(https:\/\/images\.unsplash\.com\/[^\s?]+)/mi', $testa, $m)) return [$m[1], ''];
    $primo = $err ?: ('download: risposta ' . $s);
    [$s, , $corpo, $err] = chiedi('https://unsplash.com/photos/' . $codice, true);
    if (preg_match('/https:\/\/images\.unsplash\.com\/(?:photo|flagged\/photo|reserve)[A-Za-z0-9_\/.-]*/', $corpo, $m)) return [$m[0], ''];
    return ['', $primo . '; pagina: ' . ($err ?: 'risposta ' . $s)];
}

function scarica(string $nome, string $v): string {   // restituisce '' se va bene, altrimenti il motivo
    global $FOTO, $FORMATI, $DIR;
    if (!is_dir($DIR) && !@mkdir($DIR, 0755)) return 'cartella foto non scrivibile';
    [$base, $err] = origine($FOTO[$nome]);
    if ($base === '') return $err;
    [$w, $h] = $FORMATI[$v];
    [$s, , $img, $err] = chiedi($base . '?fm=jpg&q=72&w=' . $w . '&h=' . $h . '&fit=crop&crop=entropy', true);
    if ($err) return 'immagine: ' . $err;
    if ($s !== 200) return 'immagine: risposta ' . $s;
    if (substr($img, 0, 3) !== "\xFF\xD8\xFF") return 'immagine: non è una foto JPEG';
    if (strlen($img) < 8000 || strlen($img) > 3500000) return 'immagine: dimensione anomala (' . strlen($img) . ' byte)';
    $tmp = $DIR . '/' . $nome . '-' . $v . '.' . getmypid() . '.tmp';
    if (@file_put_contents($tmp, $img, LOCK_EX) === false) return 'cartella foto non scrivibile';
    @rename($tmp, $DIR . '/' . $nome . '-' . $v . '.jpg');
    @unlink($DIR . '/' . $nome . '-' . $v . '.no');
    return '';
}

function pronta(string $nome, string $v): bool { global $DIR; $f = $DIR . '/' . $nome . '-' . $v . '.jpg'; return is_file($f) && filesize($f) > 8000; }

function prova(string $nome, string $v): string {   // scarica se manca, rispettando l'attesa dopo un errore
    global $DIR;
    if (pronta($nome, $v)) return '';
    $no = $DIR . '/' . $nome . '-' . $v . '.no';
    if (is_file($no) && time() - filemtime($no) < RIPROVA_DOPO) return 'in attesa (' . trim((string)@file_get_contents($no)) . ')';
    $err = scarica($nome, $v);
    if ($err !== '' && is_dir($DIR)) @file_put_contents($no, $err);
    return $err;
}

if (isset($_GET['stato']) || isset($_GET['prepara'])) {
    header('Content-Type: text/plain; charset=utf-8'); header('X-Robots-Tag: noindex'); header('Cache-Control: no-store');
    @set_time_limit(60);
    $fatte = 0; $inizio = time();
    echo "Filo Corto – foto\n\n";
    foreach ($IN_USO as [$nome, $v]) {
        if (pronta($nome, $v)) { echo "ok      $nome ($v) " . round(filesize("$DIR/$nome-$v.jpg") / 1024) . " KB\n"; continue; }
        if (isset($_GET['prepara']) && $fatte < 4 && time() - $inizio < 35) {
            if (isset($_GET['forza'])) @unlink("$DIR/$nome-$v.no");
            $err = prova($nome, $v); $fatte++;
            echo ($err === '' ? "nuova   $nome ($v) " . round(filesize("$DIR/$nome-$v.jpg") / 1024) . " KB" : "errore  $nome ($v): $err") . "\n";
        } else {
            $no = "$DIR/$nome-$v.no";
            echo "manca   $nome ($v)" . (is_file($no) ? ': ' . trim((string)@file_get_contents($no)) : '') . "\n";
        }
    }
    echo "\nIn mancanza della foto il sito mostra un disegno al suo posto.\n";
    exit;
}

$nome = (string)($_GET['f'] ?? ''); $v = (string)($_GET['v'] ?? 'banda');
if (!isset($FOTO[$nome]) || !isset($FORMATI[$v])) { http_response_code(404); exit; }
@set_time_limit(45);
if (prova($nome, $v) === '') {
    header('Content-Type: image/jpeg'); header('Cache-Control: public, max-age=2592000');
    header('Content-Length: ' . filesize("$DIR/$nome-$v.jpg"));
    readfile("$DIR/$nome-$v.jpg");
    exit;
}
// La foto non c'è: disegno del sito, che copre qualsiasi riquadro.
[$w, $h] = $FORMATI[$v];
header('Content-Type: image/svg+xml; charset=utf-8'); header('Cache-Control: public, max-age=900');
echo '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ' . $w . ' ' . $h . '" preserveAspectRatio="xMidYMid slice">'
   . '<rect width="' . $w . '" height="' . $h . '" fill="#2f5d3a"/>'
   . '<g fill="none" stroke="#477a52" stroke-width="14"><path d="M-50 ' . ($h * .78) . ' C ' . ($w * .2) . ' ' . ($h * .7) . ', ' . ($w * .4) . ' ' . ($h * .9) . ', ' . ($w * .62) . ' ' . ($h * .8) . ' S ' . ($w * .9) . ' ' . ($h * .7) . ', ' . ($w + 50) . ' ' . ($h * .76) . '"/>'
   . '<path d="M-50 ' . ($h * .92) . ' C ' . ($w * .25) . ' ' . ($h * .84) . ', ' . ($w * .45) . ' ' . ($h * 1.0) . ', ' . ($w * .66) . ' ' . ($h * .92) . ' S ' . ($w * .9) . ' ' . ($h * .86) . ', ' . ($w + 50) . ' ' . ($h * .9) . '"/></g>'
   . '<g transform="translate(' . ($w * .5 - 150) . ' ' . ($h * .5 - 150) . ')">'
   . '<path d="M96 60 C 150 60, 200 96, 214 170" fill="none" stroke="#e9b565" stroke-width="10" stroke-linecap="round" stroke-dasharray="0.1 22"/>'
   . '<path d="M0 110 C 0 50, 38 10, 104 8 C 104 70, 64 110, 0 110 Z" fill="#8fc49a" stroke="#1f2420" stroke-width="4"/><path d="M12 100 L 92 22" stroke="#1f2420" stroke-width="4" stroke-linecap="round"/>'
   . '<circle cx="236" cy="236" r="50.5" fill="#F2F4F0" stroke="#E8692C" stroke-width="18.9"/><circle cx="236" cy="236" r="17.5" fill="#12302B"/></g></svg>';
