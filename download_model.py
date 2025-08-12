from funasr import AutoModel

# Preload the base model
model = AutoModel(
    model="iic/SenseVoiceSmall",
    trust_remote_code=True,
    remote_code="./model.py",
    vad_model="fsmn-vad",
    vad_kwargs={"max_single_segment_time": 30000},
    device="cuda:0", # e.g. cpu, cuda, cuda:0
    hub="huggingface" # e.g. huggingface, modelscope
)