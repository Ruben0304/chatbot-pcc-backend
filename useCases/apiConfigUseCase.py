from repository.apiConfigRepository import ApiConfigRepository
from model.ApiConfiguration import ApiConfiguration, ApiConfigurationUpdate, ApiEndpoint

def get_api_configuration() -> ApiConfiguration:
    """Obtiene la configuración completa de APIs"""
    return ApiConfigRepository.get_configuration()

def update_api_configuration(config_update: ApiConfigurationUpdate) -> ApiConfiguration:
    """Actualiza la configuración de APIs"""
    return ApiConfigRepository.update_configuration(config_update)

def add_api_endpoint(endpoint: ApiEndpoint) -> ApiConfiguration:
    """Añade o actualiza un endpoint"""
    return ApiConfigRepository.add_endpoint(endpoint)

def delete_api_endpoint(endpoint_name: str) -> ApiConfiguration:
    """Elimina un endpoint"""
    return ApiConfigRepository.delete_endpoint(endpoint_name)

def get_api_endpoint(endpoint_name: str) -> ApiEndpoint:
    """Obtiene un endpoint específico"""
    endpoint = ApiConfigRepository.get_endpoint(endpoint_name)
    if not endpoint:
        raise ValueError(f"Endpoint '{endpoint_name}' not found")
    return endpoint