# Filo Corto – codici QR senza librerie esterne.
# Serve per il QR della pagina di ogni produttore (da mettere su etichette, cassette e menu).
# Uso:  from qr import svg, matrice
#       svg('https://ilfilocorto.it/produttori/nome.html')  -> testo SVG
# Limiti voluti: solo testo corto (indirizzi web), correzione d'errore media (M), versioni da 1 a 10.

_BLOCCHI = {   # versione: (codici di correzione per blocco, [(quanti blocchi, codici dati per blocco), ...])
    1: (10, [(1, 16)]), 2: (16, [(1, 28)]), 3: (26, [(1, 44)]), 4: (18, [(2, 32)]), 5: (24, [(2, 43)]),
    6: (16, [(4, 27)]), 7: (18, [(4, 31)]), 8: (22, [(2, 38), (2, 39)]), 9: (22, [(3, 36), (2, 37)]), 10: (26, [(4, 43), (1, 44)]),
}
_ALLINEA = {1: [], 2: [6, 18], 3: [6, 22], 4: [6, 26], 5: [6, 30], 6: [6, 34], 7: [6, 22, 38], 8: [6, 24, 42], 9: [6, 26, 46], 10: [6, 28, 50]}

# Aritmetica del campo di Galois GF(256), polinomio 0x11D
_EXP, _LOG = [0] * 512, [0] * 256
_x = 1
for _i in range(255):
    _EXP[_i], _LOG[_x] = _x, _i
    _x <<= 1
    if _x & 0x100:
        _x ^= 0x11D
for _i in range(255, 512):
    _EXP[_i] = _EXP[_i - 255]


def _correzione(dati, n):
    """I codici Reed-Solomon (n) di un blocco di dati."""
    g = [1]
    for i in range(n):
        g2 = [0] * (len(g) + 1)
        for j, c in enumerate(g):
            g2[j] ^= c
            if c:
                g2[j + 1] ^= _EXP[_LOG[c] + i]
        g = g2
    resto = [0] * n
    for b in dati:
        f = b ^ resto[0]
        resto = resto[1:] + [0]
        if f:
            for j in range(n):
                if g[j + 1]:
                    resto[j] ^= _EXP[_LOG[g[j + 1]] + _LOG[f]]
    return resto


def _codici(testo):
    """Sceglie la versione più piccola che contiene il testo e restituisce (versione, sequenza finale di codici)."""
    d = testo.encode('utf-8')
    for v in range(1, 11):
        ec, gruppi = _BLOCCHI[v]
        capienza = sum(q * n for q, n in gruppi)
        conta = 8 if v < 10 else 16
        if 4 + conta + 8 * len(d) <= capienza * 8:
            break
    else:
        raise ValueError('Testo troppo lungo per il QR: ' + testo)
    bit = [0, 1, 0, 0] + [(len(d) >> i) & 1 for i in range(conta - 1, -1, -1)]
    for b in d:
        bit += [(b >> i) & 1 for i in range(7, -1, -1)]
    bit += [0] * min(4, capienza * 8 - len(bit))
    bit += [0] * (-len(bit) % 8)
    dati = [int(''.join(map(str, bit[i:i + 8])), 2) for i in range(0, len(bit), 8)]
    riemp = (0xEC, 0x11)
    dati += [riemp[i % 2] for i in range(capienza - len(dati))]
    blocchi, p = [], 0
    for q, n in gruppi:
        for _ in range(q):
            blocchi.append(dati[p:p + n])
            p += n
    corr = [_correzione(b, ec) for b in blocchi]
    fine = [b[i] for i in range(max(len(b) for b in blocchi)) for b in blocchi if i < len(b)]
    fine += [c[i] for i in range(ec) for c in corr]
    return v, fine


_MASCHERE = [lambda r, c: (r + c) % 2 == 0, lambda r, c: r % 2 == 0, lambda r, c: c % 3 == 0, lambda r, c: (r + c) % 3 == 0,
             lambda r, c: (r // 2 + c // 3) % 2 == 0, lambda r, c: (r * c) % 2 + (r * c) % 3 == 0,
             lambda r, c: ((r * c) % 2 + (r * c) % 3) % 2 == 0, lambda r, c: ((r + c) % 2 + (r * c) % 3) % 2 == 0]


def _penalita(m):
    n = len(m)
    p = 0
    righe = [list(r) for r in m] + [[m[r][c] for r in range(n)] for c in range(n)]
    for riga in righe:
        lung = 1
        for i in range(1, n):
            if riga[i] == riga[i - 1]:
                lung += 1
            else:
                if lung >= 5:
                    p += lung - 2
                lung = 1
        if lung >= 5:
            p += lung - 2
        s = ''.join('1' if x else '0' for x in riga)
        p += 40 * (s.count('10111010000') + s.count('00001011101'))
    for r in range(n - 1):
        for c in range(n - 1):
            if m[r][c] == m[r][c + 1] == m[r + 1][c] == m[r + 1][c + 1]:
                p += 3
    scuri = sum(sum(1 for x in r if x) for r in m)
    p += 10 * (abs(scuri * 20 - n * n * 10) // (n * n))
    return p


def matrice(testo):
    """La griglia del QR: lista di righe, True = modulo scuro."""
    v, codici = _codici(testo)
    n = 17 + 4 * v
    m = [[False] * n for _ in range(n)]
    f = [[False] * n for _ in range(n)]   # moduli di servizio (non portano dati)

    def metti(r, c, scuro):
        m[r][c], f[r][c] = bool(scuro), True

    for r0, c0 in ((0, 0), (0, n - 7), (n - 7, 0)):   # i tre mirini con il bordo chiaro
        for dr in range(-1, 8):
            for dc in range(-1, 8):
                r, c = r0 + dr, c0 + dc
                if 0 <= r < n and 0 <= c < n:
                    dentro = 0 <= dr <= 6 and 0 <= dc <= 6
                    metti(r, c, dentro and (dr in (0, 6) or dc in (0, 6) or (2 <= dr <= 4 and 2 <= dc <= 4)))
    for i in range(8, n - 8):   # linee di sincronismo
        metti(6, i, i % 2 == 0)
        metti(i, 6, i % 2 == 0)
    pos = _ALLINEA[v]
    for r0 in pos:   # riferimenti di allineamento
        for c0 in pos:
            if (r0, c0) in ((6, 6), (6, pos[-1]), (pos[-1], 6)):
                continue
            for dr in range(-2, 3):
                for dc in range(-2, 3):
                    metti(r0 + dr, c0 + dc, max(abs(dr), abs(dc)) != 1)
    for i in range(9):   # spazio per le informazioni di formato
        if not f[8][i]:
            metti(8, i, False)
        if not f[i][8]:
            metti(i, 8, False)
    for i in range(8):
        metti(8, n - 1 - i, False)
        metti(n - 1 - i, 8, False)
    metti(n - 8, 8, True)
    if v >= 7:   # informazioni di versione
        resto = v
        for _ in range(12):
            resto = (resto << 1) ^ ((resto >> 11) * 0x1F25)
        bitv = v << 12 | resto
        for i in range(18):
            b = (bitv >> i) & 1
            a, t = n - 11 + i % 3, i // 3
            metti(t, a, b)
            metti(a, t, b)

    bit = [(x >> i) & 1 for x in codici for i in range(7, -1, -1)]
    i, su, c = 0, True, n - 1
    while c > 0:   # i dati salgono e scendono a zig-zag, due colonne per volta
        if c == 6:
            c -= 1
        for k in range(n):
            r = n - 1 - k if su else k
            for cc in (c, c - 1):
                if not f[r][cc]:
                    m[r][cc] = bool(bit[i]) if i < len(bit) else False
                    i += 1
        su = not su
        c -= 2

    migliore = None
    for num, regola in enumerate(_MASCHERE):
        g = [[(m[r][c] ^ regola(r, c)) if not f[r][c] else m[r][c] for c in range(n)] for r in range(n)]
        dato = num   # livello M = 00, poi il numero della maschera
        resto = dato
        for _ in range(10):
            resto = (resto << 1) ^ ((resto >> 9) * 0x537)
        bitf = (dato << 10 | resto) ^ 0x5412
        b = lambda k: bool((bitf >> k) & 1)
        for k in range(6):
            g[k][8] = b(k)
        g[7][8], g[8][8], g[8][7] = b(6), b(7), b(8)
        for k in range(9, 15):
            g[8][14 - k] = b(k)
        for k in range(8):
            g[8][n - 1 - k] = b(k)
        for k in range(8, 15):
            g[n - 15 + k][8] = b(k)
        g[n - 8][8] = True
        p = _penalita(g)
        if migliore is None or p < migliore[0]:
            migliore = (p, g)
    return migliore[1]


def svg(testo, classe='', margine=4, colore='#1f2420', sfondo='#ffffff'):
    """Il QR come immagine SVG (testo): un rettangolo per ogni fila di moduli scuri."""
    g = matrice(testo)
    n = len(g)
    lato = n + 2 * margine
    d = []
    for r, riga in enumerate(g):
        c = 0
        while c < n:
            if riga[c]:
                c0 = c
                while c < n and riga[c]:
                    c += 1
                d.append(f'M{c0 + margine} {r + margine}h{c - c0}v1h-{c - c0}z')
            else:
                c += 1
    cls = f' class="{classe}"' if classe else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg"{cls} viewBox="0 0 {lato} {lato}" width="{lato * 8}" height="{lato * 8}" shape-rendering="crispEdges" role="img" aria-label="Codice QR">'
            f'<rect width="{lato}" height="{lato}" fill="{sfondo}"/><path d="{"".join(d)}" fill="{colore}"/></svg>')


if __name__ == '__main__':
    import sys
    print(svg(sys.argv[1] if len(sys.argv) > 1 else 'https://ilfilocorto.it/'))
