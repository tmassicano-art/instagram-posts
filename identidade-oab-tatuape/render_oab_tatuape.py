#!/usr/bin/env python3
"""
Gerador de carrossel na identidade visual da OAB Tatuapé.

Uso:
    python3 render_oab_tatuape.py roteiro.json -o pasta/saida [--jpg]

Lê um roteiro em JSON e gera um arquivo 1080x1350 por card.
Paleta, tipografia e ornamentos seguem a arte de referência da Subseção
(fundo claro, azul-marinho, dourado, títulos serifados).
"""

import argparse
import json
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- identidade

FUNDO = (242, 242, 242)
NAVY = (11, 43, 73)
NAVY_ESCURO = (11, 32, 56)
DOURADO = (217, 163, 84)
BRANCO = (250, 250, 250)
CINZA = (90, 104, 122)

FONTES = {
    "serif": "PlayfairDisplay-Black.ttf",
    "serif_bold": "PlayfairDisplay-Bold.ttf",
    "sans": "Montserrat-Medium.ttf",
    "sans_bold": "Montserrat-Bold.ttf",
    "sans_black": "Montserrat-ExtraBold.ttf",
}

ESCALA = 2  # desenha em 2x e reduz, para curvas suaves
W0, H0 = 1080, 1350

_cache = {}


def fonte(chave, tam):
    k = (chave, int(tam))
    if k not in _cache:
        _cache[k] = ImageFont.truetype(os.path.join(AQUI, "fonts", FONTES[chave]), int(tam))
    return _cache[k]


def px(v):
    return int(round(v * ESCALA))


# ---------------------------------------------------------------- texto

def quebrar(draw, texto, f, largura):
    linhas = []
    for par in texto.split("\n"):
        atual = ""
        for palavra in par.split():
            teste = (atual + " " + palavra).strip()
            if draw.textlength(teste, font=f) <= largura or not atual:
                atual = teste
            else:
                linhas.append(atual)
                atual = palavra
        linhas.append(atual)
    return linhas


def caber(draw, texto, chave, largura, altura, tam_max, tam_min, entre=1.18, max_linhas=None):
    """Maior corpo que cabe na caixa. Devolve (fonte, linhas, altura_linha)."""
    tam = tam_max
    while True:
        f = fonte(chave, tam)
        linhas = quebrar(draw, texto, f, largura)
        alt_linha = tam * entre
        if (len(linhas) * alt_linha <= altura and
                (max_linhas is None or len(linhas) <= max_linhas)) or tam <= tam_min:
            return f, linhas, alt_linha
        tam = max(tam_min, int(tam * 0.95))


def escrever(draw, linhas, f, alt_linha, x, y, cor, alinhar="centro", largura=None):
    """Escreve linhas a partir do topo y. Devolve o y final."""
    fundo_tinta = y
    for ln in linhas:
        anc = "ma" if alinhar == "centro" else "la"
        draw.text((x, y), ln, font=f, fill=cor, anchor=anc)
        fundo_tinta = max(fundo_tinta, draw.textbbox((x, y), ln, font=f, anchor=anc)[3])
        y += alt_linha
    return fundo_tinta


def bloco_texto(draw, texto, chave, cor, x, y, largura, altura, tam_max, tam_min,
                entre=1.18, alinhar="centro", max_linhas=None, centralizar_v=False):
    f, linhas, al = caber(draw, texto, chave, largura, altura, tam_max, tam_min, entre, max_linhas)
    total = len(linhas) * al
    if centralizar_v:
        y = y + (altura - total) / 2
    return escrever(draw, linhas, f, al, x, y, cor, alinhar), total


# ---------------------------------------------------------------- ornamentos

def canto(img, draw, W, H):
    """Curva azul com filete dourado no canto superior esquerdo."""
    cx, cy = W * 0.62, W * 0.62
    r = math.hypot(cx, cy - H * 0.235)
    # área azul: tudo fora do círculo, no canto
    mask = Image.new("L", (W, H), 0)
    md = ImageDraw.Draw(mask)
    md.rectangle([0, 0, W, H], fill=255)
    md.ellipse([cx - r, cy - r, cx + r, cy + r], fill=0)
    md.rectangle([int(W * 0.5), 0, W, H], fill=0)
    md.rectangle([0, int(H * 0.5), W, H], fill=0)
    img.paste(NAVY, (0, 0, W, H), mask)
    rg = r - px(16)
    draw.arc([cx - rg, cy - rg, cx + rg, cy + rg], 180, 270, fill=DOURADO, width=px(4))


def regua(draw, x1, x2, y, ornamento=True):
    """Filete dourado; com um pequeno x no centro, como na arte de referência."""
    draw.line([(x1, y), (x2, y)], fill=DOURADO, width=px(4))
    if ornamento:
        cx = (x1 + x2) / 2
        g = px(13)
        draw.rectangle([cx - g - px(4), y - g, cx + g + px(4), y + g], fill=FUNDO)
        d = px(8)
        draw.line([(cx - d, y - d), (cx + d, y + d)], fill=DOURADO, width=px(4))
        draw.line([(cx - d, y + d), (cx + d, y - d)], fill=DOURADO, width=px(4))


def balanca(draw, cx, cy, tam, cor=DOURADO):
    """Balança simples: haste, travessão e dois pratos."""
    w = px(3)
    s = tam
    draw.line([(cx, cy - s * 0.55), (cx, cy + s * 0.42)], fill=cor, width=w)
    draw.ellipse([cx - s * 0.07, cy - s * 0.66, cx + s * 0.07, cy - s * 0.52], fill=cor)
    draw.line([(cx - s * 0.5, cy - s * 0.38), (cx + s * 0.5, cy - s * 0.38)], fill=cor, width=w)
    for lado in (-1, 1):
        px0 = cx + lado * s * 0.5
        draw.line([(px0, cy - s * 0.38), (px0 - s * 0.2, cy + s * 0.05)], fill=cor, width=px(2))
        draw.line([(px0, cy - s * 0.38), (px0 + s * 0.2, cy + s * 0.05)], fill=cor, width=px(2))
        draw.pieslice([px0 - s * 0.24, cy - s * 0.12, px0 + s * 0.24, cy + s * 0.2], 0, 180, fill=cor)
    draw.polygon([(cx - s * 0.12, cy + s * 0.32), (cx + s * 0.12, cy + s * 0.32),
                  (cx + s * 0.26, cy + s * 0.5), (cx - s * 0.26, cy + s * 0.5)], fill=cor)


def seta(draw, x, y, direcao):
    a = px(10)
    draw.line([(x - direcao * a, y - a), (x, y)], fill=DOURADO, width=px(3))
    draw.line([(x - direcao * a, y + a), (x, y)], fill=DOURADO, width=px(3))


def rodape(draw, W, H, completo):
    y = H - px(205 if completo else 150)
    cx = W / 2
    m = px(150)
    draw.line([(m, y), (cx - px(48), y)], fill=DOURADO, width=px(3))
    draw.line([(cx + px(48), y), (W - m, y)], fill=DOURADO, width=px(3))
    seta(draw, cx - px(48), y, 1)
    seta(draw, cx + px(48), y, -1)
    balanca(draw, cx, y, px(56))
    y += px(52)
    draw.text((cx, y), "OAB TATUAPÉ", font=fonte("sans_black", px(30)), fill=NAVY, anchor="ma")
    y += px(40)
    draw.text((cx, y), "JUNTOS, SOMOS MAIS FORTES!", font=fonte("sans", px(25)), fill=NAVY, anchor="ma")
    if completo:
        y += px(38)
        draw.text((cx, y), "Presidente OAB Tatuapé: Thiago Massicano", font=fonte("sans", px(25)),
                  fill=NAVY, anchor="ma")


def logo(img, cx, y, largura):
    lg = Image.open(os.path.join(AQUI, "img", "logo-oab-tatuape-navy.png"))
    h = int(lg.height * largura / lg.width)
    lg = lg.resize((int(largura), h), Image.LANCZOS)
    img.paste(lg, (int(cx - largura / 2), int(y)), lg)
    return y + h


def contador(draw, W, i, n):
    draw.text((W - px(54), px(48)), f"{i}/{n}", font=fonte("sans_bold", px(26)), fill=NAVY, anchor="ra")


def caixa(draw, x1, y1, x2, y2):
    draw.rounded_rectangle([x1, y1, x2, y2], radius=px(20), fill=NAVY, outline=DOURADO, width=px(5))


def linhas_na_caixa(draw, itens, x1, y1, x2, y2, rotulos=None):
    """Caixa azul em faixas, cada uma com rótulo dourado, divisória e texto,
    como o bloco de horário e local da arte de referência."""
    caixa(draw, x1, y1, x2, y2)
    n = len(itens)
    alt = (y2 - y1) / n
    col = px(150)
    for k, txt in enumerate(itens):
        ty = y1 + k * alt
        if k:
            draw.line([(x1 + px(40), ty), (x2 - px(40), ty)], fill=DOURADO, width=px(3))
        rot = rotulos[k] if rotulos else f"{k + 1:02d}"
        draw.text((x1 + col / 2 + px(14), ty + alt / 2), rot, font=fonte("serif", px(58)),
                  fill=DOURADO, anchor="mm", features=["lnum"])
        draw.line([(x1 + col + px(22), ty + alt * 0.2), (x1 + col + px(22), ty + alt * 0.8)],
                  fill=BRANCO, width=px(3))
        tx = x1 + col + px(52)
        larg = x2 - tx - px(36)
        bloco_texto(draw, txt, "sans_bold", BRANCO, tx, ty + px(14), larg, alt - px(28),
                    px(36), px(24), entre=1.25, alinhar="esq", centralizar_v=True)


# ---------------------------------------------------------------- cards

def novo(W, H, com_canto=True):
    img = Image.new("RGB", (W, H), FUNDO)
    d = ImageDraw.Draw(img)
    if com_canto:
        canto(img, d, W, H)
    return img, d


def card_capa(c, W, H, i, n):
    img, d = novo(W, H)
    contador(d, W, i, n)
    y = logo(img, W / 2, px(46), px(340)) + px(44)
    m = px(90)
    if c.get("chamada"):
        y, _ = bloco_texto(d, c["chamada"].upper(), "serif_bold", NAVY, W / 2, y, W - 2 * m, px(130),
                           px(56), px(36), entre=1.08)
        y += px(24)
        regua(d, px(180), W - px(180), y)
        y += px(36)
    y, _ = bloco_texto(d, c.get("titulo", "").upper(), "serif", NAVY, W / 2, y, W - px(110), px(380),
                       px(118), px(64), entre=1.02, max_linhas=3)
    y += px(30)
    regua(d, px(130), W - px(130), y, ornamento=False)
    y += px(38)
    apoio = c.get("apoio", "")
    if apoio:
        y2 = H - px(260)
        caixa(d, px(70), y, W - px(70), y2)
        bloco_texto(d, apoio, "sans_bold", BRANCO, W / 2, y + px(30), W - px(220), y2 - y - px(60),
                    px(40), px(26), entre=1.3, centralizar_v=True)
    rodape(d, W, H, completo=True)
    return img


def cabecalho(img, d, c, W, H, i, n):
    contador(d, W, i, n)
    y = logo(img, W / 2, px(46), px(250)) + px(40)
    if c.get("etiqueta"):
        f = fonte("sans_black", px(26))
        d.text((W / 2, y), " ".join(c["etiqueta"].upper()).replace("   ", "  "), font=f,
               fill=DOURADO, anchor="ma")
        y += px(50)
    y, _ = bloco_texto(d, c.get("titulo", "").upper(), "serif", NAVY, W / 2, y, W - px(140), px(200),
                       px(76), px(48), entre=1.04, max_linhas=3)
    y += px(26)
    regua(d, px(170), W - px(170), y)
    return y + px(40)


def card_conteudo(c, W, H, i, n):
    img, d = novo(W, H)
    y = cabecalho(img, d, c, W, H, i, n)
    y2 = H - px(190)
    if c.get("itens"):
        linhas_na_caixa(d, c["itens"], px(64), y, W - px(64), y2)
    else:
        larg, alt_max = W - px(220), y2 - y - px(100)
        f, linhas, al = caber(d, c.get("texto", ""), "sans", larg, alt_max, px(48), px(26), 1.42)
        alt = len(linhas) * al + px(100)
        y0 = y + (y2 - y - alt) / 2
        caixa(d, px(64), y0, W - px(64), y0 + alt)
        escrever(d, linhas, f, al, px(110), y0 + px(50) + (al - f.size) * 0.3, BRANCO, alinhar="esq")
    rodape(d, W, H, completo=False)
    return img


def card_destaque(c, W, H, i, n):
    img, d = novo(W, H)
    contador(d, W, i, n)
    y = logo(img, W / 2, px(46), px(250)) + px(70)
    regua(d, px(170), W - px(170), y)
    y += px(20)
    if c.get("numero"):
        fn = fonte("serif", px(300))
        d.text((W / 2, y), c["numero"], font=fn, fill=NAVY, anchor="ma", features=["lnum"])
        y = d.textbbox((W / 2, y), c["numero"], font=fn, anchor="ma", features=["lnum"])[3] + px(36)
    y, _ = bloco_texto(d, c.get("titulo", "").upper(), "serif", NAVY, W / 2, y, W - px(120), px(160),
                       px(78), px(46), entre=1.04)
    y += px(30)
    regua(d, px(170), W - px(170), y, ornamento=False)
    y += px(40)
    bloco_texto(d, c.get("texto", ""), "sans", NAVY, W / 2, y, W - px(200), H - px(190) - y - px(30),
                px(40), px(26), entre=1.38)
    rodape(d, W, H, completo=False)
    return img


def card_cta(c, W, H, i, n):
    img, d = novo(W, H)
    contador(d, W, i, n)
    y = logo(img, W / 2, px(46), px(300)) + px(50)
    y, _ = bloco_texto(d, c.get("titulo", "").upper(), "serif", NAVY, W / 2, y, W - px(120), px(220),
                       px(92), px(54), entre=1.04, max_linhas=2)
    y += px(28)
    regua(d, px(170), W - px(170), y)
    y += px(40)
    acoes = c.get("acoes") or ["Siga a OAB Tatuapé", "Compartilhe com quem precisa", "Salve para consultar depois"]
    linhas_na_caixa(d, acoes, px(64), y, W - px(64), H - px(260))
    rodape(d, W, H, completo=True)
    return img


RENDER = {"capa": card_capa, "conteudo": card_conteudo, "destaque": card_destaque, "cta": card_cta}


def gerar(roteiro, saida, jpg=False):
    W, H = px(W0), px(H0)
    cards = roteiro["cards"]
    os.makedirs(saida, exist_ok=True)
    feitos = []
    for i, c in enumerate(cards, start=1):
        img = RENDER.get(c.get("tipo", "conteudo"), card_conteudo)(c, W, H, i, len(cards))
        img = img.resize((W0, H0), Image.LANCZOS)
        if jpg:
            p = os.path.join(saida, f"slide-{i:02d}.jpg")
            img.save(p, "JPEG", quality=93, optimize=True)
        else:
            p = os.path.join(saida, f"slide-{i:02d}.png")
            img.save(p, "PNG", optimize=True)
        feitos.append(p)
        print("gerado:", p)
    return feitos


def main():
    ap = argparse.ArgumentParser(description="Carrossel na identidade da OAB Tatuapé")
    ap.add_argument("roteiro")
    ap.add_argument("-o", "--saida", required=True)
    ap.add_argument("--jpg", action="store_true", help="salvar em JPG em vez de PNG")
    a = ap.parse_args()
    with open(a.roteiro, encoding="utf-8") as fh:
        gerar(json.load(fh), a.saida, a.jpg)


if __name__ == "__main__":
    sys.exit(main())
