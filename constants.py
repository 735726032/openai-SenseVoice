import os

try:
    import torch
except ImportError:
    torch = None
from funasr import AutoModel
from fastapi.security import HTTPBearer

# Determine device based on availability
if torch is not None:
    device = "cpu" if os.getenv("FORCE_CPU", "false").lower() == "true" else (
        "cuda" if torch.cuda.is_available() else "cpu")
else:
    device = "cpu"

security = HTTPBearer()
MAX_THREADS = 6

SUPPORTED_LANGUAGES = (
    "auto", "zh", "en", "yue", "ja", "ko", "nospeech"
)
SUPPORTED_MODELS = ("iic/SenseVoiceSmall",)

SUPPORTED_EXTENSIONS = ("mp3", "mp4", "mpeg", "mpga", "m4a", "wav", "webm", "opus", "flac", "ogg")

SUPPORTED_RESPONSE_FORMATS = ("text", "verbose_json")

SUPPORTED_TIMESTAMP_GRANULARITIES = ("segment", "word")
