"""Gera as paginas HTML (para celular) da biblioteca de materiais do KIT.

Le materiais/README.md e cada materiais/*.md e grava:
  materiais/index.html            -> biblioteca (link enviado pelo ManyChat)
  materiais/<nome>.html           -> cada material em .md
Os links do README para .md passam a apontar para o .html correspondente.
Uso: python scripts/build_materiais.py   (rode na raiz do repositorio)
"""
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAT = ROOT / "materiais"

CSS = """
:root{--azul:#0b2a5b;--azul2:#1f5fbf;--fundo:#f4f6fa;--texto:#1b2333;--card:#fff}
*{box-sizing:border-box}
body{margin:0;background:var(--fundo);color:var(--texto);font:17px/1.55 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif}
header{background:var(--azul);color:#fff;padding:22px 16px 18px}
header a{color:#fff}
main{max-width:680px;margin:0 auto;padding:16px}
h1{font-size:1.45rem;margin:0 0 6px;line-height:1.25}
h2{font-size:1.15rem;margin:0 0 6px;color:var(--azul)}
h3{font-size:1.02rem;margin:18px 0 6px;color:var(--azul)}
.sub{opacity:.85;font-size:.95rem;margin:0}
section.card{background:var(--card);border-radius:14px;padding:16px;margin:14px 0;box-shadow:0 1px 4px rgba(11,42,91,.08)}
a{color:var(--azul2)}
a.btn{display:inline-block;margin-top:8px;background:var(--azul2);color:#fff;text-decoration:none;padding:11px 16px;border-radius:10px;font-weight:600}
ul,ol{padding-left:22px}
li{margin:4px 0}
footer{max-width:680px;margin:0 auto;padding:8px 16px 32px;font-size:.9rem;opacity:.8}
"""


def inline(text: str) -> str:
    t = html.escape(text, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![\*\w])\*(?!\s)(.+?)(?<!\s)\*(?!\w)", r"<em>\1</em>", t)

    def link(m):
        label, href = m.group(1), m.group(2)
        if href.endswith(".md") and "://" not in href:
            href = href[:-3] + ".html"
        cls = ' class="btn"' if label.lower().startswith("abrir") or "oficial" in label.lower() else ""
        ext = ' target="_blank" rel="noopener"' if "://" in href else ""
        return f'<a href="{href}"{cls}{ext}>{label}</a>'

    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link, t)
    return t


def md_to_html(md: str):
    """Conversor minimo para os materiais (titulos, listas, negrito, links)."""
    out, title, in_list = [], None, None
    for raw in md.splitlines():
        line = raw.rstrip()
        if line.strip().startswith("<!--"):
            continue
        m_ul = re.match(r"^\s*[-*]\s+(.*)", line)
        m_ol = re.match(r"^\s*\d+[.)]\s+(.*)", line)
        kind = "ul" if m_ul else "ol" if m_ol else None
        if in_list and kind != in_list:
            out.append(f"</{in_list}>")
            in_list = None
        if kind:
            if not in_list:
                out.append(f"<{kind}>")
                in_list = kind
            out.append(f"<li>{inline((m_ul or m_ol).group(1))}</li>")
            continue
        if not line.strip() or line.strip() == "---":
            continue
        h = re.match(r"^(#{1,3})\s+(.*)", line)
        if h:
            lvl = len(h.group(1))
            if lvl == 1 and title is None:
                title = h.group(2).strip()
                continue
            out.append(f"<h{lvl + 1 if lvl < 3 else 3}>{inline(h.group(2))}</h{lvl + 1 if lvl < 3 else 3}>")
            continue
        out.append(f"<p>{inline(line.strip())}</p>")
    if in_list:
        out.append(f"</{in_list}>")
    return title or "Material", "\n".join(out)


def page(title: str, sub: str, body: str, back: bool) -> str:
    voltar = '<p class="sub"><a href="index.html">&larr; Todos os materiais</a></p>' if back else ""
    return f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><style>{CSS}</style></head>
<body><header><main style="padding:0">{voltar}<h1>{html.escape(title)}</h1><p class="sub">{sub}</p></main></header>
<main>{body}</main>
<footer>Thiago Massicano · Advogado · <a href="https://instagram.com/thiago.massicano">@thiago.massicano</a><br>
Material informativo, sem caráter de consultoria.</footer></body></html>
"""


def build_index():
    md = (MAT / "README.md").read_text(encoding="utf-8")
    # divide em blocos por "## "
    head, *blocos = re.split(r"(?m)^## ", md)
    intro = [l for l in head.splitlines()[1:] if l.strip() and not l.startswith("<!--")]
    sub = inline(" ".join(intro))
    cards = []
    for b in blocos:
        b = b.split("\n---")[0]
        titulo, *resto = b.split("\n", 1)
        _, corpo = md_to_html("# x\n" + (resto[0] if resto else ""))
        corpo = corpo.replace("👉 ", "")
        cards.append(f'<section class="card"><h2>{inline(titulo.strip())}</h2>{corpo}</section>')
    (MAT / "index.html").write_text(
        page("Materiais gratuitos", sub, "\n".join(cards), back=False), encoding="utf-8")


def build_materiais():
    for f in sorted(MAT.glob("*.md")):
        if f.name == "README.md":
            continue
        title, body = md_to_html(f.read_text(encoding="utf-8"))
        (MAT / (f.stem + ".html")).write_text(
            page(title, "IA na advocacia, com ética", f'<section class="card">{body}</section>', back=True),
            encoding="utf-8")


if __name__ == "__main__":
    build_materiais()
    build_index()
    print("ok:", ", ".join(p.name for p in sorted(MAT.glob("*.html"))))
