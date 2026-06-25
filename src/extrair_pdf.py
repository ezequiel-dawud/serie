"""
Extrai e estrutura o conteúdo do PDF do livro em capítulos.
"""
import re
import json
from pathlib import Path

try:
    import pdfplumber
except ImportError:
    raise SystemExit("Execute: pip install pdfplumber")


BOOK_PATH = Path(__file__).parent.parent / "book" / "Experimento 154.pdf"
OUTPUT_DIR = Path(__file__).parent.parent / "output"


def extrair_texto_completo(pdf_path: Path) -> str:
    texto = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                texto.append(t)
    return "\n".join(texto)


def dividir_em_capitulos(texto: str) -> list[dict]:
    # Detecta marcadores de capítulo como "Capítulo 1", "Capítulo 2", etc.
    padrao = re.compile(r"(Cap[ií]tulo\s+\d+)", re.IGNORECASE)
    partes = padrao.split(texto)

    capitulos = []
    i = 1
    while i < len(partes):
        cabecalho = partes[i].strip()
        conteudo = partes[i + 1].strip() if i + 1 < len(partes) else ""

        # Extrai subtítulo (primeiras duas linhas não vazias após o cabeçalho)
        linhas = [l.strip() for l in conteudo.split("\n") if l.strip()]
        subtitulo = linhas[0] if linhas else ""
        subtema = linhas[1] if len(linhas) > 1 else ""

        # Texto narrativo começa após os dois subtítulos
        inicio_narrativa = conteudo.find(subtema) + len(subtema) if subtema else 0
        narrativa = conteudo[inicio_narrativa:].strip()

        numero = re.search(r"\d+", cabecalho)
        capitulos.append({
            "numero": int(numero.group()) if numero else i,
            "titulo": subtitulo,
            "subtema": subtema,
            "texto": narrativa,
            "palavras": len(narrativa.split()),
        })
        i += 2

    return capitulos


def calcular_episodios_por_capitulo(palavras: int) -> int:
    # ~130 palavras por minuto narradas = 1040-1300 palavras por episódio de 8-10 min
    palavras_por_episodio = 1170  # média
    episodios = max(2, min(4, round(palavras / palavras_por_episodio)))
    return episodios


def dividir_capitulo_em_blocos(texto: str, num_episodios: int) -> list[str]:
    # Divide por parágrafos, agrupa em blocos de tamanho igual
    paragrafos = [p.strip() for p in texto.split("\n\n") if p.strip()]
    tamanho_bloco = max(1, len(paragrafos) // num_episodios)

    blocos = []
    for i in range(num_episodios):
        inicio = i * tamanho_bloco
        fim = inicio + tamanho_bloco if i < num_episodios - 1 else len(paragrafos)
        bloco = "\n\n".join(paragrafos[inicio:fim])
        blocos.append(bloco)

    return [b for b in blocos if b]


def processar_livro() -> dict:
    print(f"Lendo: {BOOK_PATH}")
    texto = extrair_texto_completo(BOOK_PATH)

    print("Dividindo em capítulos...")
    capitulos = dividir_em_capitulos(texto)

    estrutura = {"capitulos": [], "total_episodios": 0}

    for cap in capitulos:
        num_ep = calcular_episodios_por_capitulo(cap["palavras"])
        blocos = dividir_capitulo_em_blocos(cap["texto"], num_ep)

        episodios = []
        for idx, bloco in enumerate(blocos, 1):
            ep_num_global = estrutura["total_episodios"] + idx
            episodios.append({
                "episodio_global": ep_num_global,
                "episodio_no_capitulo": idx,
                "titulo": f"Ep{ep_num_global:02d} — {cap['titulo']} (Parte {idx})",
                "texto_bruto": bloco,
                "palavras": len(bloco.split()),
                "duracao_estimada_min": round(len(bloco.split()) / 130),
                "roteiro_gerado": False,
                "video_heygen_id": None,
                "video_url": None,
            })

        estrutura["total_episodios"] += len(episodios)
        estrutura["capitulos"].append({
            "numero": cap["numero"],
            "titulo": cap["titulo"],
            "subtema": cap["subtema"],
            "palavras_totais": cap["palavras"],
            "num_episodios": len(episodios),
            "episodios": episodios,
        })

    # Salva estrutura
    out = OUTPUT_DIR / "estrutura_serie.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(estrutura, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\nEstrutura salva em: {out}")
    print(f"Total de capítulos: {len(estrutura['capitulos'])}")
    print(f"Total de episódios: {estrutura['total_episodios']}")

    for cap in estrutura["capitulos"]:
        print(f"  Capítulo {cap['numero']}: {cap['titulo']} → {cap['num_episodios']} episódios")

    return estrutura


if __name__ == "__main__":
    processar_livro()
