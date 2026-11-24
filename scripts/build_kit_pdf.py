"""Gera o PDF unico do KIT (todos os materiais em um arquivo) para o ManyChat.

Le materiais/README.md (a ordem dos blocos "## " e a ordem do kit, o mais novo primeiro) e monta:
  - material .md                -> convertido para HTML
  - material .pdf               -> usa materiais/fontes/<nome>.html (o HTML que gerou o PDF)
  - link externo (ferramenta)   -> pagina curta com descricao e endereco
Grava materiais/kit-ia-na-advocacia.html e imprime em materiais/kit-ia-na-advocacia.pdf
com o Edge (ou Chrome) em modo headless.
Uso: python scripts/build_kit_pdf.py   (rode na raiz do repositorio)
"""
import datetime as dt
import html
import re
import subprocess
from pathlib import Path

from build_materiais import inline, md_to_html  # mesmo conversor da pagina do celular

ROOT = Path(__file__).resolve().parent.parent
MAT = ROOT / "materiais"
FONTES = MAT / "fontes"
SAIDA_HTML = MAT / "kit-ia-na-advocacia.html"
SAIDA_PDF = MAT / "kit-ia-na-advocacia.pdf"
NAVEGADORES = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
]

CSS = """
@page{size:A4;margin:0}
*{box-sizing:border-box;-webkit-print-color-adjust:exact;print-color-adjust:exact}
html,body{margin:0;background:#071226}
body{font-family:"Segoe UI",Arial,sans-serif;color:#e8eefc}
.p{padding:52px 60px 40px;page-break-after:always;break-after:page}
.p:last-child{page-break-after:auto;break-after:auto}
.h{font-size:13px;letter-spacing:2px;color:#7fb2ff;text-transform:uppercase}
h1{font-size:38px;line-height:1.08;margin:10px 0 6px;color:#fff;font-weight:900;text-transform:uppercase}
h2{color:#7fb2ff;font-size:19px;margin:26px 0 8px}
h3{color:#7fb2ff;font-size:16px;margin:20px 0 6px}
.sub{color:#a9c4f5;font-size:17px;margin-bottom:24px}
p{font-size:15px;line-height:1.5;margin:8px 0}
ol,ul{padding-left:22px}
li{margin:0 0 12px;font-size:15px;line-height:1.5}
.box{background:#0d1f3d;border-left:4px solid #3d8bff;padding:14px 18px;margin:10px 0 16px;border-radius:6px;font-size:14.5px;line-height:1.5}
.q{font-family:Consolas,monospace;font-size:13.5px;color:#d6e4ff}
.f{margin-top:30px;border-top:1px solid #23406e;padding-top:14px;font-size:12.5px;color:#8fa9d6}
b,strong{color:#fff}
a{color:#7fb2ff}
.capa{min-height:1120px;display:flex;flex-direction:column;justify-content:center}
.capa h1{font-size:58px}
.sumario li{font-size:17px;margin-bottom:14px}
.num{display:inline-block;min-width:34px;color:#3d8bff;font-weight:900}
.p .box{margin:6px 0 8px;padding:9px 14px;line-height:1.4}
.p .q{font-size:13px}
.p{padding:34px 56px 16px}
.p .f{margin-top:14px;padding-top:8px}
.p h2{margin:14px 0 4px}
.p h1{font-size:34px}
.p .sub{margin-bottom:16px;font-size:16px}
.capa h1{font-size:58px}
.p h2{margin:20px 0 6px}
.md li{margin:0 0 6px;font-size:14.5px}
.md h1{font-size:34px}
"""


def bloco_fonte(nome_pdf: str) -> str | None:
    """Conteudo da pagina que gerou o PDF (div.p de materiais/fontes/<nome>.html)."""
    f = FONTES / (Path(nome_pdf).stem + ".html")
    if not f.exists():
        return None
    t = f.read_text(encoding="utf-8")
    m = re.search(r'<div class="p">(.*)</div>\s*</body>', t, re.S)
    return m.group(1) if m else None


def blocos_readme():
    md = (MAT / "README.md").read_text(encoding="utf-8")
    _, *blocos = re.split(r"(?m)^## ", md)
    for b in blocos:
        b = b.split("\n---")[0].strip()
        titulo, _, resto = b.partition("\n")
        links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", resto)
        desc = re.sub(r"👉.*", "", resto).strip()
        yield titulo.strip(), desc, (links[0][1] if links else "")


def secao(titulo: str, desc: str, alvo: str) -> str | None:
    cab = '<div class="h">@thiago.massicano · IA na advocacia</div>'
    if alvo.endswith(".pdf"):
        corpo = bloco_fonte(alvo)
        if corpo is None:
            print("AVISO: sem fonte HTML para", alvo, "- material fora do kit")
            return None
        return f'<div class="p">{corpo}</div>'
    if alvo.endswith(".md") and "://" not in alvo:
        t, corpo = md_to_html((MAT / alvo).read_text(encoding="utf-8"))
        corpo = corpo.replace("<h2>", "<h2>").replace("<p><em>Material informativo", '<p class="f"><em>Material informativo')
        return (f'<div class="p md">{cab}<h1>{html.escape(t)}</h1>'
                f'<div class="sub">{inline(desc)}</div>{corpo}</div>')
    if "://" in alvo:
        return (f'<div class="p">{cab}<h1>{inline(titulo)}</h1><div class="sub">{inline(desc)}</div>'
                f'<div class="box">Endereço oficial: <a href="{alvo}">{html.escape(alvo)}</a></div>'
                '<div class="f">Material informativo, sem caráter de consultoria. Thiago Massicano · Advogado</div></div>')
    return None


def montar() -> str:
    itens = [(t, s) for t, d, a in blocos_readme() if (s := secao(t, d, a))]
    hoje = dt.date.today().strftime("%d/%m/%Y")
    sumario = "".join(f'<li><span class="num">{i:02d}</span>{inline(t)}</li>'
                      for i, (t, _) in enumerate(itens, 1))
    capa = (f'<div class="p capa"><div class="h">@thiago.massicano · IA na advocacia</div>'
            f'<h1>Kit IA na Advocacia</h1>'
            f'<div class="sub">Todos os materiais gratuitos do perfil em um só arquivo. '
            f'Prompts, checklists e ferramentas para usar a IA com ética no dia a dia do escritório.</div>'
            f'<h2>Neste kit</h2><ol class="sumario" style="list-style:none;padding:0">{sumario}</ol>'
            f'<div class="f">Atualizado em {hoje}. Comente <b>KIT</b> em qualquer post do '
            f'@thiago.massicano para receber a versão mais recente. Material informativo, sem caráter de '
            f'consultoria. Thiago Massicano · Advogado</div></div>')
    return (f'<!doctype html><html lang="pt-br"><head><meta charset="utf-8">'
            f'<title>Kit IA na Advocacia · @thiago.massicano</title><style>{CSS}</style></head><body>'
            + capa + "".join(s for _, s in itens) + "</body></html>")


def imprimir():
    nav = next((n for n in NAVEGADORES if Path(n).exists()), None)
    if not nav:
        raise SystemExit("Edge/Chrome nao encontrado para gerar o PDF")
    subprocess.run([nav, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={SAIDA_PDF}", SAIDA_HTML.as_uri()],
                   check=True, capture_output=True, timeout=120)


if __name__ == "__main__":
    SAIDA_HTML.write_text(montar(), encoding="utf-8")
    imprimir()
    print("ok:", SAIDA_PDF, SAIDA_PDF.stat().st_size, "bytes")
