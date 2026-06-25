"""
Pipeline principal: orquestra extração → roteiro → HeyGen → download.

Uso:
  python gerar_serie.py --explorar            # lista avatares/vozes disponíveis
  python gerar_serie.py --configurar          # configura avatares dos personagens
  python gerar_serie.py --capitulo=1          # processa cap 1 completo
  python gerar_serie.py --episodio=1          # processa só o episódio 1
  python gerar_serie.py --status              # mostra status de todos os vídeos
"""
import json
import sys
import os
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent.parent / "output"
ROTEIROS_DIR = OUTPUT_DIR / "roteiros"
VIDEOS_DIR = OUTPUT_DIR / "videos"
STATUS_DIR = OUTPUT_DIR / "status"


def cmd_explorar():
    from heygen_client import HeyGenClient
    client = HeyGenClient()

    print("\n=== Créditos ===")
    print(json.dumps(client.creditos_restantes(), indent=2))

    print("\n=== Primeiros 30 avatares ===")
    avatares = client.listar_avatares()
    for av in avatares[:30]:
        print(f"  {av.get('avatar_id'):40s} | {av.get('avatar_name'):30s} | {av.get('gender', '?')}")

    print("\n=== Vozes em Português ===")
    vozes = client.listar_vozes("Portuguese")
    for v in vozes:
        print(f"  {v.get('voice_id'):40s} | {v.get('display_name'):30s} | {v.get('gender', '?')}")


def cmd_configurar():
    """Guia interativo para mapear personagens → avatar_id + voice_id."""
    from heygen_client import carregar_config_avatares, salvar_config_avatares

    print("\nConfiguração de avatares para Experimento 154")
    print("=" * 50)
    print("Após explorar (--explorar), copie os IDs abaixo:\n")

    personagens = ["NARRADOR", "ZACK", "NINA", "JUAN"]
    config = carregar_config_avatares()

    for p in personagens:
        atual = config.get(p, {})
        print(f"\n[{p}]")
        print(f"  Avatar ID atual: {atual.get('avatar_id', '(não configurado)')}")
        print(f"  Voice ID atual:  {atual.get('voice_id', '(não configurado)')}")

        avatar_id = input(f"  Novo avatar_id (Enter para manter): ").strip()
        voice_id = input(f"  Novo voice_id  (Enter para manter): ").strip()

        if p not in config:
            config[p] = {}
        if avatar_id:
            config[p]["avatar_id"] = avatar_id
        if voice_id:
            config[p]["voice_id"] = voice_id

        # Fundo padrão: azul escuro para narrativa, mais claro para personagens
        if "background" not in config[p]:
            if p == "NARRADOR":
                config[p]["background"] = {"type": "color", "value": "#0d0d1a"}
            else:
                config[p]["background"] = {"type": "color", "value": "#1a1a2e"}

    salvar_config_avatares(config)
    print("\nConfiguração salva!")


def processar_episodio(ep_num_global: int):
    estrutura_path = OUTPUT_DIR / "estrutura_serie.json"
    if not estrutura_path.exists():
        raise FileNotFoundError("Execute: python extrair_pdf.py")

    estrutura = json.loads(estrutura_path.read_text(encoding="utf-8"))

    # Encontra o episódio
    ep_encontrado = None
    cap_encontrado = None
    for cap in estrutura["capitulos"]:
        for ep in cap["episodios"]:
            if ep["episodio_global"] == ep_num_global:
                ep_encontrado = ep
                cap_encontrado = cap
                break

    if not ep_encontrado:
        print(f"Episódio {ep_num_global} não encontrado.")
        return

    print(f"\nProcessando: {ep_encontrado['titulo']}")

    # 1. Gerar roteiro se não existe
    roteiro_path = ROTEIROS_DIR / f"ep{ep_num_global:02d}.json"
    if not roteiro_path.exists():
        print("Gerando roteiro com Claude...")
        from adaptar_roteiro import adaptar_episodio
        import anthropic
        client = anthropic.Anthropic()
        roteiro = adaptar_episodio(client, ep_encontrado, cap_encontrado)
        roteiro_path.write_text(json.dumps(roteiro, ensure_ascii=False, indent=2), encoding="utf-8")
        ep_encontrado["roteiro_gerado"] = True
    else:
        print("Roteiro já existe.")

    roteiro = json.loads(roteiro_path.read_text(encoding="utf-8"))

    # 2. Submeter ao HeyGen
    status_path = STATUS_DIR / f"ep{ep_num_global:02d}.json"

    if status_path.exists():
        status = json.loads(status_path.read_text(encoding="utf-8"))
        if status.get("status") == "completed":
            print(f"Vídeo já gerado: {status.get('video_url')}")
            return

    from heygen_client import HeyGenClient, carregar_config_avatares
    config_avatares = carregar_config_avatares()

    if not config_avatares:
        print("Configure os avatares primeiro: python gerar_serie.py --configurar")
        return

    client = HeyGenClient()
    payload = client.construir_payload_episodio(roteiro, config_avatares, ep_encontrado["titulo"])

    print(f"Submetendo {len(payload['video_inputs'])} cenas ao HeyGen...")
    video_id = client.criar_video(payload)
    print(f"Video ID: {video_id}")

    # Salva status inicial
    status_path.write_text(
        json.dumps({"video_id": video_id, "status": "processing", "episodio": ep_num_global},
                   ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # 3. Aguarda e baixa
    status_final = client.aguardar_video(video_id)
    video_url = status_final.get("video_url")

    destino = VIDEOS_DIR / f"ep{ep_num_global:02d}.mp4"
    client.baixar_video(video_url, destino)

    # Atualiza status
    status_final["episodio"] = ep_num_global
    status_path.write_text(json.dumps(status_final, ensure_ascii=False, indent=2), encoding="utf-8")

    # Atualiza estrutura
    ep_encontrado["video_heygen_id"] = video_id
    ep_encontrado["video_url"] = video_url
    estrutura_path.write_text(json.dumps(estrutura, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\nEpisódio {ep_num_global} concluído: {destino}")


def cmd_status():
    estrutura_path = OUTPUT_DIR / "estrutura_serie.json"
    if not estrutura_path.exists():
        print("Nenhuma estrutura encontrada. Execute: python extrair_pdf.py")
        return

    estrutura = json.loads(estrutura_path.read_text(encoding="utf-8"))

    print("\n=== Status da Série ===")
    for cap in estrutura["capitulos"]:
        print(f"\nCapítulo {cap['numero']}: {cap['titulo']}")
        for ep in cap["episodios"]:
            ep_num = ep["episodio_global"]
            roteiro_ok = "✓" if ep.get("roteiro_gerado") else "○"
            video_ok = "✓" if ep.get("video_url") else "○"
            print(f"  Ep{ep_num:02d} | Roteiro:{roteiro_ok} | Vídeo:{video_ok} | {ep['titulo']}")


def main():
    args = sys.argv[1:]

    if "--explorar" in args:
        cmd_explorar()
    elif "--configurar" in args:
        cmd_configurar()
    elif "--status" in args:
        cmd_status()
    elif any(a.startswith("--episodio=") for a in args):
        ep = int(next(a for a in args if a.startswith("--episodio=")).split("=")[1])
        processar_episodio(ep)
    elif any(a.startswith("--capitulo=") for a in args):
        cap_num = int(next(a for a in args if a.startswith("--capitulo=")).split("=")[1])
        estrutura_path = OUTPUT_DIR / "estrutura_serie.json"
        if not estrutura_path.exists():
            raise FileNotFoundError("Execute: python extrair_pdf.py")
        estrutura = json.loads(estrutura_path.read_text(encoding="utf-8"))
        for cap in estrutura["capitulos"]:
            if cap["numero"] == cap_num:
                for ep in cap["episodios"]:
                    processar_episodio(ep["episodio_global"])
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
