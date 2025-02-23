# Avaltar Entry Task  

## Description  
The goal of this project was to create a continuous video stream from a given `.mp4` video. The video stream should detect people using the YOLOv8 model and be presented in a simple web app.  

For this purpose, a Python Flask app was created. The app implements two video streaming formats:  
- **MJPEG (Motion JPEG)** – The client receives the stream as a sequence of JPEG images.  
- **HLS (HTTP Live Streaming)** – A more standard streaming format.  

The MJPEG stream is generated on the backend of the Flask app. To subscribe to it, the user only needs to visit the `/m-jpeg-stream` endpoint. The HLS stream, on the other hand, is created via a separate script, `services.stream.py`, which generates the necessary files that are then streamed to the client via an API.  

## Installation  

It is recommended to create a virtual environment with the required Python packages:  

```sh
python -m venv ./my-venv  # Create a virtual environment in the current folder
source ./my-venv/bin/activate  # Activate it (Linux/macOS)
```

after creating virtual enviroment use the following command to install dependencies:

```
python -m pip install -r requirements.txt
```

### Hosting the app locally

To run the server, use the following command:

```
python app.py
```

To produce the HLS stream, run the following command in a separate terminal:

```
python -m services.stream
```

### Running the web app
By default, the app runs on port 5000. Open a web browser and visit http://127.0.0.1:5000