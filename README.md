# omniparser-vl-app
# OmniParser-VL-App 🚀

This repository contains a Dockerized Gradio application that combines **Microsoft OmniParser v2** (for GUI screenshot parsing) with **Qwen 2.5-VL-32B** (a vision-language model) via `llama.cpp`. The app can analyze a screenshot of a user interface, list its GUI elements, and answer questions about the UI.

## Features

- **OmniParser v2** for extracting structured GUI elements (buttons, icons, text fields, etc.) and their associated text or icon descriptions from a screenshot.
- **Qwen 2.5-VL (32B)** via `llama.cpp` for answering questions about the image (visual Q&A or description), running locally.
- **Gradio UI** to upload an image, run the parser, and interact with the vision-language model.

## Project Structure

omniparser-vl-app/
├── Dockerfile # Docker configuration to set up environment and run servers
├── app.py # Gradio application code (OmniParser + Qwen VL integration)
├── requirements.txt # Python dependencies for the app
└── models/
└── qwen2.5-vl-32b.QwenMM.gguf # (Not included) Qwen model file to be placed here (see below)
bash
Kopieren
Bearbeiten

> **Note:** The `qwen2.5-vl-32b.QwenMM.gguf` model file is **not stored in this Git repo**. You need to download it separately (instructions below) because it’s large.

## Getting Started

### 1. Download the Qwen2.5-VL Model

Obtain the Qwen 2.5-VL 32B model in GGUF format and place it in the `models/` directory. For example, you can download a Qwen-VL-Chat GGUF from Hugging Face:


mkdir -p models
wget -O models/qwen2.5-vl-32b.QwenMM.gguf \
  https://huggingface.co/Qwen/Qwen-VL-Chat-GGUF/resolve/main/qwen2.5-vl-32b.QwenMM.gguf
Ensure the file path matches what is used in the Docker CMD (/app/models/qwen2.5-vl-32b.QwenMM.gguf). If you download a different variant or quantization, update the Dockerfile CMD accordingly.

### 2. Build the Docker Image
Build the Docker image using the provided Dockerfile:
bash
Kopieren
Bearbeiten
docker build -t omniparser-vl-app .
This will create a Docker image named omniparser-vl-app containing:
OmniParser v2 and its dependencies (YOLO-based detector, etc.),
The Gradio app (app.py),
llama.cpp built with HTTP server support,
(No model inside yet – we’ll provide the model at runtime).
Note: If you plan to run the model on CPU only, you might remove nvidia/cuda base image and use a lighter base. The current setup assumes you have an NVIDIA GPU and CUDA for optimal performance (especially since Qwen2.5-32B is a large model).

### 3. Run the Container
Run the Docker container, exposing the necessary ports and mounting the model file into it:
bash
Kopieren
Bearbeiten
docker run --gpus all -p 7861:7861 -p 8080:8080 \
  -v $(pwd)/models:/app/models \
  omniparser-vl-app
Explanation:
--gpus all enables GPU access for the container (remove this if running on CPU).
-p 7861:7861 maps the Gradio app to your host’s port 7861.
-p 8080:8080 maps the llama.cpp completion API to host port 8080 (in case you want to query it directly or for debugging).
-v $(pwd)/models:/app/models mounts the models folder (with the Qwen GGUF file) into the container’s /app/models. This way, the container can load the model without the image needing to contain it.
omniparser-vl-app is the image name to run.

### 4. Use the Application
Once the container is running:
Open your browser to http://localhost:7861. You should see the Gradio interface.
Upload a screenshot of a GUI.
Click "Run OmniParser" to get the parsed GUI elements (the right panel will show an annotated image and a list of elements).
(Optional) Enter a question in the text box (for example, "What is the purpose of this window?" or "Describe the interface.") and click "Ask Qwen (llama.cpp)". The Qwen 2.5-VL model will generate a response about the image.
You can also access the Qwen model’s API via http://localhost:8080/completion if needed (this is what the app uses under the hood).

### 5. Customizations and Notes
LLaVA vs Qwen in OmniParser: By default, OmniParser uses a smaller vision-language model (LLaVA) internally for understanding iconography (vlm_model='llava'). We pair it with the more powerful Qwen model for chat. In future, it’s possible to switch OmniParser to use Qwen for both parsing and chat if integrated differently, but that would require more extensive changes.
System Prompts: The prompt format used is already aligned with Qwen-VL’s expected input (including the <image> token). If needed, you could add a system prompt by modifying the payload with a <|im_start|>system\n...<|im_end|> segment.
Model Quantization: Running Qwen 32B requires significant RAM/VRAM. If you run on CPU or have limited memory, consider using a quantized GGUF model (e.g., Q4_K_M or Q8_0). Just ensure the file name in the Docker CMD matches the file you use.
OCR Dependency: If you find text is not being extracted from the image, double-check that paddleocr is installed in the container. We left it optional to keep the image lighter. Install it via pip or add to requirements.txt if needed, then rebuild.
Future Improvements: You can integrate everything into a single multi-modal model (like using a unified LLaVA or another vision-chat model for both layout parsing and Q&A). Also, you might consider adding a system prompt or persona for Qwen to better guide its answers (this could be done by editing the prompt string in app.py).

### Contributing
Feel free to modify this project or use it as a template. If you make improvements (like a better UI or integration with other models), consider creating a template repository or sharing your version for others to learn from. Happy coding! 🎉
