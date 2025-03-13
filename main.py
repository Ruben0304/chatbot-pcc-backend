from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import endpoints
from repository.messagesRepository import MessageRepository

app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["https://chatbot-pcc-cujae.vercel.app"],  # Solo permite este origen
#     allow_credentials=True,  # Permite el envío de credenciales
#     allow_methods=["*"],  # Permite todos los métodos HTTP
#     allow_headers=["*"],  # Permite todos los encabezados
# )

app.include_router(endpoints.router)
