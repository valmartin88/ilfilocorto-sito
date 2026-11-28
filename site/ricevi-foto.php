<?php
// Filo Corto – ricezione una tantum delle foto del sito (28/11/2026).
// Le foto le scarica il browser di Val (licenza Unsplash, autori in crediti.html) e le manda qui, una per volta.
// Accetta SOLO i file elencati sotto, riconosciuti dall'impronta SHA-256 del contenuto: qualsiasi altro file è rifiutato,
// quindi l'indirizzo non serve a nessun altro. Scrive in foto/. Dopo l'uso questo file viene sostituito da una versione che risponde 404.

$ATTESI = [
    'ulivo-alto.jpg'      => '6f69549a8e8fed6871010ec506c69be9a58d9936208da48682a86c6e7ee3ad97',
    'mani-largo.jpg'      => 'db65c62a29368d6624bbb5ce3b23f68ea3bf604b99bb153e58a1196202e10a3f',
    'chef-largo.jpg'      => '30ece4933d07b6e309de60fcff058bc1b7979688a7bd7fe4849f28c035afddab',
    'olive-banda.jpg'     => 'c26cf9cdf70840718ae14204171c15e74af5bd8d72c76db0d414d036ad89b22d',
    'chef-banda.jpg'      => 'abe3b93c074cd26e8734f9c94e7fb07436fc8043a17c4d1fed8f93cfdd1b0788',
    'barattoli-banda.jpg' => '2ba5daa2abb87d5291a3224c855d6bf7913571d79b874c4f1b5e67df6248ca62',
    'cassette-banda.jpg'  => '5bc5ebb0ec4f36f4fc1388813a8304151df15e93e886d58a782a740f242c07a8',
    'mercato-banda.jpg'   => 'af842d8462504719d125020f328fcee0c9ebad78564e83a09fe84f0e9c625864',
    'civita-banda.jpg'    => '8a17077cb78e1a646543c2314623478eb0b70e45944e052a4061717023fb1148',
    'legumi-banda.jpg'    => 'fe999a372b0e974fabb758ad3a112723f7d42b7afae52a1c24021c6e13ad0e4b',
];

header('Content-Type: text/plain; charset=utf-8'); header('X-Robots-Tag: noindex'); header('Cache-Control: no-store');
if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') { http_response_code(404); exit; }
$nome = (string)($_POST['nome'] ?? '');
if (!isset($ATTESI[$nome]) || !isset($_FILES['file']) || $_FILES['file']['error'] !== UPLOAD_ERR_OK || $_FILES['file']['size'] > 800000) {
    http_response_code(400); echo 'rifiutato'; exit;
}
$dati = file_get_contents($_FILES['file']['tmp_name']);
if ($dati === false || !hash_equals($ATTESI[$nome], hash('sha256', $dati))) { http_response_code(403); echo 'impronta diversa'; exit; }
$dir = __DIR__ . '/foto';
if (!is_dir($dir) && !mkdir($dir, 0755, true)) { http_response_code(500); echo 'cartella non creata'; exit; }
$dest = $dir . '/' . $nome;
if (is_file($dest) && hash_equals($ATTESI[$nome], hash_file('sha256', $dest))) { echo 'già presente'; exit; }
if (file_put_contents($dest, $dati, LOCK_EX) !== strlen($dati)) { http_response_code(500); echo 'scrittura non riuscita'; exit; }
echo 'ok';
