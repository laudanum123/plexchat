# PlexChat

A Flask-based chat application that uses the Perplexity AI API for intelligent conversations. The app maintains conversation history and automatically manages token limits for optimal performance.

## Features

- Real-time chat interface with Perplexity AI
- Multi-turn conversation support
- Automatic token management (max ~100k tokens)
- Conversation history persistence
- Token count display
- Clear chat functionality
- Modern, responsive UI

## Prerequisites

- Python 3.6+
- Perplexity API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/plexchat.git
cd plexchat
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp example.env .env
```
Then edit `.env` and add your Perplexity API key:
```
PPLX_API_KEY=your_api_key_here
```

## Usage

1. Start the Flask application:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

3. Start chatting with the AI!

## Features in Detail

- **Token Management**: The application automatically manages conversation history to stay within the ~100k token limit
- **Conversation History**: All messages are preserved until the token limit is reached
- **Clear Chat**: Option to clear the conversation history and start fresh
- **Token Counter**: Real-time display of current token usage

## Security Notes

- Never commit your `.env` file containing the API key
- The application uses Flask's session management for conversation history
- All sensitive data is properly handled through environment variables

## License

MIT License - feel free to use this project as you wish

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request