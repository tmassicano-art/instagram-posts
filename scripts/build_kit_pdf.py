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

from build_materiais import inline  # links da descricao
from material_pdf import CSS as CSS_MAT, bloco_material, converter, documento  # modelo visual desde 28/11/2026

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

CSS = CSS_MAT


def md_do_alvo(alvo: str) -> Path | None:
    """Material em .md: o proprio link, ou o .md de mesmo nome de um link .pdf (ex.: checklist-pdf)."""
    if "://" in alvo or not alvo:
        return None
    p = MAT / alvo
    if p.suffix == ".pdf":
        p = p.with_suffix(".md")
    return p if p.suffix == ".md" and p.exists() else None


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
    mdp = md_do_alvo(alvo)
    if mdp:
        return bloco_material(mdp.read_text(encoding="utf-8"), mdp.stem)
    if "://" in alvo:
        return (f'<div class="capa"><div class="txt"><div class="kick">@thiago.massicano · ferramenta</div>'
                f'<h1>{inline(titulo)}</h1><p class="sub">{inline(desc)}</p></div><div class="barra"></div></div>'
                f'<div class="call dica"><div class="ic">→</div><div class="lb">Endereço oficial</div>'
                f'<a href="{alvo}">{html.escape(alvo)}</a></div>')
    print("AVISO: material sem .md, fora do kit:", alvo)
    return None


def montar() -> str:
    itens = [(t, s) for t, d, a in blocos_readme() if (s := secao(t, d, a))]
    hoje = dt.date.today().strftime("%d/%m/%Y")
    sumario = "".join(f"<li><b>{i:02d}</b>{inline(t)}</li>" for i, (t, _) in enumerate(itens, 1))
    capa = (f'<div class="capa"><div class="txt"><div class="kick">@thiago.massicano · IA na advocacia</div>'
            f'<h1>Kit IA na Advocacia</h1><p class="sub">Todos os materiais gratuitos do perfil em um só arquivo: '
            f'prompts, checklists e protocolos, cada um com a base legal conferida na fonte oficial.</p></div>'
            f'<div class="barra"></div></div>'
            f'<div class="meta"><div class="bloco"><div class="rot">Neste kit</div><ol class="sum">{sumario}</ol></div></div>'
            f'<p style="font-size:9pt;color:#4a5b7c">Atualizado em {hoje}. Comente <b>KIT</b> em qualquer post do '
            f'@thiago.massicano para receber a versão mais recente.</p>')
    corpo = capa + "".join(f'<div class="quebra"></div>{s}' for _, s in itens)
    return documento("Kit IA na Advocacia · @thiago.massicano", corpo)


def imprimir(origem: Path, destino: Path):
    nav = next((n for n in NAVEGADORES if Path(n).exists()), None)
    if not nav:
        raise SystemExit("Edge/Chrome nao encontrado para gerar o PDF")
    subprocess.run([nav, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--allow-file-access-from-files",
                    f"--print-to-pdf={destino}", origem.as_uri()],
                   check=True, capture_output=True, timeout=120)


def pdf_de_md(mdp: Path, nome: str | None = None) -> Path:
    mdp = Path(mdp).resolve()
    nome = nome or mdp.stem
    md = mdp.read_text(encoding="utf-8")
    FONTES.mkdir(exist_ok=True)
    tmp = FONTES / (nome + ".html")
    tmp.write_text(documento(converter(md)[0], bloco_material(md, nome)), encoding="utf-8")
    destino = MAT / (nome + ".pdf")
    imprimir(tmp, destino)
    return destino


def pdfs_individuais():
    """Cada material do README com .md ganha o proprio PDF (materiais/<nome>.pdf), no modelo visual novo."""
    for _, _, alvo in blocos_readme():
        mdp = md_do_alvo(alvo)
        if mdp:
            print("pdf:", pdf_de_md(mdp).name)


def pdf_avulso(md_path: Path, desc: str = "") -> Path:
    """PDF independente de um material .md (mesmo de fora do README): materiais/<nome>.pdf."""
    return pdf_de_md(Path(md_path))


if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 3 and sys.argv[1] == "--material":
        # uso: python scripts/build_kit_pdf.py --material <caminho.md>
        print("pdf:", pdf_avulso(Path(sys.argv[2])))
        raise SystemExit
    SAIDA_HTML.write_text(montar(), encoding="utf-8")
    imprimir(SAIDA_HTML, SAIDA_PDF)
    pdfs_individuais()
    print("ok:", SAIDA_PDF, SAIDA_PDF.stat().st_size, "bytes")
