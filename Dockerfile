FROM nvidia/cuda:12.2.0-cudnn8-runtime-ubuntu22.04

# Base system setup
RUN apt-get update && apt-get install -y \
    git wget curl python3 python3-pip build-essential \
    libgl1 libglib2.0-0 libjpeg-dev ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY requirements.txt /tmp/
RUN pip3 install --upgrade pip && pip3 install -r /tmp/requirements.txt

# Build llama.cpp with server support
RUN git clone --depth=1 https://github.com/ggerganov/llama.cpp /app/llama.cpp && \
    cd /app/llama.cpp && make LLAMA_CUBLAS=1 LLAMA_SERVER=1

# Copy application code
WORKDIR /app
COPY app.py .

# Create models directory (you will mount or add the model file here later)
RUN mkdir -p /app/models

# Expose ports for Gradio (7861) and llama.cpp server (8080)
EXPOSE 7861 8080

# Entrypoint: start llama.cpp HTTP server and Gradio app
CMD bash -c "cd /app/llama.cpp && \
    ./server -m /app/models/qwen2.5-vl-32b.QwenMM.gguf --host 0.0.0.0 & \
    python3 /app/app.py"
