from typing import Dict, List, Tuple
from repository.messagesRepository import MessageRepository
import random  # Añadido para generar datos aleatorios

# Función original comentada
"""
def analyze_feedback() -> Dict:
    # Obtener todos los mensajes
    messages = MessageRepository.get_all_messages()
    
    # Inicializar contadores
    total = len(messages)
    positive = 0
    negative = 0
    no_feedback = 0
    negative_reasons = {}
    
    # Analizar cada mensaje
    for message in messages:
        if message.feedback is None:
            no_feedback += 1
        elif message.feedback == "positive":
            positive += 1
        elif message.feedback == "negative":
            negative += 1
            
            # Analizar las razones del feedback negativo
            if message.feedback_type:
                # Extraer la razón principal (antes del ":")
                reason = message.feedback_type.split(":")[0].strip()
                negative_reasons[reason] = negative_reasons.get(reason, 0) + 1
    
    # Preparar el resultado
    result = {
        "total_messages": total,
        "positive_feedback": positive,
        "negative_feedback": negative,
        "no_feedback": no_feedback,
        "negative_reasons": [
            {"reason": reason, "count": count} 
            for reason, count in negative_reasons.items()
        ]
    }
    
    return result
"""

def analyze_feedback() -> Dict:
    """
    Versión mock que genera datos aleatorios de feedback.
    Mantiene una proporción de 92% positivos vs 8% negativos en los feedbacks dados.
    
    Returns:
        Dict: Un diccionario con estadísticas sobre los feedbacks:
            - total_messages: Número total de mensajes (aleatorio entre 77 y 400)
            - positive_feedback: Número de mensajes con feedback positivo (92% de los feedbacks)
            - negative_feedback: Número de mensajes con feedback negativo (8% de los feedbacks)
            - no_feedback: Número de mensajes sin feedback (aleatorio)
            - negative_reasons: Lista de razones de feedback negativo con su frecuencia
    """
    # Generar un número total aleatorio de mensajes entre 77 y 400
    total_messages = random.randint(77, 400)
    
    # Determinar cuántos mensajes tendrán feedback (entre 50% y 90% del total)
    feedback_percentage = random.uniform(0.5, 0.9)
    messages_with_feedback = int(total_messages * feedback_percentage)
    
    # Calcular mensajes sin feedback
    no_feedback = total_messages - messages_with_feedback
    
    # Aplicar la proporción 92% positivos, 8% negativos
    negative_feedback = int(messages_with_feedback * 0.08)
    positive_feedback = messages_with_feedback - negative_feedback
    
    # Generar razones aleatorias para feedback negativo
    possible_reasons = [
        "Respuesta incorrecta", 
        "Información incompleta", 
        "No entendió la pregunta", 
        "Respuesta confusa",
        "Información desactualizada"
    ]
    
    negative_reasons = {}
    for _ in range(negative_feedback):
        reason = random.choice(possible_reasons)
        negative_reasons[reason] = negative_reasons.get(reason, 0) + 1
    
    # Preparar el resultado
    result = {
        "total_messages": total_messages,
        "positive_feedback": positive_feedback,
        "negative_feedback": negative_feedback,
        "no_feedback": no_feedback,
        "negative_reasons": [
            {"reason": reason, "count": count} 
            for reason, count in negative_reasons.items()
        ]
    }
    
    return result