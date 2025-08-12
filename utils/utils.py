import os
import tempfile
from fastapi import Depends, HTTPException, status, UploadFile
from fastapi.security import HTTPAuthorizationCredentials

from funasr import AutoModel
from funasr.utils.postprocess_utils import rich_transcription_postprocess

from constants import security, SUPPORTED_EXTENSIONS, SUPPORTED_LANGUAGES, SUPPORTED_MODELS, SUPPORTED_RESPONSE_FORMATS
from logging_config import get_logger

logger = get_logger()


def authenticate_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    correct_api_key = os.getenv("API_KEY", "dummy_api_key")  # replace with your dummy API key
    if credentials.scheme != "Bearer" or credentials.credentials != correct_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": {
                    "message": "Incorrect API key",
                    "type": "invalid_request_error",
                    "param": "Authorization",
                    "code": 401
                }
            },
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials


def get_file_extension(filename: str) -> str:
    _, extension = os.path.splitext(filename)
    return extension[1:].lower()


async def transcribe_temp_file(file: UploadFile, extension: str, model: AutoModel, language: str):
    temp_file = tempfile.NamedTemporaryFile(suffix=extension, delete=False)
    try:
        temp_file.write(await file.read())
        temp_file.close()
        res = model.generate(temp_file.name, language=language, use_itn=True, batch_size_s=60, merge_vad=True,
                             merge_length_s=15)
        text = rich_transcription_postprocess(res[0]["text"])
    finally:
        os.unlink(temp_file.name)
    return text


def create_segment_data(segments: list, word_timestamps: bool):
    segment_data = []
    for segment in segments:
        segment_dict = {
            "text": segment.text.strip(),
            "start": segment.start,
            "end": segment.end,
        }
        if word_timestamps:
            words_data = []
            for word in segment.words:
                words_data.append({
                    "word": word.word.strip(),
                    "start": word.start,
                    "end": word.end
                })
            segment_dict["words"] = words_data
        segment_data.append(segment_dict)
    return segment_data


async def process_file(file: UploadFile, model: AutoModel, language: str):
    extension = get_file_extension(file.filename)
    full_text = await transcribe_temp_file(file, extension, model, language)
    return {
        "filename": file.filename,
        # "detected_language": info.language,
        # "language_probability": info.language_probability,
        "text": full_text
    }


def validate_parameters(files, language, model_size, response_format):
    for file in files:
        extension = get_file_extension(file.filename)
        if extension not in SUPPORTED_EXTENSIONS:
            logger.warning(f"Invalid file extension: {extension}")
            raise HTTPException(status_code=400, detail={
                "error": {
                    "message": f"Invalid file extension. Supported extensions are: {', '.join(SUPPORTED_EXTENSIONS)}",
                    "type": "invalid_request_error",
                    "param": "files",
                    "code": 400
                }
            })
    if language is not None and language not in SUPPORTED_LANGUAGES:
        logger.warning(f"Invalid language: {language}")
        raise HTTPException(status_code=400, detail={
            "error": {
                "message": f"Invalid language {language}. Language parameter must be specified in ISO-639-1 format.",
                "type": "invalid_request_error",
                "param": "language",
                "code": 400
            }
        })
    if model_size not in SUPPORTED_MODELS:
        logger.warning(f"Invalid model size: {model_size}")
        raise HTTPException(status_code=400, detail={
            "error": {
                "message": f"Invalid model size. Supported models are: {', '.join(SUPPORTED_MODELS)}",
                "type": "invalid_request_error",
                "param": "model",
                "code": 400
            }
        })
    if response_format not in SUPPORTED_RESPONSE_FORMATS:
        logger.warning(f"Invalid response_format value: {response_format}")
        raise HTTPException(status_code=400, detail={
            "error": {
                "message": f"Invalid response_format. Supported format are: {', '.join(SUPPORTED_RESPONSE_FORMATS)}",
                "type": "invalid_request_error",
                "param": "response_format",
                "code": 400
            }
        })
