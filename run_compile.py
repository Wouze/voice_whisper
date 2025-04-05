import torch
from torch.nn.attention import SDPBackend, sdpa_kernel
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from tqdm import tqdm
import time  # Import the time module

torch.set_float32_matmul_precision("high")

device = "mps"  # or "cuda" for NVIDIA GPUs
torch_dtype = torch.float16 

model_id = "openai/whisper-large-v3"

model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True
).to(device)

# Enable static cache and compile the forward pass
model.generation_config.cache_implementation = "static"
model.generation_config.max_new_tokens = 256
model.forward = torch.compile(model.forward, mode="reduce-overhead", fullgraph=True)

processor = AutoProcessor.from_pretrained(model_id)

pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    torch_dtype=torch_dtype,
    device=device,
)

sample = 'videoplayback.mp3'

# Warm-up steps with timing
start_time = time.time()
for _ in tqdm(range(2), desc="Warm-up step"):
    with sdpa_kernel(SDPBackend.MATH):
        result = pipe(sample,return_timestamps=True)
warmup_time = time.time() - start_time
print(f"Warm-up time: {warmup_time:.2f} seconds")

# Fast run with timing
start_time = time.time()
with sdpa_kernel(SDPBackend.MATH):
    result = pipe(sample.copy())
fast_run_time = time.time() - start_time
print(f"Fast run time: {fast_run_time:.2f} seconds")

print(result)
