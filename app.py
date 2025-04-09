# Required Libraries
from moviepy import VideoFileClip
# import subprocess
import assemblyai as aai
import numpy as np
import streamlit as st
import tempfile
import os

# Function: Convert Video to Audio
def convert_video_to_audio(video_path, audio_path):
    # try:
    #     command = f"ffmpeg -y -i \"{video_path}\" -vn -acodec pcm_s16le -ar 44100 -ac 2 \"{audio_path}\""
    #     subprocess.run(command, shell=True, check=True)
    #     print(f"Successfully converted {video_path} to {audio_path}")
    # except Exception as e:
    #     print(f"Error: {e}")
        
    try:
        video_clip = VideoFileClip(video_path)
        audio_clip = video_clip.audio
        audio_clip.write_audiofile(audio_path)
        video_clip.close()
        audio_clip.close()
        print(f"Successfully converted {video_path} to {audio_path}")
    except Exception as e:
        print(f"Error: {e}")

# Function: Create Subtitle Using AssemblyAI
def create_subtitle(audio_path):
    aai.settings.api_key = "c1bd6fe182be49eb88b52174e4cb3390"

    # Transcribe the audio
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_path)

    # Parameters
    words_per_subtitle = 10
    subtitles = []

    # Temporary storage
    current_subtitle = []
    current_start = None
    last_end = None

    for word_info in transcript.words:
        word = word_info.text
        start = word_info.start / 1000  # Convert to seconds
        end = word_info.end / 1000

        if current_start is None:
            current_start = start

        current_subtitle.append(word)
        last_end = end

        if len(current_subtitle) >= words_per_subtitle:
            subtitle_text = ' '.join(current_subtitle)
            subtitles.append({'start': current_start, 'end': end, 'text': subtitle_text})
            current_subtitle = []
            current_start = None

    # Add remaining words
    if current_subtitle:
        subtitle_text = ' '.join(current_subtitle)
        subtitles.append({'start': current_start, 'end': last_end, 'text': subtitle_text})

    return subtitles

# Function: Convert to SRT Format
def convert_to_srt(subtitle_data, srt_file_path):
    try:
        with open(srt_file_path, 'w', encoding='utf-8') as srt_file:
            for i, subtitle in enumerate(subtitle_data):
                start_time = format_time(subtitle['start'])
                end_time = format_time(subtitle['end'])
                text = subtitle['text'].strip()  # Remove leading/trailing spaces

                srt_file.write(f"{i + 1}\n")
                srt_file.write(f"{start_time} --> {end_time}\n")
                srt_file.write(f"{text}\n\n")

        print(f"SRT file created successfully: {srt_file_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Helper: Format Time in SRT Format
def format_time(seconds):
    milliseconds = int(seconds * 1000)
    hours = milliseconds // (3600 * 1000)
    milliseconds %= (3600 * 1000)
    minutes = milliseconds // (60 * 1000)
    milliseconds %= (60 * 1000)
    seconds = milliseconds // 1000
    milliseconds %= 1000
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

# ==============================
# Streamlit App Starts Here
# ==============================
st.set_page_config(page_title="Subtitle Generator", layout="centered")
st.title("🎬 Video Subtitle Generator with SRT Download")

# Upload Video
uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "avi", "mov", "mkv"])

if uploaded_file is not None:
    # Save uploaded video to a temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_video_file:
        tmp_video_file.write(uploaded_file.read())
        video_path = tmp_video_file.name

    # Paths
    audio_path = os.path.splitext(video_path)[0] + ".wav"
    srt_file_path = os.path.splitext(video_path)[0] + ".srt"

    # Step 1: Convert Video to Audio
    with st.spinner("🎧 Extracting audio from video..."):
        convert_video_to_audio(video_path, audio_path)

    # Step 2: Generate Subtitles
    with st.spinner("🧠 Transcribing and generating subtitles..."):
        subtitles = create_subtitle(audio_path)

    # Step 3: Convert to SRT
    with st.spinner("📄 Creating SRT file..."):
        convert_to_srt(subtitles, srt_file_path)

    st.success("✅ Subtitle generation completed!")

    # Video Player
    st.subheader("🎞️ Uploaded Video")
    st.video(video_path)

    # Download SRT
    with open(srt_file_path, "rb") as srt_file:
        st.download_button("📥 Download SRT File", srt_file, file_name="subtitles.srt", mime="text/plain")

    # Show Generated Subtitles
    st.subheader("📝 Generated Text")
    text = []
    for subtitle in subtitles:
        text.append(subtitle['text'])
    st.write(' '.join(text))

    