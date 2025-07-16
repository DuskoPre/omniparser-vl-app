import gradio as gr
from PIL import Image
import io
import base64
import requests
from omniparser import OmniParser

# llama.cpp HTTP API endpoint
LLAMA_CPP_URL = "http://localhost:8080/completion"

# Initialize OmniParser v2 with specified models
parser = OmniParser(
    det_model='dino',   # Detection model for UI elements (DINO model)
    vlm_model='llava',  # Visual language model for interpreting icons (using LLaVA model within OmniParser)
    ocr_model='paddle', # OCR model for text extraction (using PaddleOCR)
    device='cuda'       # Use GPU ('cuda') if available for faster processing
)

# Function to parse the GUI image using OmniParser
def run_omnivision(image: Image.Image):
    result = parser(image)
    rendered_image = result['image']                 # Image with detected regions drawn
    content_list = result.get("content", [])         # List of detected elements and texts
    # Format the parsed output as an enumerated list of elements
    parsed_output = "\n".join(
        [f"{idx + 1}. {c['type']}: {c.get('text', '')}" for idx, c in enumerate(content_list)]
    )
    return rendered_image, parsed_output

# Helper to convert an image to a base64 string (for sending to llama.cpp API)
def image_to_base64(image: Image.Image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

# Function to ask the Qwen2.5-VL model (via llama.cpp HTTP server) a question about the image
def ask_qwen_llamacpp(image: Image.Image, prompt: str):
    image_b64 = image_to_base64(image)
    payload = {
        "prompt": f"<|im_start|>user\n<image>\n{prompt}<|im_end|>\n<|im_start|>assistant\n",
        "n_predict": 512,   # Maximum number of tokens to predict (adjust as needed for response length)
        "images": [image_b64],  # Attach image (as base64 string)
        "stream": False     # We’ll get the complete response in one go (no streaming)
    }
    try:
        response = requests.post(LLAMA_CPP_URL, json=payload)
        response.raise_for_status()
        # The llama.cpp server returns JSON with a "content" field containing the assistant's reply
        return response.json().get("content", "No response from llama.cpp.")
    except Exception as e:
        return f"Error: {str(e)}"

# Build the Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# OmniParser v2 + Qwen2.5-VL via llama.cpp 🚀")

    with gr.Row():
        # Left column: inputs
        with gr.Column():
            image_input = gr.Image(type="pil", label="Upload Screenshot")
            parse_button = gr.Button("Run OmniParser")
            question_input = gr.Textbox(label="Ask a question (Qwen2.5-VL)", placeholder="e.g. What does this UI show?")
            ask_button = gr.Button("Ask Qwen (llama.cpp)")

        # Right column: outputs
        with gr.Column():
            parsed_image_output = gr.Image(type="pil", label="Parsed Image")
            parsed_text_output = gr.Textbox(label="Parsed GUI Elements")
            chat_output = gr.Textbox(label="Vision Chat Response")

    # Define button click events
    parse_button.click(
        fn=run_omnivision,
        inputs=image_input,
        outputs=[parsed_image_output, parsed_text_output]
    )
    ask_button.click(
        fn=ask_qwen_llamacpp,
        inputs=[image_input, question_input],
        outputs=chat_output
    )

# Launch the Gradio app on port 7861, accessible on host network
demo.launch(share=True, server_name="0.0.0.0", server_port=7861)
