import time
import torch
from transformers import pipeline
from transformers.utils import is_flash_attn_2_available

# Start timing
start_time = time.time()

pipe = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-large-v3",  # select checkpoint from https://huggingface.co/openai/whisper-large-v3#model-details
    torch_dtype=torch.float16,
    device="mps",  # or mps for Mac devices
    # model_kwargs={"attn_implementation": "flash_attention_2"} if is_flash_attn_2_available() else {"attn_implementation": "sdpa"},
)

outputs = pipe(
    "videoplayback.mp3",
    chunk_length_s=30,
    batch_size=36,
    return_timestamps=True,
)

# End timing
end_time = time.time()

print(outputs)
print(f"Execution time: {end_time - start_time:.2f} seconds")
