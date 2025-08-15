# openai-SenseVoice

The overall framework remains consistent with [FastWhisperAPI](https://github.com/3choff/FastWhisperAPI/blob/main/README.md), using SenseVoice to convert audio to text.
## Requirements
- Python 3.10
- Refer to the SenseVoice documentation for the GPU requirements [here](https://github.com/FunAudioLLM/SenseVoice/blob/main/README.md).

1. Clone the repository:
    ```bash
    git clone https://github.com/735726032/openai-SenseVoice.git
    ```

2. Navigate to the project directory:
    ```bash
    cd openai-SenseVoice
    ```

3. Create a new environment, use Miniconda3(after installing miniconda3 environment):
    ```bash
    conda create -n openai-SenseVoice python=3.10 -y
   
    conda activate openai-SenseVoice
    ```

4. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

5. Preload the base model (Download it from huggingface by default, and can be switched by modifying the 'hub' configuration in the code.).By default, the model directories downloaded using modelscope are in `~/.cache/modelscope/hub/models`
    ```bash
    python download_model.py
    ```

6. Modify .env
    ```bash
   PORT=8000
   API_KEY=dummy_api_key
   
   # When the option is 'True', the model is not recreated based on the entry parameter, and the last created model is reused. Default is 'False'.
   FORCE_CACHE_INVOKE=True
    ```

## Usage

To run the FastAPI app, use the following command:

```bash
fastapi run main.py
```

If you want to specify a different port, use the --port option followed by the desired port number:

```bash
fastapi run main.py --port 8000
```

The API automatically detects the availability of a GPU and configures the device accordingly, either on CPU or CUDA.

The application will begin running at `http://localhost:8000` if the port was not specified, or at `http://localhost:PORT` if a different port was specified.

To authenticate API requests, set the API key to "dummy_api_key" in your environment (Default).

## Alternative Setup and Run Methods

### Docker

This API can be dockerized for deployment, and a Dockerfile is included in the repository. Please note that you may need to edit the Dockerfile based on your specific setup and CUDA version installed.

Use the following commands to build and run the container:

***Build a Docker container:***
   ```shell
      docker build -t openai-SenseVoice .
   ```
***Run the container***
   ```shell
      docker run -p 8000:8000 openai-SenseVoice
   ```

## Parameters

- `file`: A list of audio files to transcribe. This is a required parameter.
- `model`: The size of the model to use for transcription. This is an optional parameter. The options are 'iic/SenseVoiceSmall'. Default is 'iic/SenseVoiceSmall'.You can write directly to the file path, and the automatic download model operation will not be triggered. e.g. `/root/.cache/modelscope/hub/models/iic/SenseVoiceSmall/`
- `vad_model`: This is an optional parameter. The options are 'fsmn-vad'. Default is 'fsmn-vad'.You can write directly to the file path, and the automatic download model operation will not be triggered.`/root/.cache/modelscope/hub/models/iic/speech_fsmn_vad_zh-cn-16k-common-pytorch/`
- `language`: This parameter specifies the language of the audio files. It is optional, with accepted values being lowercase ISO-639-1 format (e.g., 'en' for English). If not provided, the system will automatically detect the language. The options are 'auto, 'zh, 'en', 'yue', 'ja', 'ko, 'nospeech. Default is 'auto'.
- `response_format`: The format of the response. This is an optional parameter. The options are 'text', 'verbose_json'. Default is 'text'.

### Example curl request

You can use the following `curl` command to send a POST request to the `/v1/audio/transcriptions` endpoint:

```bash
curl -X POST "http://localhost:8000/v1/audio/transcriptions" \
-H  "accept: application/json" \
-H  "Content-Type: multipart/form-data" \
-H  "Authorization: Bearer dummy_api_key" \
-F "file=@audio1.wav;type=audio/wav" \
-F "file=@audio2.wav;type=audio/wav" \
-F "model=iic/SenseVoiceSmall" \
-F "vad_model=fsmn-vad" \
-F "language=auto" \
-F "response_format=text" 
```
## Endpoints

- `/`: Redirects to the `/docs` endpoint, which provides a Swagger UI for interactive exploration of the API. You can call and test the API directly from your browser.
- `/info`: Provides information about the device used for transcription and the parameters.
- `/v1/audio/transcriptions`: API designed to transcribe audio files.

## Acknowledgements

This project was made possible thanks to:

- [SenseVoice](https://github.com/FunAudioLLM/SenseVoice): For providing the transcription model used in this project.
- [FastAPI](https://github.com/tiangolo/fastapi): For the web framework used to build the API.
- [AI Anytime](https://www.youtube.com/watch?v=NU406wZz1eU): For inspiring this project.

## License

This project is licensed under the Apache License 2.0.
