"""Modelo visual dos materiais em PDF (padrao desde 28/11/2026).

Converte um material .md num HTML A4 claro, com capa em faixa azul (titulo, subtitulo, foto do
Thiago, "fundamentado em" e sumario), secoes numeradas, quadros de fundamento/atencao/na pratica,
caixa de prompt para copiar, checklist com caixinhas, tabelas e rodape em todas as paginas.

Convencoes do .md (ver _Tarefas/instagram-pauta-semanal.md, "Padrao do material"):
  # Titulo
  *subtitulo em italico*                 (linha logo abaixo do titulo)
  Base: LGPD, art. 6º, III · CPC, art. 77   (vira as etiquetas "Fundamentado em")
  ## Secao                               (numerada automaticamente; "## Fontes" fica sem numero)
  > **Fundamento:** texto                (tambem: Atenção, Na prática, Exemplo, Erro comum, Resumo)
  ```  prompt  ```                       (caixa escura "copie e cole")
  - [ ] item de checklist
  | tabela | markdown |
"""
import hashlib
import html
import re
from pathlib import Path

FOTOS = Path(r"C:\Users\Dr.Thiago\OneDrive\Instagram - IA na Advocacia\Fotos")
FOTOS_CAPA = ["08-sueter-maos-no-queixo-sorrindo.jpg", "09-mesa-estante-blazer-sorrindo.jpg",
              "10-mesa-estante-blazer-serio.jpg", "13-pb-janela-sorrindo.jpg", "02-retrato-sentado-terno-cinza.jpg",
              "01-escritorio-estante-em-pe-sorrindo.jpg", "12-retrato-pb-close-serio.jpg", "03-retrato-mao-no-queixo.jpg"]

CALLOUTS = {
    "fundamento": ("§", "fund"), "fundamentos": ("§", "fund"), "o que diz a lei": ("§", "fund"),
    "atenção": ("!", "alerta"), "atencao": ("!", "alerta"), "cuidado": ("!", "alerta"), "erro comum": ("!", "alerta"),
    "na prática": ("✓", "dica"), "na pratica": ("✓", "dica"), "dica": ("✓", "dica"), "resumo": ("✓", "dica"),
    "exemplo": ("→", "ex"), "exemplo fictício": ("→", "ex"),
}

CSS = """
@page{size:A4;margin:16mm 15mm 20mm}
@page:first{margin-top:0}
*{box-sizing:border-box;-webkit-print-color-adjust:exact;print-color-adjust:exact}
html,body{margin:0;background:#fff}
body{font-family:"Segoe UI",Arial,sans-serif;color:#1d2a3f;font-size:10.5pt;line-height:1.5}
.capa{background:linear-gradient(135deg,#061226 0%,#0b2350 60%,#123a7a 100%);color:#fff;
  margin:0 -15mm 18px;padding:15mm 15mm 12mm;display:flex;gap:22px;align-items:center;position:relative}
.capa .txt{flex:1}
.kick{font-size:8.5pt;letter-spacing:2.2px;text-transform:uppercase;color:#7fb6ff;font-weight:700}
.capa h1{font-size:25pt;line-height:1.08;margin:8px 0 8px;font-weight:900;letter-spacing:-.3px}
.capa .sub{font-size:11.5pt;color:#c9dcff;margin:0}
.capa .foto{width:118px;height:148px;border-radius:12px;background-size:cover;background-position:center 20%;
  border:3px solid #3d8bff;flex:none;box-shadow:0 6px 20px rgba(0,0,0,.35)}
.capa .barra{position:absolute;left:0;right:0;bottom:0;height:5px;background:linear-gradient(90deg,#3d8bff,#7fb6ff)}
.meta{display:flex;gap:18px;margin:0 0 14px}
.meta .bloco{flex:1;background:#f3f7fe;border:1px solid #dbe6fa;border-radius:10px;padding:10px 14px}
.meta .rot{font-size:7.5pt;letter-spacing:1.6px;text-transform:uppercase;color:#2f6fe0;font-weight:800;margin-bottom:6px}
.chip{display:inline-block;background:#fff;border:1px solid #b9cff5;color:#0b2350;border-radius:20px;
  padding:2px 10px;margin:0 5px 5px 0;font-size:8.5pt;font-weight:600}
.sum{margin:0;padding:0;list-style:none;counter-reset:s}
.sum li{font-size:9pt;margin:0 0 3px;color:#24365a}
.sum li b{color:#2f6fe0;margin-right:6px}
h2{font-size:14pt;color:#0b2350;margin:20px 0 8px;padding-bottom:5px;border-bottom:2px solid #e2ebfb;
  display:flex;align-items:center;gap:10px;break-after:avoid;page-break-after:avoid}
h2 .n{background:#2f6fe0;color:#fff;border-radius:8px;min-width:28px;height:28px;display:inline-flex;
  align-items:center;justify-content:center;font-size:11pt;font-weight:900}
h3{font-size:11pt;color:#2f6fe0;margin:14px 0 4px;break-after:avoid}
p{margin:6px 0}
ul,ol{margin:6px 0 8px;padding-left:20px}
li{margin:0 0 4px}
strong{color:#0b2350}
a{color:#2f6fe0;text-decoration:none;word-break:break-all}
.call{border-radius:10px;padding:10px 14px 10px 50px;margin:10px 0;position:relative;break-inside:avoid}
.call .ic{position:absolute;left:12px;top:10px;width:26px;height:26px;border-radius:50%;color:#fff;
  display:flex;align-items:center;justify-content:center;font-weight:900;font-size:12pt}
.call .lb{font-size:7.5pt;letter-spacing:1.5px;text-transform:uppercase;font-weight:800;margin-bottom:2px}
.fund{background:#eef4ff;border-left:4px solid #2f6fe0}.fund .ic{background:#2f6fe0}.fund .lb{color:#2f6fe0}
.alerta{background:#fff4ec;border-left:4px solid #e2701d}.alerta .ic{background:#e2701d}.alerta .lb{color:#c25a10}
.dica{background:#ecf9f1;border-left:4px solid #1f9d55}.dica .ic{background:#1f9d55}.dica .lb{color:#1a8048}
.ex{background:#f4f1fd;border-left:4px solid #6d4fd6}.ex .ic{background:#6d4fd6}.ex .lb{color:#5a3ec0}
.quote{border-left:4px solid #b9cff5;background:#f7f9fd;padding:8px 14px;margin:10px 0;font-style:italic;color:#33466b}
.prompt{background:#0b1830;border-radius:10px;margin:10px 0 12px;break-inside:avoid;overflow:hidden}
.prompt .lb{background:#16305e;color:#9cc4ff;font-size:7.5pt;letter-spacing:1.6px;font-weight:800;padding:6px 14px;
  text-transform:uppercase}
.prompt pre{margin:0;padding:10px 14px 12px;color:#e3ecff;font-family:Consolas,"Cascadia Mono",monospace;
  font-size:8.8pt;line-height:1.45;white-space:pre-wrap}
ul.check{list-style:none;padding-left:0}
ul.check li{position:relative;padding:5px 8px 5px 30px;margin:0 0 4px;background:#f7f9fd;border-radius:6px;break-inside:avoid}
ul.check li:before{content:"";position:absolute;left:9px;top:8px;width:12px;height:12px;border:2px solid #2f6fe0;border-radius:3px;background:#fff}
ol.passos{list-style:none;padding-left:0;counter-reset:p}
ol.passos li{counter-increment:p;position:relative;padding:6px 10px 6px 42px;margin:0 0 6px;background:#f7f9fd;
  border-radius:8px;break-inside:avoid}
ol.passos li:before{content:counter(p);position:absolute;left:10px;top:6px;width:22px;height:22px;border-radius:6px;
  background:#0b2350;color:#fff;font-weight:900;font-size:9.5pt;display:flex;align-items:center;justify-content:center}
table{width:100%;border-collapse:collapse;margin:8px 0 12px;font-size:9.3pt;break-inside:avoid}
th{background:#0b2350;color:#fff;text-align:left;padding:6px 9px;font-weight:700}
td{padding:6px 9px;border-bottom:1px solid #e2ebfb;vertical-align:top}
tr:nth-child(even) td{background:#f7f9fd}
.fontes{font-size:8.5pt;color:#4a5b7c}
.fontes li{margin-bottom:3px}
.rodape{position:fixed;bottom:-12mm;left:0;right:0;font-size:7.5pt;color:#7d8daa;display:flex;justify-content:space-between;
  border-top:1px solid #e2ebfb;padding-top:4px}
.fim{margin-top:16px;background:#0b2350;color:#fff;border-radius:10px;padding:12px 16px;display:flex;
  justify-content:space-between;align-items:center;break-inside:avoid}
.fim b{color:#7fb6ff}
.fim .s{font-size:8.5pt;color:#c9dcff}
.kitcapa{min-height:250mm;display:flex;flex-direction:column}
.quebra{break-before:page;page-break-before:always}
"""


def inline(t: str) -> str:
    t = html.escape(t, quote=False)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![\*\w])\*(?!\s)(.+?)(?<!\s)\*(?!\w)", r"<em>\1</em>", t)
    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', t)
    t = re.sub(r"(?<![\"'>=])(https?://[^\s<]+[^\s<.,;)])", r'<a href="\1">\1</a>', t)
    return t


def foto_capa(nome: str) -> str:
    i = int(hashlib.md5(nome.encode()).hexdigest(), 16) % len(FOTOS_CAPA)
    f = FOTOS / FOTOS_CAPA[i]
    return f.as_uri() if f.exists() else ""


def converter(md: str):
    """Devolve (titulo, subtitulo, bases, secoes, corpo_html)."""
    linhas = md.splitlines()
    titulo, sub, bases, secoes, out = "Material", "", [], [], []
    i, n_sec, lista = 0, 0, None

    def fecha():
        nonlocal lista
        if lista:
            out.append("</ul>" if lista in ("ul", "check") else "</ol>")
            lista = None

    while i < len(linhas):
        raw = linhas[i]
        s = raw.strip()
        i += 1
        if s.startswith("<!--"):
            continue
        if s.startswith("```"):
            fecha()
            bloco = []
            while i < len(linhas) and not linhas[i].strip().startswith("```"):
                bloco.append(linhas[i])
                i += 1
            i += 1
            rot = s[3:].strip() or "Prompt · copie e cole"
            out.append(f'<div class="prompt"><div class="lb">{html.escape(rot)}</div><pre>{html.escape(chr(10).join(bloco))}</pre></div>')
            continue
        if s.startswith("|"):
            fecha()
            tab = [s]
            while i < len(linhas) and linhas[i].strip().startswith("|"):
                tab.append(linhas[i].strip())
                i += 1
            cel = [[c.strip() for c in r.strip("|").split("|")] for r in tab if not re.match(r"^\|[\s:|-]+\|$", r)]
            th = "".join(f"<th>{inline(c)}</th>" for c in cel[0])
            tds = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in cel[1:])
            out.append(f"<table><tr>{th}</tr>{tds}</table>")
            continue
        if not s or s == "---":
            fecha()
            continue
        m = re.match(r"^(#{1,3})\s+(.*)", s)
        if m:
            fecha()
            nv, txt = len(m.group(1)), m.group(2).strip()
            if nv == 1:
                titulo = txt
                continue
            if nv == 2:
                if txt.lower().startswith("fontes"):
                    out.append(f'<h2>{inline(txt)}</h2><div class="fontes">')
                    secoes.append(txt)
                    out.append("<!--fontes-->")
                    continue
                n_sec += 1
                secoes.append(txt)
                out.append(f'<h2><span class="n">{n_sec}</span>{inline(txt)}</h2>')
            else:
                out.append(f"<h3>{inline(txt)}</h3>")
            continue
        if titulo != "Material" and not sub and not out and re.match(r"^\*[^*].*\*$", s):
            sub = s.strip("*")
            continue
        if s.lower().startswith("base:"):
            bases = [b.strip() for b in re.split(r"\s+·\s+|;", s[5:]) if b.strip()]
            continue
        if s.startswith(">"):
            fecha()
            txt = s.lstrip("> ").strip()
            while i < len(linhas) and linhas[i].strip().startswith(">"):
                txt += " " + linhas[i].strip().lstrip("> ").strip()
                i += 1
            mm = re.match(r"^\*\*([^*:]+):?\*\*:?\s*(.*)", txt)
            if mm and mm.group(1).strip().lower() in CALLOUTS:
                ic, cls = CALLOUTS[mm.group(1).strip().lower()]
                out.append(f'<div class="call {cls}"><div class="ic">{ic}</div><div class="lb">{html.escape(mm.group(1).strip())}</div>{inline(mm.group(2)[:1].upper() + mm.group(2)[1:])}</div>')
            else:
                out.append(f'<div class="quote">{inline(txt)}</div>')
            continue
        mc = re.match(r"^[-*]\s+\[[ xX]?\]\s+(.*)", s)
        mu = re.match(r"^[-*]\s+(.*)", s)
        mo = re.match(r"^\d+[.)]\s+(.*)", s)
        tipo = "check" if mc else "ul" if mu else "ol" if mo else None
        if tipo:
            if lista != tipo:
                fecha()
                ini = int(re.match(r"^(\d+)", s).group(1)) - 1 if tipo == "ol" else 0
                out.append({"check": '<ul class="check">', "ul": "<ul>", "ol": f'<ol class="passos" style="counter-reset:p {ini}">'}[tipo])
                lista = tipo
            out.append(f"<li>{inline((mc or mu or mo).group(1))}</li>")
            continue
        fecha()
        if s.startswith("*Material informativo"):
            continue
        out.append(f"<p>{inline(s)}</p>")
    fecha()
    corpo = "\n".join(out)
    if "<!--fontes-->" in corpo:
        corpo += "</div>"
    return titulo, sub, bases, secoes, corpo


def bloco_material(md: str, nome: str, palavra: str = "") -> str:
    titulo, sub, bases, secoes, corpo = converter(md)
    foto = foto_capa(nome)
    foto_html = f'<div class="foto" style="background-image:url(\'{foto}\')"></div>' if foto else ""
    chips = "".join(f'<span class="chip">{inline(b)}</span>' for b in bases) or '<span class="chip">Fontes oficiais conferidas</span>'
    numeradas = [s for s in secoes if not s.lower().startswith("fontes")]
    sumario = "".join(f"<li><b>{k:02d}</b>{inline(s)}</li>" for k, s in enumerate(numeradas, 1))
    fim = (f'<div class="fim"><div><b>Gostou?</b> Salve este PDF e compartilhe com um colega.<div class="s">'
           f'Mais conteúdo prático de IA na advocacia em @thiago.massicano</div></div><div class="s">Material informativo,<br>'
           f'sem caráter de consultoria.</div></div>')
    return (f'<div class="capa"><div class="txt"><div class="kick">@thiago.massicano · IA na advocacia</div>'
            f'<h1>{inline(titulo)}</h1><p class="sub">{inline(sub)}</p></div>{foto_html}<div class="barra"></div></div>'
            f'<div class="meta"><div class="bloco"><div class="rot">Fundamentado em</div>{chips}</div>'
            f'<div class="bloco"><div class="rot">Neste material</div><ol class="sum">{sumario}</ol></div></div>'
            f'{corpo}{fim}')


RODAPE = ('<div class="rodape"><span>Thiago Massicano · Advogado · @thiago.massicano</span>'
          '<span>Material informativo, sem caráter de consultoria</span></div>')


def documento(titulo: str, corpo: str) -> str:
    return (f'<!doctype html><html lang="pt-br"><head><meta charset="utf-8"><title>{html.escape(titulo)}</title>'
            f'<style>{CSS}</style></head><body>{RODAPE}{corpo}</body></html>')


def html_material(md_path: Path) -> str:
    md = Path(md_path).read_text(encoding="utf-8")
    titulo = converter(md)[0]
    return documento(titulo, bloco_material(md, Path(md_path).stem))

