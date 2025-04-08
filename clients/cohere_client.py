import cohere

from clients.gpt4all_client import generate_gpt4all_text

# Inicializa el cliente de Cohere con tu API key.
co = cohere.Client(api_key="r2W7dzTlvwxjBFsKXedUVUm08X0RvjAVAHZfDcVX")

def generate_cohere_text(content: str, preamble: str = None, documents: list = None) -> str:
    """
    Llama a la API de Cohere y retorna el texto generado.
    """
    
    response = co.chat(
        model="command-r-plus",
        message=content,
        preamble=preamble,
        documents=documents,
        temperature=0.5
    )
    return response.text
    # return generate_gpt4all_text(content,preamble,documents)