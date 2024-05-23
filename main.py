from flask import Flask, request, jsonify
import torch
from diffusers import AutoPipelineForText2Image, AutoPipelineForImage2Image
import base64
from io import BytesIO
from flask_cors import CORS
from PIL import Image

use_xl = False

if use_xl:
    fast_model_id, slow_model_id = "stabilityai/sdxl-turbo", "stabilityai/stable-diffusion-xl-refiner-1.0" # "stabilityai/stable-diffusion-xl-base-1.0"
else:
    fast_model_id, slow_model_id = "stabilityai/sd-turbo", "stabilityai/stable-diffusion-xl-refiner-1.0" # "stabilityai/stable-diffusion-2-1"

siz = 512
fast_pipe = AutoPipelineForText2Image.from_pretrained(
    fast_model_id,
    torch_dtype=torch.float16,
    variant="fp16",
).to("cuda")
fast_pipe.enable_xformers_memory_efficient_attention()
print(f"{fast_model_id} loaded")

slow_pipe = AutoPipelineForImage2Image.from_pretrained(
    slow_model_id,
    variant="fp16",
    torch_dtype=torch.float16,
).to("cuda")
slow_pipe.enable_xformers_memory_efficient_attention()
print(f"{slow_model_id} loaded")

fast_guidance_scale = 0.0
fast_num_inference_steps = 1

slow_guidance_scale = 7.5
slow_num_inference_steps = 50

app = Flask(__name__)
CORS(app)

@app.route("/api/generate-image", methods=["POST"])
def generate_image():
    kwargs = {"width": siz, "height": siz}

    fast = request.json.get("fast", True)
    if fast:
        pipe = fast_pipe
        kwargs["guidance_scale"] = fast_guidance_scale
        kwargs["num_inference_steps"] = fast_num_inference_steps
    else:
        pipe = slow_pipe
        kwargs["guidance_scale"] = slow_guidance_scale
        kwargs["num_inference_steps"] = slow_num_inference_steps

    seed = request.json.get("seed", None)
    if seed is None:
        seed = torch.randint(0, 2**32 - 1, (1,)).item()
    generator = torch.Generator(device=pipe.device).manual_seed(seed)

    src_image = request.json.get("image", None)
    if not fast and not src_image:
        return jsonify({"error": "A source image is required for HQ mode"}), 400
    
    if src_image:
        src_image_data = base64.b64decode(src_image[len("data:image/jpeg;base64,"):])
        src_pil_image = Image.open(BytesIO(src_image_data))
        kwargs["image"] = src_pil_image
        kwargs["strength"] = 0.5
        del kwargs["guidance_scale"]
        del kwargs["num_inference_steps"]

    prompt = request.json.get("prompt", None)
    if not prompt:
        return jsonify({"error": "A prompt is required"}), 400
    
    image = pipe(prompt, generator=generator, **kwargs).images[0]
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    base64_image = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return jsonify({
        "base64_image": base64_image,
        "prompt": prompt,
        "seed": seed,
    })
    
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"