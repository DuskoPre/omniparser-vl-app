A few points about app.py:
It uses OmniParser v2 to parse the uploaded GUI screenshot. The parser(image) call returns a dictionary with parsed results. We retrieve the result['image'] (which is an image annotated with bounding boxes around UI elements) and result['content'] (list of elements and any text).
run_omnivision prepares a newline-separated list of parsed elements (with their type and detected text if any) for display.
ask_qwen_llamacpp takes the image and a user question, converts the image to base64, and sends it to the Qwen model via the llama.cpp HTTP server. The prompt format "<|im_start|>user\n<image>\n{prompt}<|im_end|>\n<|im_start|>assistant\n" is specific to Qwen-VL’s expected conversational format (with special tokens indicating an image is included).
We then build a simple Gradio UI: an image uploader and buttons on the left, and outputs on the right. The user can:
Run OmniParser on the image to see the parsed GUI elements (and an annotated image).
Ask Qwen a question about the image for a more descriptive answer or analysis from the vision-language model.
Finally, demo.launch(..., server_name="0.0.0.0", server_port=7861) starts the app listening on all interfaces at port 7861 (so it works in Docker and can be accessed via localhost).
