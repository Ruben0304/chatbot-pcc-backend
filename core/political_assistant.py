import requests
import json
from clients.cohere_client import generate_cohere_text
from util.assistant_prompts import GENERAL_PROMPT, ASSISTANT_PROMPT
from repository.apiConfigRepository import ApiConfigRepository

def generate_multi_endpoint_prompt() -> str:
    """Genera el prompt para determinar múltiples endpoints relevantes"""
    config = ApiConfigRepository.get_configuration()
    
    prompt = "Tienes los siguientes endpoints disponibles:\n\n"
    
    for endpoint_name, endpoint in config.endpoints.items():
        if endpoint_name not in ['chat_endpoint_chat_post', 'test_new_endpoint_testnewendpoint_get']:
            prompt += f"- **{endpoint_name}**: {endpoint.description}\n"
            prompt += f"  Palabras clave: {', '.join(endpoint.keywords)}\n\n"
    
    prompt += """Instrucciones:
- Analiza la pregunta del usuario y determina QUÉ ENDPOINTS son relevantes para responderla completamente.
- Puedes seleccionar UNO O VARIOS endpoints si la pregunta requiere información de múltiples fuentes.
- Responde SOLO con una lista de nombres de endpoints separados por comas, sin explicaciones.
- Si la pregunta requiere información de militantes Y sus núcleos, incluye ambos: militantes,core
- Si la pregunta es sobre reuniones y quién participó, incluye: minutes-political,militantes
- Si es sobre estructura organizacional completa, incluye: core,militantes

Ejemplos:
- "¿Quiénes asistieron a la última reunión?" → minutes-political,militantes
- "Información del núcleo y sus miembros" → core,militantes  
- "¿Qué acuerdos se tomaron en las reuniones del núcleo X?" → minutes-political,core
- "Datos de un militante específico" → militantes"""
    
    return prompt

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

def get_relevant_endpoints(question: str) -> list:
    """Determina los endpoints relevantes usando Cohere y configuración dinámica"""
    try:
        multi_endpoint_prompt = generate_multi_endpoint_prompt()
        endpoints_response = generate_cohere_text(
            content=question,
            preamble=multi_endpoint_prompt
        )
        
        # Procesar la respuesta para obtener lista de endpoints
        endpoints = [ep.strip().lower() for ep in endpoints_response.split(',')]
        
        # Filtrar endpoints válidos
        config = ApiConfigRepository.get_configuration()
        valid_endpoints = [ep for ep in endpoints if ep in config.endpoints]
        
        return valid_endpoints if valid_endpoints else ['unknown']
        
    except Exception as e:
        print(f"Error con Cohere: {str(e)}")
        return ['unknown']

def get_api_data(endpoint: str) -> dict:
    """Obtiene datos del API usando configuración dinámica"""
    try:
        config = ApiConfigRepository.get_configuration()
        
        if endpoint not in config.endpoints:
            print(f"Endpoint '{endpoint}' no encontrado en la configuración")
            return {}
        
        endpoint_config = config.endpoints[endpoint]
        url = config.baseUrl + endpoint_config.path
        
        if endpoint_config.method == "GET":
            response = requests.get(url)
        elif endpoint_config.method == "POST":
            response = requests.post(url)
        else:
            print(f"Método HTTP '{endpoint_config.method}' no soportado")
            return {}
            
        return response.json() if response.status_code == 200 else {}
    except Exception as e:
        print(f"Error en API: {str(e)}")
        return {}

def collect_multi_endpoint_data(endpoints: list, question: str) -> dict:
    """Recolecta datos de múltiples endpoints de manera secuencial"""
    collected_data = {}
    
    for endpoint in endpoints:
        if endpoint == 'unknown':
            continue
            
        print(f"Consultando endpoint: {endpoint}")
        endpoint_data = get_api_data(endpoint)
        
        if endpoint_data:
            collected_data[endpoint] = {
                'data': endpoint_data,
                'source': endpoint,
                'description': get_endpoint_description(endpoint)
            }
        else:
            print(f"No se obtuvieron datos del endpoint: {endpoint}")
    
    return collected_data

def get_endpoint_description(endpoint: str) -> str:
    """Obtiene la descripción de un endpoint desde la configuración"""
    try:
        config = ApiConfigRepository.get_configuration()
        if endpoint in config.endpoints:
            return config.endpoints[endpoint].description
    except Exception:
        pass
    return f"Datos de {endpoint}"

def generate_final_answer_multi(question: str, multi_data: dict) -> str:
    """Genera respuesta usando Cohere con datos de múltiples endpoints"""
    try:
        if not multi_data:
            return "No se encontraron datos relevantes para responder la pregunta"
        
        # Crear documentos estructurados para cada endpoint
        documents = []
        for endpoint, endpoint_info in multi_data.items():
            data_snippet = json.dumps(endpoint_info['data'], ensure_ascii=False)[:8000]
            documents.append({
                "title": f"{endpoint_info['description']} ({endpoint})",
                "snippet": data_snippet
            })
        
        # Prompt mejorado para manejo de múltiples fuentes
        enhanced_prompt = f"""{ASSISTANT_PROMPT}

IMPORTANTE: Tienes acceso a información de múltiples fuentes de datos. Utiliza toda la información relevante para proporcionar una respuesta completa y coherente. Si hay información relacionada entre diferentes fuentes, asegúrate de conectarla de manera inteligente.

Fuentes de datos disponibles: {', '.join(multi_data.keys())}"""
        
        response = generate_cohere_text(
            content=question,
            preamble=enhanced_prompt,
            documents=documents
        )
        return response
        
    except Exception as e:
        print(f"Error generando respuesta multi-endpoint: {str(e)}")
        return "Error procesando la solicitud con múltiples fuentes"


def get_response(question: str) -> str:
    """Función principal del asistente político con soporte multi-endpoint"""
    # Paso 1: Verificar si es pregunta general
    general_response = get_general_response(question)
    if general_response:
        return general_response

    # Paso 2: Determinar endpoints relevantes (puede ser uno o varios)
    relevant_endpoints = get_relevant_endpoints(question)
    if not relevant_endpoints or relevant_endpoints == ['unknown']:
        return "No puedo acceder a esa información en este momento"

    print(f"Endpoints identificados: {relevant_endpoints}")

    # Paso 3: Recopilar datos de todos los endpoints relevantes
    multi_endpoint_data = collect_multi_endpoint_data(relevant_endpoints, question)
    if not multi_endpoint_data:
        return "No hay datos disponibles para consultar"

    # Paso 4: Generar respuesta con datos de múltiples fuentes
    return generate_final_answer_multi(question, multi_endpoint_data)