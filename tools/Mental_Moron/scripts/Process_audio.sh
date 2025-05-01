#!/bin/bash

# Default values
DURATION=300  # Max 5 minutes (300 seconds)
INPUT_DIR="raw_audio"
AUDIO_CHANNEL=1
AUDIO_RATE=16000
OUTPUT_FORMAT="wav"
BASENAME=""

# Help message function
usage() {
  echo ""
  echo "🧠 Operation Mental Moron - Audio Preprocessing Script"
  echo ""
  echo "Usage: $0 [options]"
  echo ""
  echo "Options:"
  echo "  -d <duration>        Duration in seconds (max 300). Default: 300"
  echo "  -i <input_path>      Path to input audio file or directory. Default: raw_audio/"
  echo "  -ac <channels>       Audio channels: 1 for mono, 2 for stereo. Default: 1"
  echo "  -ar <sample_rate>    Audio sample rate in Hz. Default: 16000"
  echo "  -o <format>          Output format: wav or mp3. Default: wav"
  echo "  -b <basename>        Optional basename for output file(s)."
  echo "  -h                   Show this help message and exit"
  echo ""
  echo "Example:"
  echo "  $0 -d 120 -i raw_audio/ -ac 1 -ar 22050 -o mp3 -b clip"
  echo ""
  exit 0
}

# Parse flags
while getopts ":d:i:ac:ar:o:b:h" opt; do
  case ${opt} in
    d)
      if (( OPTARG > 300 )); then
        echo "Error: Duration cannot exceed 300 seconds (5 minutes)."
        exit 1
      fi
      DURATION=$OPTARG
      ;;
    i)
      INPUT_DIR=$OPTARG
      ;;
    ac)
      if [[ "$OPTARG" != "1" && "$OPTARG" != "2" ]]; then
        echo "Error: -ac must be 1 (mono) or 2 (stereo)."
        exit 1
      fi
      AUDIO_CHANNEL=$OPTARG
      ;;
    ar)
      AUDIO_RATE=$OPTARG
      ;;
    o)
      if [[ "$OPTARG" != "wav" && "$OPTARG" != "mp3" ]]; then
        echo "Error: -o must be 'wav' or 'mp3'."
        exit 1
      fi
      OUTPUT_FORMAT=$OPTARG
      ;;
    b)
      BASENAME=$OPTARG
      ;;
    h)
      usage
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      usage
      ;;
  esac
done

# Ensure input exists
if [[ ! -e "$INPUT_DIR" ]]; then
  echo "Error: Input file or directory '$INPUT_DIR' does not exist."
  exit 1
fi

# Create output directory if not exists
mkdir -p preprocessed_audio

# Function to process a single audio file
process_file() {
  local input_file=$1
  local filename=$(basename "$input_file")
  local name="${filename%.*}"

  if [[ -n "$BASENAME" ]]; then
    name="$BASENAME"
  fi

  local output_path="preprocessed_audio/${name}.${OUTPUT_FORMAT}"

  ffmpeg -y -t "$DURATION" -i "$input_file" -ac "$AUDIO_CHANNEL" -ar "$AUDIO_RATE" "$output_path"
  echo "✅ Processed: $output_path"
}

# Process either a single file or a directory
if [[ -f "$INPUT_DIR" ]]; then
  process_file "$INPUT_DIR"
else
  for file in "$INPUT_DIR"/*; do
    [[ -f "$file" ]] && process_file "$file"
  done
fi

