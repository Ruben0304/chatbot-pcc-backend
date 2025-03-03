import random
from datetime import datetime

from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware

from cohere_client import generate_cohere_text
from political_assistant import political_assistant

app = FastAPI()


# Lista de respuestas aleatorias
possible_responses = [
    "Claro, puedo ayudarte con eso.",
    "Interesante pregunta, déjame ver...",
    "Lo siento, en este momento no tengo información al respecto.",
    "Según mis datos, el KPI ha mostrado una tendencia positiva.",
    "¿Podrías especificar un poco más tu consulta?",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_origin_regex=".*",  # Permite todos los orígenes mediante una expresión regular
    allow_credentials=True,   # Permite el envío de credenciales
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/chat")
async def chat_endpoint(request: Request):
    data = await request.json()
    user_message = data.get("message", "")

    # Llama a la función del asistente político
    response_text = political_assistant(user_message)

    # Genera un timestamp (por ejemplo, en formato "HH:MM")
    timestamp = datetime.now().strftime("%H:%M")

    return {"response": response_text, "timestamp": timestamp}
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
