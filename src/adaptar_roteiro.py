"""
Usa a API Claude para adaptar blocos do livro em roteiros para HeyGen.
Cada roteiro define: narrador + falas dos personagens com timecodes estimados.
"""
import json
import time
from pathlib import Path

try:
    import anthropic
except ImportError:
    raise SystemExit("Execute: pip install anthropic")

OUTPUT_DIR = Path(__file__).parent.parent / "output"
ROTEIROS_DIR = OUTPUT_DIR / "roteiros"
ROTEIROS_DIR.mkdir(parents=True, exist_ok=True)

PERSONAGENS = {
    "ZACK": {
        "descricao": "Garoto de 14 anos, corajoso, determinado mas assustado. Tom jovem, voz levemente trêmula em momentos de tensão.",
        "avatar_slot": "personagem_1",
    },
    "NINA": {
        "descricao": "Garota de 15 anos, fria e calculista. Voz jovem feminina, controlada, raramente demonstra emoção abertamente.",
        "avatar_slot": "personagem_2",
    },
    "JUAN": {
        "descricao": "Jovem de 19 anos, estudante de engenharia, analítico e calmo sob pressão. Voz adulta jovem, confiante.",
        "avatar_slot": "personagem_3",
    },
    "NARRADOR": {
        "descricao": "Narrador onisciente, tom dramático e cinematográfico como em 'The Last of Us'. Voz grave, pausada.",
        "avatar_slot": "narrador",
    },
}

SYSTEM_PROMPT = """Você é roteirista de séries de ficção científica/apocalipse para YouTube.
Adapta trechos do livro "Experimento 154 - O Legado dos Guilt's" em roteiros para vídeos com avatares de IA (HeyGen).

Formato de saída — JSON com esta estrutura exata:
{
  "titulo_episodio": "string",
  "duracao_estimada_min": number,
  "cenas": [
    {
      "numero": 1,
      "tipo": "NARRAÇÃO" | "FALA" | "TRANSIÇÃO",
      "personagem": "NARRADOR" | "ZACK" | "MARILUZ" | "JUAN",
      "texto": "texto que o avatar vai falar",
      "duracao_seg": number,
      "nota_direcao": "instrução opcional de tom/emoção"
    }
  ],
  "resumo_proximo_episodio": "uma frase de gancho para o próximo ep"
}

Regras:
- NARRADOR narra ações e descreve cenários (max 30 seg por cena de narração)
- Falas dos personagens devem ser do próprio livro ou muito próximas
- Cada cena de FALA deve ter 10-25 segundos de fala
- Total de cenas deve resultar em 8-10 minutos de vídeo (480-600 segundos total)
- Mantenha o tom sombrio e tenso do estilo The Last of Us
- Não invente eventos que não estão no trecho fornecido
- Responda APENAS com o JSON, sem texto adicional"""


def adaptar_episodio(
    client: anthropic.Anthropic,
    episodio: dict,
    capitulo: dict,
    ep_anterior_resumo: str = "",
) -> dict:
    contexto_anterior = ""
    if ep_anterior_resumo:
        contexto_anterior = f"\n\nCONTEXTO DO EPISÓDIO ANTERIOR:\n{ep_anterior_resumo}"

    prompt = f"""SÉRIE: Experimento 154 — O Legado dos Guilt's
CAPÍTULO {capitulo['numero']}: {capitulo['titulo']}
EPISÓDIO: {episodio['titulo']}
DURAÇÃO ALVO: {episodio['duracao_estimada_min']} minutos{contexto_anterior}

PERSONAGENS PRESENTES NESTE TRECHO:
{json.dumps(PERSONAGENS, ensure_ascii=False, indent=2)}

TRECHO DO LIVRO PARA ADAPTAR:
---
{episodio['texto_bruto']}
---

Adapte este trecho em roteiro para avatar HeyGen."""

    resposta = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
        system=SYSTEM_PROMPT,
    )

    texto_resposta = resposta.content[0].text.strip()

    # Remove blocos de código markdown se presentes
    if texto_resposta.startswith("```"):
        linhas = texto_resposta.split("\n")
        texto_resposta = "\n".join(linhas[1:-1])

    roteiro = json.loads(texto_resposta)
    return roteiro


def gerar_todos_roteiros(apenas_capitulo: int | None = None, forcar: bool = False):
    estrutura_path = OUTPUT_DIR / "estrutura_serie.json"
    if not estrutura_path.exists():
        raise FileNotFoundError("Execute extrair_pdf.py primeiro.")

    estrutura = json.loads(estrutura_path.read_text(encoding="utf-8"))

    client = anthropic.Anthropic()  # usa ANTHROPIC_API_KEY do ambiente

    ep_anterior_resumo = ""

    for cap in estrutura["capitulos"]:
        if apenas_capitulo and cap["numero"] != apenas_capitulo:
            continue

        print(f"\n=== Capítulo {cap['numero']}: {cap['titulo']} ===")

        for ep in cap["episodios"]:
            ep_num = ep["episodio_global"]
            roteiro_path = ROTEIROS_DIR / f"ep{ep_num:02d}.json"

            if roteiro_path.exists() and not forcar:
                print(f"  Ep{ep_num:02d} — já existe, pulando. (use --forcar para regenerar)")
                dados = json.loads(roteiro_path.read_text(encoding="utf-8"))
                ep_anterior_resumo = dados.get("resumo_proximo_episodio", "")
                continue

            print(f"  Gerando roteiro: {ep['titulo']}...")

            try:
                roteiro = adaptar_episodio(client, ep, cap, ep_anterior_resumo)
                ep_anterior_resumo = roteiro.get("resumo_proximo_episodio", "")

                # Salva roteiro
                roteiro_path.write_text(
                    json.dumps(roteiro, ensure_ascii=False, indent=2),
                    encoding="utf-8",
                )

                # Atualiza estrutura
                ep["roteiro_gerado"] = True
                total_seg = sum(c.get("duracao_seg", 0) for c in roteiro.get("cenas", []))
                ep["duracao_real_min"] = round(total_seg / 60, 1)

                print(f"    ✓ {len(roteiro.get('cenas', []))} cenas, ~{ep['duracao_real_min']} min")

                # Pausa para não sobrecarregar API
                time.sleep(2)

            except Exception as e:
                print(f"    ✗ Erro: {e}")

    # Salva estrutura atualizada
    estrutura_path.write_text(
        json.dumps(estrutura, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("\nRoteiros salvos em output/roteiros/")


if __name__ == "__main__":
    import sys

    apenas_cap = None
    forcar = "--forcar" in sys.argv

    for arg in sys.argv[1:]:
        if arg.startswith("--capitulo="):
            apenas_cap = int(arg.split("=")[1])

    gerar_todos_roteiros(apenas_capitulo=apenas_cap, forcar=forcar)
