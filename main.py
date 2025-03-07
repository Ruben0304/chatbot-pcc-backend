from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import endpoints
from repository.messagesRepository import MessageRepository

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_origin_regex=".*",  # Permite todos los orígenes mediante una expresión regular
    allow_credentials=True,   # Permite el envío de credenciales
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(endpoints.router)
