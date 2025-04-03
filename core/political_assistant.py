import requests
import json
from clients.cohere_client import generate_cohere_text
from util.assistant_prompts import GENERAL_PROMPT, ENDPOINT_PROMPT, ASSISTANT_PROMPT

# Configuración inicial
BASE_URL = "https://part-back.onrender.com"

def get_general_response(question: str) -> str:
    """Maneja preguntas generales no relacionadas con documentos"""
    try:
        response = generate_cohere_text(
            content=question,
            preamble=GENERAL_PROMPT,
        )
        
        # Intentar parsear la respuesta como JSON
        try:
            parsed_response = json.loads(response)
            if parsed_response.get("is_general", False):
                return parsed_response.get("response", "")
            else:
                return ""
        except json.JSONDecodeError:
            # Fallback para compatibilidad con versiones anteriores
            print("Advertencia: Respuesta no está en formato JSON")
            return response if response.lower() != "no" else ""
            
    except Exception as e:
        print(f"Error en respuesta general: {str(e)}")
        return ""

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

def generate_final_answer(question: str, data: dict) -> str:
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


def get_response(question: str) -> str:
    """Función principal del asistente político"""
    # Nuevo paso: Verificar si es pregunta general
    general_response = get_general_response(question)
    if general_response:
        return general_response

    # Mantener el flujo original para consultas específicas
    endpoint = get_endpoint(question)
    if endpoint == "unknown":
        return "No puedo acceder a esa información en este momento"

    api_data = get_api_data(endpoint)
    if not api_data:
        return "No hay datos disponibles para consultar"

    return generate_final_answer(question, api_data)