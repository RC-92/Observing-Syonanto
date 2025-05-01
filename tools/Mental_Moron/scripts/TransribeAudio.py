from faster_whisper import WhisperModel
import os

# Adjusted paths (relative to script location)
input_dir = "/home/$user/Operation-MentalMoron/preprocessed_audio"
output_dir = "/home/$user/Operation-MentalMoron/transcripts"

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Load model with GPU support
model_size = "medium"  # Options: tiny, base, small, medium, large
model = WhisperModel(model_size, device="cuda", compute_type="float16")

# Iterate through all .wav files in the input folder
for filename in os.listdir(input_dir):
    if filename.endswith(".wav"):
        audio_path = os.path.join(input_dir, filename)
        transcript_path = os.path.join(output_dir, f"{filename}.txt")

        segments, info = model.transcribe(audio_path, beam_size=5, language="en")

        with open(transcript_path, "w") as f:
            for segment in segments:
                f.write(f"[{segment.start:.2f}s - {segment.end:.2f}s] {segment.text}\n")

        print(f"Transcribed: {filename}")

