from flask import Flask, render_template, request, jsonify, session
import openai
from dotenv import load_dotenv
import os
import tiktoken

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Required for session management

# Initialize OpenAI client with Perplexity API
openai.api_key = os.getenv('PPLX_API_KEY')
openai.api_base = "https://api.perplexity.ai"

# Initialize tokenizer for GPT-3.5/4 (works well with Perplexity models)
tokenizer = tiktoken.get_encoding("cl100k_base")

def count_tokens(messages):
    """Count the total number of tokens in a list of messages."""
    total_tokens = 0
    for message in messages:
        # Add tokens for message format (role, content, etc.)
        total_tokens += 4  # Format tokens
        for key, value in message.items():
            total_tokens += len(tokenizer.encode(str(value)))
    total_tokens += 2  # Add tokens for assistant label
    return total_tokens

def trim_conversation_history(messages, max_tokens=100000):
    """Trim conversation history to stay under the token limit."""
    while count_tokens(messages) > max_tokens and len(messages) > 2:  # Keep at least system and one user message
        # Remove the oldest non-system message
        for i, msg in enumerate(messages):
            if msg["role"] != "system":
                messages.pop(i)
                break
    return messages

@app.route('/')
def home():
    # Initialize empty conversation history with system message
    if 'messages' not in session:
        session['messages'] = [
            {
                "role": "system",
                "content": "You are a helpful AI assistant. Provide clear and concise responses."
            }
        ]
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json['message']
        
        # Get conversation history from session
        messages = session.get('messages', [
            {
                "role": "system",
                "content": "You are a helpful AI assistant. Provide clear and concise responses."
            }
        ])
        
        # Add user message to history
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        # Trim conversation if needed
        messages = trim_conversation_history(messages)
        
        # Create chat completion
        response = openai.ChatCompletion.create(
            model="sonar-reasoning",
            messages=messages
        )
        
        # Extract the assistant's response
        assistant_response = response.choices[0].message.content
        
        # Add assistant's response to history
        messages.append({
            "role": "assistant",
            "content": assistant_response
        })
        
        # Update session with new history
        session['messages'] = messages
        
        # Get token count for monitoring
        current_tokens = count_tokens(messages)
        
        return jsonify({
            'response': assistant_response,
            'token_count': current_tokens
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@app.route('/clear', methods=['POST'])
def clear_history():
    """Clear the conversation history."""
    session['messages'] = [
        {
            "role": "system",
            "content": "You are a helpful AI assistant. Provide clear and concise responses."
        }
    ]
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)
