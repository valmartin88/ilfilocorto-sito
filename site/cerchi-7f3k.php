<?php
// File temporaneo di sola lettura: elenca come sono disegnati i cerchi nelle pagine. Da cancellare.
header('Content-Type: text/plain; charset=utf-8');
header('X-Robots-Tag: noindex');
foreach (glob(__DIR__ . '/*.html') as $f) {
    $s = file_get_contents($f);
    if (!preg_match_all('/<svg[^>]*>|<circle[^>]*>|<ellipse[^>]*>/', $s, $m)) continue;
    echo "== ", basename($f), "\n";
    foreach (array_count_values($m[0]) as $k => $v) echo "  ", $v, " x ", $k, "\n";
}
foreach (['favicon.svg', 'icona.png', 'og.png', 'logo.svg', 'logo.png'] as $f) {
    echo "file ", $f, ": ", file_exists(__DIR__ . '/' . $f) ? filesize(__DIR__ . '/' . $f) . " byte" : "non c'e'", "\n";
}
