import re
import json
import time
from google import genai


def llamar_gemini(prompt: str, api_key: str, status=None, max_retries: int = 5):
    """
    Llama a Gemini 2.5 Flash con exponential backoff ante errores 503/429/UNAVAILABLE.
    Acepta un objeto `status` de Streamlit para actualizar el label durante reintentos.
    Devuelve el objeto response o lanza excepción si se agotan los intentos.
    """
    client = genai.Client(api_key=api_key)
    for intento in range(max_retries):
        try:
            return client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
        except Exception as api_e:
            es_reintentable = (
                "503" in str(api_e) or
                "429" in str(api_e) or
                "UNAVAILABLE" in str(api_e)
            )
            if es_reintentable and intento < max_retries - 1:
                t_espera = 2 ** intento
                if status:
                    status.update(
                        label=f"⏳ Gemini saturado. Reintentando en {t_espera}s ({intento + 1}/{max_retries})...",
                        state="running"
                    )
                time.sleep(t_espera)
            else:
                raise api_e


def parsear_json_respuesta(text: str) -> dict | None:
    """
    Extrae y parsea el primer objeto JSON del texto de respuesta de Gemini.
    Devuelve el dict parseado, o None si no hay JSON válido.
    """
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if not match:
        return None
    try:
        return json.loads(match.group(0))
    except json.JSONDecodeError:
        return None
