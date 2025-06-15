#!/usr/bin/env python3
"""
G4F API Server for Vercel with Streaming Support
This Flask API server provides access to AI models through the g4f library.
Optimized for serverless deployment on Vercel with streaming response capability.
"""

import os
import logging
import json
import uuid
from typing import Dict, List, Optional, Union, Any, Generator
from datetime import datetime
from flask import Flask, request, jsonify, Response, stream_template
from flask_cors import CORS

# G4F imports
import g4f
from g4f.client import Client as G4FClient

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Available models in g4f
AVAILABLE_MODELS = [
    {"id": "gpt-3.5-turbo", "name": "GPT-3.5 Turbo", "description": "Fast and efficient"},
    {"id": "gpt-4", "name": "GPT-4", "description": "Advanced reasoning"},
    {"id": "gpt-4o", "name": "GPT-4o", "description": "Latest GPT-4 version"},
    {"id": "gpt-4o-mini", "name": "GPT-4o Mini", "description": "Compact but powerful"},
    {"id": "claude-3-opus", "name": "Claude-3 Opus", "description": "Anthropic's flagship model"},
    {"id": "claude-3-sonnet", "name": "Claude-3 Sonnet", "description": "Balanced Claude model"},
    {"id": "gemini-pro", "name": "Gemini Pro", "description": "Google's AI model"},
]

# Default settings
DEFAULT_SETTINGS = {
    "model": "gpt-4o-mini",
    "temperature": 0.7,
    "max_tokens": 1000,
    "web_search": False,
}

# Session storage - for Vercel, this will reset on each cold start
# For production, consider using a database or Redis
sessions = {}

class ChatSession:
    """Class to manage chat session data"""
    
    def __init__(self, session_id: str, settings: Dict[str, Any] = None):
        self.session_id = session_id
        self.settings = settings or DEFAULT_SETTINGS.copy()
        self.history = []
        self.created_at = datetime.now()
        self.last_activity = datetime.now()
        self.client = G4FClient()
    
    def add_message(self, role: str, content: str) -> None:
        """Add a message to the conversation history"""
        self.history.append({"role": role, "content": content})
        self.last_activity = datetime.now()
    
    def get_history(self) -> List[Dict[str, str]]:
        """Get the conversation history"""
        return self.history
    
    def clear_history(self) -> None:
        """Clear the conversation history"""
        self.history = []
        self.last_activity = datetime.now()
    
    def update_settings(self, settings: Dict[str, Any]) -> None:
        """Update session settings"""
        self.settings.update(settings)
        self.last_activity = datetime.now()
    
    def get_response(self, message: str = None) -> str:
        """Get a response from the AI model (non-streaming)"""
        if message:
            self.add_message("user", message)
        
        try:
            # First try using the client API
            response = self.client.chat.completions.create(
                model=self.settings["model"],
                messages=self.get_history(),
                temperature=self.settings["temperature"],
                max_tokens=self.settings["max_tokens"],
                web_search=self.settings["web_search"],
            )
            ai_response = response.choices[0].message.content
            
        except Exception as e:
            logger.warning(f"G4F client API failed: {e}, falling back to direct method")
            try:
                # Fallback to direct method
                ai_response = g4f.ChatCompletion.create(
                    model=self.settings["model"],
                    messages=self.get_history(),
                    temperature=self.settings["temperature"],
                )
                
            except Exception as e2:
                logger.error(f"G4F direct method also failed: {e2}")
                raise Exception(f"Failed to get response: {str(e2)}")
        
        self.add_message("assistant", ai_response)
        return ai_response
    
    def get_streaming_response(self, message: str = None) -> Generator[str, None, None]:
        """Get a streaming response from the AI model"""
        if message:
            self.add_message("user", message)
        
        full_response = ""
        
        try:
            # Try using the client API with streaming
            try:
                response = self.client.chat.completions.create(
                    model=self.settings["model"],
                    messages=self.get_history(),
                    temperature=self.settings["temperature"],
                    max_tokens=self.settings["max_tokens"],
                    web_search=self.settings["web_search"],
                    stream=True
                )
                
                for chunk in response:
                    if hasattr(chunk, 'choices') and chunk.choices:
                        delta = chunk.choices[0].delta
                        if hasattr(delta, 'content') and delta.content:
                            content = delta.content
                            full_response += content
                            yield content
                            
            except Exception as e:
                logger.warning(f"G4F client streaming failed: {e}, falling back to direct method")
                
                # Fallback to direct method with streaming
                response = g4f.ChatCompletion.create(
                    model=self.settings["model"],
                    messages=self.get_history(),
                    temperature=self.settings["temperature"],
                    stream=True
                )
                
                for chunk in response:
                    if chunk:
                        full_response += chunk
                        yield chunk
                        
        except Exception as e:
            logger.error(f"All streaming methods failed: {e}")
            error_msg = f"Ошибка при получении ответа: {str(e)}"
            full_response = error_msg
            yield error_msg
        
        # Add the complete response to history
        if full_response:
            self.add_message("assistant", full_response)

def get_session(session_id: str) -> ChatSession:
    """Get or create a session"""
    if session_id not in sessions:
        sessions[session_id] = ChatSession(session_id)
    return sessions[session_id]

@app.route('/', methods=['GET'])
def index():
    """Root endpoint for health check"""
    return jsonify({
        "success": True,
        "message": "G4F API Server is running with streaming support",
        "version": "1.1.0",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/models', methods=['GET'])
def get_models():
    """Get available models"""
    return jsonify({
        "success": True,
        "models": AVAILABLE_MODELS
    })

@app.route('/api/sessions', methods=['GET'])
def list_sessions():
    """List all sessions"""
    result = []
    for session_id, session in sessions.items():
        result.append({
            "session_id": session_id,
            "created_at": session.created_at.isoformat(),
            "last_activity": session.last_activity.isoformat(),
            "message_count": len(session.history),
            "settings": session.settings
        })
    
    return jsonify({
        "success": True,
        "sessions": result
    })

@app.route('/api/sessions', methods=['POST'])
def create_session():
    """Create a new session"""
    data = request.json or {}
    settings = data.get('settings', DEFAULT_SETTINGS.copy())
    
    # Validate model
    if settings.get('model') and not any(m['id'] == settings['model'] for m in AVAILABLE_MODELS):
        return jsonify({
            "success": False,
            "error": f"Invalid model: {settings['model']}"
        }), 400
    
    # Create session
    session_id = str(uuid.uuid4())
    sessions[session_id] = ChatSession(session_id, settings)
    
    return jsonify({
        "success": True,
        "session_id": session_id,
        "settings": settings
    })

@app.route('/api/sessions/<session_id>', methods=['GET'])
def get_session_info(session_id):
    """Get session information"""
    if session_id not in sessions:
        return jsonify({
            "success": False,
            "error": "Session not found"
        }), 404
    
    session = sessions[session_id]
    
    return jsonify({
        "success": True,
        "session_id": session_id,
        "created_at": session.created_at.isoformat(),
        "last_activity": session.last_activity.isoformat(),
        "message_count": len(session.history),
        "settings": session.settings
    })

@app.route('/api/sessions/<session_id>', methods=['DELETE'])
def delete_session(session_id):
    """Delete a session"""
    if session_id not in sessions:
        return jsonify({
            "success": False,
            "error": "Session not found"
        }), 404
    
    del sessions[session_id]
    
    return jsonify({
        "success": True,
        "message": f"Session {session_id} deleted"
    })

@app.route('/api/sessions/<session_id>/settings', methods=['PUT'])
def update_session_settings(session_id):
    """Update session settings"""
    if session_id not in sessions:
        return jsonify({
            "success": False,
            "error": "Session not found"
        }), 404
    
    data = request.json or {}
    if not data:
        return jsonify({
            "success": False,
            "error": "No settings provided"
        }), 400
    
    # Validate model if provided
    if data.get('model') and not any(m['id'] == data['model'] for m in AVAILABLE_MODELS):
        return jsonify({
            "success": False,
            "error": f"Invalid model: {data['model']}"
        }), 400
    
    session = sessions[session_id]
    session.update_settings(data)
    
    return jsonify({
        "success": True,
        "settings": session.settings
    })

@app.route('/api/sessions/<session_id>/history', methods=['GET'])
def get_session_history(session_id):
    """Get session history"""
    if session_id not in sessions:
        return jsonify({
            "success": False,
            "error": "Session not found"
        }), 404
    
    session = sessions[session_id]
    
    return jsonify({
        "success": True,
        "history": session.get_history()
    })

@app.route('/api/sessions/<session_id>/history', methods=['DELETE'])
def clear_session_history(session_id):
    """Clear session history"""
    if session_id not in sessions:
        return jsonify({
            "success": False,
            "error": "Session not found"
        }), 404
    
    session = sessions[session_id]
    session.clear_history()
    
    return jsonify({
        "success": True,
        "message": "History cleared"
    })

@app.route('/api/sessions/<session_id>/chat', methods=['POST'])
def chat(session_id):
    """Send a message and get a response (non-streaming)"""
    if session_id not in sessions:
        return jsonify({
            "success": False,
            "error": "Session not found"
        }), 404
    
    data = request.json or {}
    message = data.get('message')
    
    if not message:
        return jsonify({
            "success": False,
            "error": "No message provided"
        }), 400
    
    session = sessions[session_id]
    
    try:
        response = session.get_response(message)
        
        return jsonify({
            "success": True,
            "response": response,
            "history": session.get_history()
        })
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/sessions/<session_id>/chat/stream', methods=['POST'])
def chat_stream(session_id):
    """Send a message and get a streaming response"""
    if session_id not in sessions:
        return jsonify({
            "success": False,
            "error": "Session not found"
        }), 404
    
    data = request.json or {}
    message = data.get('message')
    
    if not message:
        return jsonify({
            "success": False,
            "error": "No message provided"
        }), 400
    
    session = sessions[session_id]
    
    def generate():
        """Generator function for streaming response"""
        try:
            # Send initial success message
            yield f"data: {json.dumps({'success': True, 'type': 'start'})}\n\n"
            
            # Stream the AI response
            for chunk in session.get_streaming_response(message):
                if chunk:
                    yield f"data: {json.dumps({'success': True, 'type': 'chunk', 'content': chunk})}\n\n"
            
            # Send completion message with updated history
            yield f"data: {json.dumps({'success': True, 'type': 'end', 'history': session.get_history()})}\n\n"
            
        except Exception as e:
            logger.error(f"Error in streaming chat: {e}")
            yield f"data: {json.dumps({'success': False, 'error': str(e)})}\n\n"
    
    return Response(
        generate(),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
        }
    )

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "success": True,
        "status": "healthy",
        "version": "1.1.0",
        "features": ["streaming", "sessions", "multiple_models"],
        "timestamp": datetime.now().isoformat()
    })

# Special handler for Vercel serverless functions
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def catch_all(path):
    """Catch-all route for Vercel"""
    return jsonify({
        "success": False,
        "error": f"Endpoint not found: /{path}",
        "available_endpoints": [
            "/api/models",
            "/api/sessions",
            "/api/sessions/<session_id>",
            "/api/sessions/<session_id>/settings",
            "/api/sessions/<session_id>/history",
            "/api/sessions/<session_id>/chat",
            "/api/sessions/<session_id>/chat/stream",
            "/api/health"
        ]
    }), 404

# For local development
if __name__ == '__main__':
    # Get port from environment variable or use default
    port = int(os.environ.get('PORT', 5000))
    
    # Run the app
    app.run(host='0.0.0.0', port=port, debug=True)

