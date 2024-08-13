import gradio as gr
import ollama
from retriever import retrieve_data, convert_prompt_to_retrieval_prompt
import requests


def get_memory_banks():
    url = "http://localhost:6568/api/silk/memorybanks"
    try:
        response = requests.get(url)
        response.raise_for_status()
        memory_banks = response.json()
        # The API response structure isn't specified in the docs, so we're assuming it's a list of objects with a 'name' field
        return [bank.get('name') for bank in memory_banks['SilkMemoryBanks'] if bank.get('name')]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching memory banks: {e}")
        return ["Default"]  # Return a default option if the API call fails


def chat_function(message, history, memory_bank):
    # Convert the user's message to a retrieval prompt
    with open("templates/recipe_template.md") as file:
        prompt_template = file.read()
    retrieval_prompt = convert_prompt_to_retrieval_prompt(message, prompt_template)
    
    # Retrieve data
    retrieved_data = retrieve_data(retrieval_prompt, memory_bank, 10)
    
    # Prepare the prompt for the LLM
    with open("sample_prompt.md") as file:
        retrieval_prompt_template = file.read()
    
    full_prompt = f"{retrieval_prompt_template} : RAG_response {retrieved_data}, keywords: {retrieval_prompt}, original_prompt: {message}"
    
    # Use Ollama to generate a response
    response = ""
    stream = ollama.chat(
        model="llama3",  # or whichever model you're using
        messages=[{"role": "system", "content": "Your system prompt here"}, 
                  {"role": "user", "content": full_prompt}],
        stream=True,
    )
    
    for chunk in stream:
        response += chunk['message']['content']
        yield history + [("Human", message), ("AI", response)]

def enable_textbox(choice):
    return gr.update(interactive=True if choice else False)

# Set up the Gradio interface
with gr.Blocks(title="dabarqus") as demo:
    memory_banks = get_memory_banks()
    memory_bank = gr.Dropdown(choices=memory_banks, label="Select Memory Bank", value=None, allow_custom_value=False)
    chatbot = gr.Chatbot()
    with gr.Row():
        msg = gr.Textbox(label="Type your message here", placeholder="Enter your question...", interactive=False)
        submit = gr.Button("Send", interactive=False)
    clear = gr.Button("Clear Chat")

    memory_bank.change(enable_textbox, inputs=[memory_bank], outputs=[msg])
    memory_bank.change(lambda x: gr.update(interactive=True if x else False), inputs=[memory_bank], outputs=[submit])

    msg.submit(chat_function, inputs=[msg, chatbot, memory_bank], outputs=[chatbot])
    submit.click(chat_function, inputs=[msg, chatbot, memory_bank], outputs=[chatbot])
    clear.click(lambda: None, None, chatbot, queue=False)

# Launch the app
if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",  # Makes the app accessible on your local network
    )