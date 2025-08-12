# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a FastAPI-based chatbot for the Cuban Communist Party (PCC) at CUJAE university. It implements a RAG (Retrieval-Augmented Generation) architecture to provide information about party members, political acts, and nuclei using dynamic API configuration and Cohere's AI models.

## Development Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run development server (default port 8000)
uvicorn main:app --reload

# Run on custom port (as configured in main.py)
uvicorn main:app --host 127.0.0.1 --port 82 --reload

# Test endpoints manually
# Use test_main.http file with REST client extensions
```

## Architecture Overview

### Core Components

**main.py**: FastAPI application entry point with CORS middleware configuration allowing all origins, credentials, methods, and headers.

**api/endpoints.py**: REST API router with endpoints:
- `/chat` (POST) - Main chatbot interaction
- `/messages/{message_id}/feedback` (PATCH) - User feedback collection
- `/feedback/analysis` (GET) - Feedback analytics
- `/api-config/*` - Dynamic API configuration management

**core/political_assistant.py**: RAG implementation with three-step process:
1. **General Response Check**: Determines if query is general knowledge vs specific data lookup
2. **Dynamic Endpoint Selection**: Uses Cohere to map user queries to configured API endpoints
3. **Response Generation**: Fetches data from external APIs and generates contextualized responses

### Dynamic Configuration System

The system uses `database/api_configuration.json` to dynamically configure:
- **Base URL**: External API base endpoint (`https://part-back.onrender.com`)
- **Endpoints**: Configurable endpoints with descriptions, paths, methods, fields, and keywords
- **Auto-routing**: Cohere AI automatically routes questions to appropriate endpoints based on keywords

Current configured endpoints:
- `militantes` - Party member information
- `minutes-political` - Political meeting minutes  
- `core` - Nucleus/organization structure

### Data Flow Architecture

```
User Query → General Check → [If Specific] → Endpoint Selection → API Fetch → AI Response Generation
           ↘ [If General] → Direct AI Response
```

### Repository Pattern

**repository/messagesRepository.py**: MongoDB data access layer
- Connection: MongoDB Atlas with hardcoded URI (line 13)
- Collections: `chatbot-pcc.messages` for conversation history
- Operations: CRUD for messages and feedback updates

**repository/apiConfigRepository.py**: JSON-based configuration management for dynamic API endpoints

### Use Cases Layer

**useCases/chatUseCase.py**: Main chat logic with async message persistence
**useCases/feedbackUseCase.py**: Feedback collection and storage
**useCases/feedbackAnalysisUseCase.py**: Feedback analytics and insights
**useCases/apiConfigUseCase.py**: API configuration CRUD operations

## External Dependencies

**Cohere Integration**: 
- Client: `clients/cohere_client.py` 
- Model: `command-r-plus`
- API Key: Hardcoded in client (line 6) - should be moved to environment variables

**External API**: `https://part-back.onrender.com` for political data retrieval

**MongoDB Atlas**: Cloud database for persistence with connection string in `messagesRepository.py:13`

## Deployment Configuration

**vercel.json**: Configured for Vercel deployment
- Runtime: Python 3.9
- Max Lambda Size: 15mb
- Entry Point: `main.py`

## Key Patterns

### Dynamic Prompt Generation
The system generates AI prompts dynamically based on configured endpoints, allowing for runtime API configuration changes without code modifications.

### Async Message Persistence
Chat responses are returned immediately while database storage happens asynchronously via threading to improve user experience.

### Two-Stage AI Processing
Uses Cohere twice: first to classify query type and route to endpoints, then to generate final responses with retrieved data.

### Pydantic Models
Structured data validation using Pydantic models in `model/Message.py` and `model/ApiConfiguration.py` for type safety and API documentation.

## Security Considerations

- API keys are hardcoded and should be moved to environment variables
- MongoDB connection string is hardcoded and should use environment variables  
- CORS is configured to allow all origins (`*`) - should be restricted for production
- No authentication/authorization implemented on endpoints