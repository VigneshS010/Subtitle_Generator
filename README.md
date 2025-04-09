

# Video Subtitle Generator 🎬

The Video Subtitle Generator is a Python application that allows users to upload a video file and generate an SRT file containing subtitles for the given video. The application makes use of the MoviePy library for extracting audio from video files and the AssemblyAI service to transcribe the audio into text and generate subtitles.

## Features

- Upload a video file (MP4, AVI, MOV, MKV).
- Extract audio from the video file.
- Transcribe the audio into text using AssemblyAI.
- Generate subtitles based on the transcription and organize them into an SRT file.
- Download the generated SRT file.
- Display the generated text subtitles in the app.

## Installation

To get started, you need to install the required libraries. You can do so by using the following command:

```bash
pip install moviepy assemblyai streamlit
```

Make sure that you have `ffmpeg` installed on your system as well (which is typically a requirement for MoviePy). If you need instructions on how to install `ffmpeg`, refer to the [official FFmpeg website](https://www.ffmpeg.org/download.html).

## Usage

To run the Streamlit application, first save the provided script into a file named `app.py` and execute the following command:

```bash
streamlit run app.py
```

This will start a local server where you can interact with the application through your web browser.

### Step-by-Step Usage

1. Open the web interface and you will see an option to upload a video file.
2. Click on the "Upload a video file" button and choose a video file (supported formats include MP4, AVI, MOV, MKV).
3. Once the video file is uploaded, the application will:
    
    - Extract the audio from the video and save it as a `.wav` file.
    - Transcribe the audio using AssemblyAI.
    - Generate a set of subtitles from the transcription which are grouped by a specified number of words (default is 10 words per subtitle).
    - Save the generated subtitles in an SRT file format.
4. Once the subtitle generation is completed, a success message will be displayed.
5. An embedded video player will show the uploaded video.
6. A "Download SRT File" button will appear which, when clicked, will download the generated SRT file (named `subtitles.srt`).

## Contributing

Contributions to the Video Subtitle Generator are very welcome! Here’s how you can help:

1. Fork the repository to your own GitHub account.
2. Clone the repository to your local machine.
3. Make your changes and commit them to a new branch.
4. Push your changes to the branch on your fork.
5. Open a pull request to the main repository.

Please make sure that your code adheres to the project's coding standards and that you have written or updated any necessary documentation.

## License

The license information for this project was not explicitly mentioned in the provided script. If you plan to make this repository public, you should include a license file (e.g., `LICENSE.md`) which specifies the terms under which others can use, copy, and contribute to your project. Common options include MIT, Apache 2.0, and GPL licenses. 

## Important Notes

This script uses a hardcoded AssemblyAI API key for the transcription step. For security reasons, it is recommended not to share or make public API keys. A better practice is to use environment variables to keep such sensitive data secure. For example:

```python
import os
aai.settings.api_key = os.environ.get("ASSEMBLYAI_API_KEY")
```

Thus, before running the `streamlit run app.py` command, set an environment variable named `ASSEMBLYAI_API_KEY` with your actual AssemblyAI API key.

By following these steps, you should be able to use the Video Subtitle Generator efficiently and contribute to its future development and enhancements.
```}
