
# OmniParser-VL-App 🚀

This repository contains a Dockerized Gradio application that combines **Microsoft OmniParser v2** (for GUI screenshot parsing) with **Qwen 2.5-VL-32B** (a vision-language model) via `llama.cpp`. The app can analyze a screenshot of a user interface, list its GUI elements, and answer questions about the UI.

---

## 🧠 Features

- ✅ **OmniParser v2** for detecting GUI elements (buttons, icons, text fields) and their labels from screenshots.
- ✅ **Qwen 2.5-VL-32B** via `llama.cpp` for local image-based question answering.
- ✅ **Gradio UI** to upload an image, parse elements, and chat with the vision model.

---

## 📁 Project Structure

```
omniparser-vl-app/
├── Dockerfile              # Docker setup (GPU-enabled)
├── app.py                  # Gradio application logic
├── requirements.txt        # Python dependencies
└── models/
    └── qwen2.5-vl-32b.QwenMM.gguf   # (Not included - download separately)
```

> ⚠️ **Note:** The `qwen2.5-vl-32b.QwenMM.gguf` model is not included due to size. You'll need to download it yourself (see below).

---

## 🚀 Getting Started

### 1. Download the Qwen2.5-VL Model

Download the Qwen 2.5-VL 32B GGUF model and place it in the `models/` folder:

```bash
mkdir -p models
wget -O models/qwen2.5-vl-32b.QwenMM.gguf \
  https://huggingface.co/Qwen/Qwen-VL-Chat-GGUF/resolve/main/qwen2.5-vl-32b.QwenMM.gguf
```

Make sure the file path matches the one in the Dockerfile command:
```
/app/models/qwen2.5-vl-32b.QwenMM.gguf
```

---

### 2. Build the Docker Image

Run the following in the project root:

```bash
docker build -t omniparser-vl-app .
```

This builds a container that includes:

- OmniParser v2 and its ML dependencies
- Gradio frontend
- llama.cpp built with GPU + HTTP server support

> 💡 The base image uses CUDA. You’ll need an NVIDIA GPU + drivers for full functionality.

---

### 3. Run the Container

```bash
docker run --gpus all -p 7861:7861 -p 8080:8080 \
  -v $(pwd)/models:/app/models \
  omniparser-vl-app
```

**Flags explained:**
- `--gpus all`: Enables GPU usage
- `-p 7861:7861`: Exposes Gradio app on `localhost:7861`
- `-p 8080:8080`: Exposes llama.cpp API at `localhost:8080/completion`
- `-v $(pwd)/models:/app/models`: Mounts the model directory into the container

---

## 🖼 Using the App

1. Visit [http://localhost:7861](http://localhost:7861)
2. Upload a screenshot (e.g., a GUI or webpage)
3. Click **“Run OmniParser”** to analyze the image
4. Enter a question and click **“Ask Qwen (llama.cpp)”** to get a response

You can also access the Qwen model API directly at:

```
http://localhost:8080/completion
```

---

## ⚙️ Notes & Customization

- **LLaVA vs Qwen:** OmniParser uses `llava` internally for element parsing, while Qwen handles VQA.
- **System Prompts:** You can add a system prompt by prepending a `<|im_start|>system\n...<|im_end|>` block to your prompt.
- **Model Quantization:** Consider Q4_K_M or Q8_0 variants for lower VRAM usage if needed.
- **OCR Dependency:** If text isn't extracted, make sure `paddleocr` is installed (or add it to `requirements.txt`).
- **Lighter CPU Builds:** You may remove CUDA from the base image if GPU isn’t needed (e.g., for low-load CPU testing).

---

## 💡 Future Improvements

- ✅ Replace LLaVA in OmniParser with Qwen for unified reasoning
- ✅ Add prompt tuning or system persona
- ✅ Integrate model fallback or streaming mode
- ✅ Deploy to Hugging Face Spaces or GPU cloud

---

## 🤝 Contributing

Feel free to fork, remix, or use this as a GitHub Template. PRs welcome!

---

## 📄 License

Apache-2.0 (https://github.com/DuskoPre/omniparser-vl-app#)

---

Happy parsing! 🎉
