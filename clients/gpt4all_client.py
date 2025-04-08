import requests
import json

# Initialize the endpoint for the GPT4All API
GPT4ALL_API_URL = "http://localhost:4891/v1/chat/completions"

def generate_gpt4all_text(content: str, preamble: str = None, documents: list = None, model: str = "Llama 3.1 8B Instruct 128k", max_tokens: int = 10000, temperature: float = 0.28) -> str:
    """
    Calls the GPT4All API and returns the generated text.
    
    Args:
        content: The user message to send to the model
        preamble: Optional context or instructions to prepend to the message
        documents: Optional list of documents to include as context
        model: The model to use (default: "Llama 3.1 8B Instruct 128k")
        max_tokens: Maximum number of tokens to generate
        temperature: Controls randomness (lower is more deterministic)
        
    Returns:
        The generated text response
    """
    # Prepare the message content
    message_content = content
    
    # Add preamble if provided
    if preamble:
        message_content = f"{preamble}\n\n{message_content}"
    
    # Add documents if provided
    if documents:
        docs_text = "\n\n".join([f"Document {i+1}:\n{doc}" for i, doc in enumerate(documents)])
        message_content = f"{message_content}\n\nReference Documents:\n{docs_text}"
    
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": message_content}],
        "max_tokens": max_tokens,
        "temperature": temperature
    }
    
    try:
        response = requests.post(GPT4ALL_API_URL, data=json.dumps(payload))
        response.raise_for_status()  # Raise exception for HTTP errors
        
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Error calling GPT4All API: {e}")
        return f"Error generating response: {str(e)}"