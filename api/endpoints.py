from fastapi import APIRouter, HTTPException,Request


from model.Message import FeedbackUpdate, ChatRequest
from model.ApiConfiguration import ApiEndpoint, ApiConfigurationUpdate
from useCases.chatUseCase import sendMessage
from useCases.feedbackUseCase import give_feedback
from useCases.feedbackAnalysisUseCase import analyze_feedback
from useCases.apiConfigUseCase import (
    get_api_configuration, 
    update_api_configuration, 
    add_api_endpoint, 
    delete_api_endpoint,
    get_api_endpoint
)

router = APIRouter()
@router.post("/chat")
async def chat_endpoint(chat_request: ChatRequest):
    return sendMessage(chat_request.message)


@router.patch("/messages/{message_id}/feedback")
def update_feedback(message_id: int, feedback: FeedbackUpdate):
    give_feedback(message_id, feedback)

@router.get("/feedback/analysis")
def feedback_analysis():
    """Endpoint para obtener análisis de feedback de los mensajes"""
    return analyze_feedback()

@router.get("/")
async def root():
    return {"message": "Hello World"}

# API Configuration endpoints
@router.get("/api-config")
def get_configuration():
    """Obtiene la configuración completa de APIs"""
    return get_api_configuration()

@router.put("/api-config")
def update_configuration(config_update: ApiConfigurationUpdate):
    """Actualiza la configuración de APIs"""
    return update_api_configuration(config_update)

@router.post("/api-config/endpoints")
def create_endpoint(endpoint: ApiEndpoint):
    """Crea o actualiza un endpoint"""
    return add_api_endpoint(endpoint)

@router.get("/api-config/endpoints/{endpoint_name}")
def get_endpoint_details(endpoint_name: str):
    """Obtiene detalles de un endpoint específico"""
    try:
        return get_api_endpoint(endpoint_name)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/api-config/endpoints/{endpoint_name}")
def remove_endpoint(endpoint_name: str):
    """Elimina un endpoint"""
    return delete_api_endpoint(endpoint_name)

@router.get("/testnewendpoint")
def test_new_endpoint():
    """Endpoint de prueba que devuelve un chiste"""
    return {"chiste": "¿Por qué los programadores prefieren el modo oscuro? Porque la luz atrae bugs! 🐛"} 
