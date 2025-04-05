import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
import time

device = "mps" 
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

model_id = "openai/whisper-large-v3"

start_time = time.time()

model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
)
model.to(device)

processor = AutoProcessor.from_pretrained(model_id)

pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    torch_dtype=torch_dtype,
    device=device,
)

load_time = time.time()
print(f"Model and pipeline loaded in {load_time - start_time:.2f} seconds.")

sample = "videoplayback.mp3"

inference_start = time.time()
result = pipe(sample, return_timestamps=True, generate_kwargs={"language": "arabic"})
inference_end = time.time()

print(result)
print(f"Inference completed in {inference_end - inference_start:.2f} seconds.")
