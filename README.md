# Dabarqus Python Chatbot UI

DabarqusPythonChatbotUI is a user-friendly interface for interacting with the Dabarqus retrieval-augmented generation (RAG) system. It provides a chat-like interface where users can select memory banks and engage in conversations powered by Dabarqus's semantic search capabilities.

## Features

- Interactive chat interface
- Memory bank selection
- Integration with Dabarqus API for semantic search
- Powered by Gradio for easy web deployment

## Prerequisites

- Python 3.8+
- Dabarqus server running and accessible

## Installation

1. Clone the repository:  
`git clone https://github.com/yourusername/DabarqusChatbotUI.git`  
`cd DabarqusChatbotUI`  
The application will start and provide a local URL (usually http://127.0.0.1:7860). Open this URL in your web browser to access the chat interface.

1. Select a memory bank from the dropdown menu.
2. Type your message in the text box.
3. Click "Send" or press Enter to submit your query.
4. View the AI's response in the chat window.

## File Structure

- `app.py`: Main application file containing the Gradio interface
- `retriever.py`: Contains functions for interacting with the Dabarqus API
- `templates/`: Directory containing prompt templates
- `sample_prompt.md`: Sample prompt file for the chatbot

## Contributing

Contributions to DabarqusChatbotUI are welcome! Please feel free to submit a Pull Request.

## License

TODO
