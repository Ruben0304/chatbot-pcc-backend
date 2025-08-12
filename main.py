from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import endpoints
from repository.messagesRepository import MessageRepository

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Solo permite estos orígenes
    allow_credentials=True,  # Permite el envío de credenciales
    allow_methods=["*"],  # Permite todos los métodos HTTP
    allow_headers=["*"],  # Permite todos los encabezados
)

app.include_router(endpoints.router)

@app.get("/testnewendpoint") 
def test_new_endpoint():
    """Endpoint de prueba que devuelve un chiste"""
    return {"chiste": "¿Por qué los programadores prefieren el modo oscuro? Porque la luz atrae bugs! 🐛"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=82)
