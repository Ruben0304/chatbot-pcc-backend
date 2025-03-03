import requests
import json
from cohere_client import generate_cohere_text

# Configuración inicial
BASE_URL = "https://part-back.onrender.com"

# Definir los prompts originales
ENDPOINT_PROMPT = """Tienes los siguientes endpoints disponibles:

1. **militantes**: 
   - Descripción: Obtiene información sobre los militantes.
   - Campos: `id`, `firstname`, `lastname`, `email`, `organization`, `estado`, `address`, `phone`, `core`, `abscents`.

2. **minutes-political**: 
   - Descripción: Obtiene actas políticas.
   - Campos: `id`, `name`, `status`, `fecha`, `hora`, `lugar`, `createdAt`, `total`, `ausentes`, `porciento`, `total_trabajador`, `total_organismo`, `causa`, `tema`, `planteamientos`, `acuerdos`, `valoracion`, `name_orientador`, `name_secretario`, `core`.

3. **core**: 
   - Descripción: Obtiene información sobre el núcleo (core) y sus militantes.
   - Campos: `id`, `name`, `secretarioGeneral`, `secretarioFuncionamiento`, `comite`, `militantes`, `actas`, `actas_cp`, `computo`.

Instrucciones:
- Solo responde con el nombre del endpoint que corresponda a la pregunta del usuario.
- No agregues explicaciones, comentarios ni ningún otro texto.

Ejemplos:
- Pregunta: "Necesito los datos de los militantes."
  Respuesta: militantes
- Pregunta: "¿Dónde puedo ver las actas políticas?"
  Respuesta: minutes-political
- Pregunta: "Quiero información sobre el núcleo."
  Respuesta: core."""

ASSISTANT_PROMPT = """Eres un asistente virtual inteligente y profesional. Te proporcionaré información relevante y una pregunta basada en esa información. Tu tarea es responder la pregunta de manera clara y precisa, utilizando solo la información proporcionada. Si la pregunta no puede responderse con la información dada, debes indicarlo de manera profesional.

Instrucciones:
1. Analiza la información proporcionada.
2. Responde la pregunta de manera concisa y útil.
3. Si no encuentras la respuesta en la información proporcionada, di: "No encuentro una respuesta precisa en la información proporcionada. ¿Puedes brindarme más detalles o reformular la pregunta?".
4. Mantén un tono profesional y amable en todo momento."""

def get_endpoint(question: str) -> str:
    """Determina el endpoint correcto usando Cohere"""
    try:
        endpoint = generate_cohere_text(
            content=question,
            preamble=ENDPOINT_PROMPT
        )
        return endpoint.strip().lower()
    except Exception as e:
        print(f"Error con Cohere: {str(e)}")
        return "unknown"

def get_api_data(endpoint: str) -> dict:
    """Obtiene datos del API"""
    try:
        response = requests.get(f"{BASE_URL}/{endpoint}")
        return response.json() if response.status_code == 200 else {}
    except Exception as e:
        print(f"Error en API: {str(e)}")
        return {}

def generate_answer(question: str, data: dict) -> str:
    """Genera respuesta usando Cohere con datos del API"""
    try:
        info = json.dumps(data, ensure_ascii=False)[:2000]  # Limitar tamaño para el modelo
        response = generate_cohere_text(
            content=question,
            preamble=ASSISTANT_PROMPT,
            documents=[{"title": "Datos API", "snippet": info}]
        )
        return response
    except Exception as e:
        print(f"Error generando respuesta: {str(e)}")
        return "Error procesando la solicitud"

def political_assistant(question: str) -> str:
    """Función principal del asistente político"""
    # Paso 1: Determinar endpoint
    endpoint = get_endpoint(question)
    if endpoint == "unknown":
        return "No puedo acceder a esa información en este momento"

    # Paso 2: Obtener datos
    api_data = get_api_data(endpoint)
    if not api_data:
        return "No hay datos disponibles para consultar"

    # Paso 3: Generar respuesta
    return generate_answer(question, api_data)