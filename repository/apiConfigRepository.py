import json
import os
from typing import Dict, Optional
from model.ApiConfiguration import ApiConfiguration, ApiConfigurationUpdate, ApiEndpoint

class ApiConfigRepository:
    CONFIG_FILE_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'api_configuration.json')
    
    @staticmethod
    def _ensure_config_file():
        """Asegura que el archivo de configuración existe"""
        if not os.path.exists(ApiConfigRepository.CONFIG_FILE_PATH):
            # Crear configuración por defecto
            default_config = {
                "baseUrl": "https://part-back.onrender.com",
                "endpoints": {}
            }
            with open(ApiConfigRepository.CONFIG_FILE_PATH, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=2, ensure_ascii=False)
    
    @staticmethod
    def get_configuration() -> ApiConfiguration:
        """Obtiene la configuración completa de APIs"""
        ApiConfigRepository._ensure_config_file()
        
        try:
            with open(ApiConfigRepository.CONFIG_FILE_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return ApiConfiguration(**data)
        except Exception as e:
            print(f"Error reading configuration: {e}")
            # Retornar configuración por defecto
            return ApiConfiguration(baseUrl="https://part-back.onrender.com", endpoints={})
    
    @staticmethod
    def update_configuration(config_update: ApiConfigurationUpdate) -> ApiConfiguration:
        """Actualiza la configuración de APIs"""
        current_config = ApiConfigRepository.get_configuration()
        
        # Actualizar campos si se proporcionan
        if config_update.baseUrl is not None:
            current_config.baseUrl = config_update.baseUrl
        
        if config_update.endpoints is not None:
            current_config.endpoints.update(config_update.endpoints)
        
        # Guardar la configuración actualizada
        ApiConfigRepository._save_configuration(current_config)
        
        return current_config
    
    @staticmethod
    def add_endpoint(endpoint: ApiEndpoint) -> ApiConfiguration:
        """Añade o actualiza un endpoint"""
        current_config = ApiConfigRepository.get_configuration()
        current_config.endpoints[endpoint.name] = endpoint
        
        ApiConfigRepository._save_configuration(current_config)
        return current_config
    
    @staticmethod
    def delete_endpoint(endpoint_name: str) -> ApiConfiguration:
        """Elimina un endpoint"""
        current_config = ApiConfigRepository.get_configuration()
        
        if endpoint_name in current_config.endpoints:
            del current_config.endpoints[endpoint_name]
            ApiConfigRepository._save_configuration(current_config)
        
        return current_config
    
    @staticmethod
    def get_endpoint(endpoint_name: str) -> Optional[ApiEndpoint]:
        """Obtiene un endpoint específico"""
        config = ApiConfigRepository.get_configuration()
        return config.endpoints.get(endpoint_name)
    
    @staticmethod
    def _save_configuration(config: ApiConfiguration):
        """Guarda la configuración en el archivo JSON"""
        try:
            # Convertir a diccionario para serialización
            config_dict = {
                "baseUrl": config.baseUrl,
                "endpoints": {
                    name: {
                        "name": endpoint.name,
                        "description": endpoint.description,
                        "path": endpoint.path,
                        "method": endpoint.method,
                        "fields": [
                            {
                                "name": field.name,
                                "type": field.type,
                                "description": field.description
                            }
                            for field in endpoint.fields
                        ],
                        "keywords": endpoint.keywords
                    }
                    for name, endpoint in config.endpoints.items()
                }
            }
            
            with open(ApiConfigRepository.CONFIG_FILE_PATH, 'w', encoding='utf-8') as f:
                json.dump(config_dict, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving configuration: {e}")
            raise