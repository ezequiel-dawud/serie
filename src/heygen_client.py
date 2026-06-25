"""
Cliente da HeyGen API para geração de vídeos dos episódios.
Documentação: https://docs.heygen.com/reference/
"""
import json
import time
import os
from pathlib import Path
from typing import Optional

try:
    import requests
except ImportError:
    raise SystemExit("Execute: pip install requests")

HEYGEN_API_BASE = "https://api.heygen.com"
OUTPUT_DIR = Path(__file__).parent.parent / "output"
STATUS_DIR = OUTPUT_DIR / "status"
STATUS_DIR.mkdir(parents=True, exist_ok=True)


class HeyGenClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("HEYGEN_API_KEY")
        if not self.api_key:
            raise ValueError(
                "HeyGen API key não encontrada. "
                "Configure HEYGEN_API_KEY no ambiente ou passe como argumento."
            )
        self.headers = {
            "X-Api-Key": self.api_key,
            "Content-Type": "application/json",
        }

    def _get(self, endpoint: str) -> dict:
        r = requests.get(f"{HEYGEN_API_BASE}{endpoint}", headers=self.headers)
        r.raise_for_status()
        return r.json()

    def _post(self, endpoint: str, payload: dict) -> dict:
        r = requests.post(
            f"{HEYGEN_API_BASE}{endpoint}",
            headers=self.headers,
            json=payload,
        )
        r.raise_for_status()
        return r.json()

    # ── Informações ──────────────────────────────────────────────────────────

    def listar_avatares(self) -> list[dict]:
        data = self._get("/v2/avatars")
        return data.get("data", {}).get("avatars", [])

    def listar_vozes(self, idioma: str = "Portuguese") -> list[dict]:
        data = self._get("/v2/voices")
        vozes = data.get("data", {}).get("voices", [])
        return [v for v in vozes if idioma.lower() in v.get("language", "").lower()]

    def creditos_restantes(self) -> dict:
        data = self._get("/v2/user/remaining_quota")
        return data.get("data", {})

    # ── Geração de vídeo ─────────────────────────────────────────────────────

    def construir_payload_episodio(
        self,
        roteiro: dict,
        config_avatares: dict,
        titulo: str,
    ) -> dict:
        """
        Monta o payload da API HeyGen a partir do roteiro gerado pelo Claude.
        config_avatares: mapeamento personagem → {avatar_id, voice_id}
        """
        clips = []

        for cena in roteiro.get("cenas", []):
            personagem = cena.get("personagem", "NARRADOR")
            config = config_avatares.get(personagem, config_avatares.get("NARRADOR", {}))

            if not config.get("avatar_id") or not config.get("voice_id"):
                print(f"  Aviso: avatar/voz não configurado para {personagem}, pulando cena.")
                continue

            clip = {
                "character": {
                    "type": "avatar",
                    "avatar_id": config["avatar_id"],
                    "avatar_style": "normal",
                },
                "voice": {
                    "type": "text",
                    "input_text": cena["texto"],
                    "voice_id": config["voice_id"],
                    "speed": 1.0,
                },
                "background": config.get("background", {"type": "color", "value": "#1a1a2e"}),
            }
            clips.append(clip)

        return {
            "video_inputs": clips,
            "ratio": "16:9",
            "test": False,  # altere para True para testes sem consumir créditos
        }

    def criar_video(self, payload: dict) -> str:
        """Submete vídeo para geração. Retorna o video_id."""
        data = self._post("/v2/video/generate", payload)
        video_id = data.get("data", {}).get("video_id")
        if not video_id:
            raise RuntimeError(f"Resposta inesperada: {data}")
        return video_id

    def status_video(self, video_id: str) -> dict:
        data = self._get(f"/v1/video_status.get?video_id={video_id}")
        return data.get("data", {})

    def aguardar_video(self, video_id: str, timeout_min: int = 30) -> dict:
        """Aguarda a geração do vídeo com polling. Retorna os dados finais."""
        inicio = time.time()
        intervalo = 30  # segundos entre checks

        print(f"  Aguardando vídeo {video_id}...")
        while True:
            status = self.status_video(video_id)
            estado = status.get("status", "")

            if estado == "completed":
                print(f"  ✓ Vídeo pronto: {status.get('video_url')}")
                return status
            elif estado == "failed":
                raise RuntimeError(f"Vídeo falhou: {status.get('error')}")
            elif time.time() - inicio > timeout_min * 60:
                raise TimeoutError(f"Timeout após {timeout_min} min.")

            print(f"  Status: {estado} — aguardando {intervalo}s...")
            time.sleep(intervalo)

    # ── Download ─────────────────────────────────────────────────────────────

    def baixar_video(self, url: str, destino: Path) -> Path:
        destino.parent.mkdir(parents=True, exist_ok=True)
        r = requests.get(url, stream=True)
        r.raise_for_status()
        with open(destino, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"  Baixado: {destino}")
        return destino


# ── Configuração de avatares ──────────────────────────────────────────────────

def carregar_config_avatares() -> dict:
    config_path = OUTPUT_DIR.parent / "config_avatares.json"
    if config_path.exists():
        return json.loads(config_path.read_text(encoding="utf-8"))
    return {}


def salvar_config_avatares(config: dict):
    config_path = OUTPUT_DIR.parent / "config_avatares.json"
    config_path.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Config salva em: {config_path}")


# ── CLI de exploração ─────────────────────────────────────────────────────────

def explorar_recursos():
    """Lista avatares e vozes disponíveis para configurar os personagens."""
    client = HeyGenClient()

    print("\n=== Créditos disponíveis ===")
    creditos = client.creditos_restantes()
    print(json.dumps(creditos, indent=2))

    print("\n=== Avatares disponíveis ===")
    avatares = client.listar_avatares()
    for av in avatares[:20]:
        print(f"  ID: {av.get('avatar_id')} | Nome: {av.get('avatar_name')} | Gênero: {av.get('gender')}")

    print(f"\n  ... e mais {max(0, len(avatares) - 20)} avatares")

    print("\n=== Vozes em Português ===")
    vozes = client.listar_vozes("Portuguese")
    for v in vozes:
        print(f"  ID: {v.get('voice_id')} | Nome: {v.get('display_name')} | Gênero: {v.get('gender')}")


if __name__ == "__main__":
    import sys

    if "--explorar" in sys.argv:
        explorar_recursos()
    else:
        print("Use: python heygen_client.py --explorar")
        print("     Para ver avatares e vozes disponíveis na sua conta.")
