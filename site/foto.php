<?php
// Foto del sito (licenza Unsplash, uso commerciale libero). Il server le scarica una volta sola
// e poi le serve dalla cartella foto/: i visitatori non si collegano mai a siti esterni.
$foto = [
    'uliveto'  => 'hnkdeJJoY-A',   // olive dopo la pioggia, Italia
    'mani'     => 'fp1x-X7DwDs',   // mani di contadino con patate appena raccolte
    'formaggi' => '0aE3EGmC9kw',   // forme di formaggio in stagionatura, Modena
    'legumi'   => 't4X660oKiYs',   // legumi al mercato
    'chef'     => 'MaWMfm-HCqQ',   // chef che impiatta
];
$f = $_GET['f'] ?? '';
if (!isset($foto[$f])) { http_response_code(404); exit; }
$file = __DIR__ . '/foto/' . $f . '.jpg';
if (!is_file($file) || filesize($file) < 10000) {
    if (!is_dir(__DIR__ . '/foto')) mkdir(__DIR__ . '/foto', 0755);
    $prima = 'https://unsplash.com/photos/' . $foto[$f] . '/download?force=true';
    $loc = '';
    if (function_exists('curl_init')) {
        $ch = curl_init($prima);
        curl_setopt_array($ch, [CURLOPT_RETURNTRANSFER => true, CURLOPT_HEADER => true, CURLOPT_NOBODY => true, CURLOPT_FOLLOWLOCATION => false, CURLOPT_TIMEOUT => 20, CURLOPT_USERAGENT => 'ilfilocorto.it']);
        $r = (string)curl_exec($ch); curl_close($ch);
    } else {
        $ctx = stream_context_create(['http' => ['method' => 'GET', 'follow_location' => 0, 'ignore_errors' => true, 'timeout' => 20, 'header' => "User-Agent: ilfilocorto.it\r\n"]]);
        @file_get_contents($prima, false, $ctx, 0, 1);
        $r = implode("\n", $http_response_header ?? []);
    }
    if (!preg_match('/^location:\s*(https:\/\/images\.unsplash\.com\/\S+)/mi', $r, $m)) { http_response_code(502); exit; }
    $url = trim($m[1]); $url .= (strpos($url, '?') === false ? '?' : '&') . 'w=1600&q=70&fm=jpg';
    if (function_exists('curl_init')) {
        $ch = curl_init($url);
        curl_setopt_array($ch, [CURLOPT_RETURNTRANSFER => true, CURLOPT_FOLLOWLOCATION => true, CURLOPT_TIMEOUT => 30, CURLOPT_USERAGENT => 'ilfilocorto.it']);
        $img = curl_exec($ch); curl_close($ch);
    } else {
        $img = @file_get_contents($url, false, stream_context_create(['http' => ['timeout' => 30, 'header' => "User-Agent: ilfilocorto.it\r\n"]]));
    }
    if (!$img || substr($img, 0, 3) !== "\xFF\xD8\xFF" || strlen($img) > 4000000) { http_response_code(502); exit; }
    file_put_contents($file, $img, LOCK_EX);
}
header('Content-Type: image/jpeg');
header('Cache-Control: public, max-age=2592000');
readfile($file);
