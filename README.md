# Purpose
Observing Syonanto is an Open Source Intelligence (OSINT) platform built to provide real-time situational awareness within Singapore.

The platform consists of two parts:
1. Main: The primary application providing real-time aggregated feeds.
2. Tools: A collection of additional utilities to support OSINT operations:

# Tools: 
## Mental_Moron
A tool that allows users to transcribe audio into text using OpenAI's Whisper model.
## TeleRipper:
A tool that allows users to download all videos shared within a Telegram channel.
## Operation 143:
A tool that allow the automation of  recording of TikTok Live videos from a specific content creator.


# Instructions
## Prerequisites:
This Platform and it's tools were developed and tested on a Linux based environment which allows a minimum python version of Python 3.10 to be ran.
- OS: Linux Based OS
- Python: Python 3.10 and above
- Internet: An Active internet connection
- Memory: 16GB
- Storage: 50GB
- GPU: Nvidia RTX 2060 
- CUDA: 12.2
## Setup
### 1. Main
### 2. Tools
## Mental_Moron

📂 Directory Purpose
- raw_audio
This folder contains the original, unprocessed audio files (e.g., .mp3, .wav). 
Files placed here are not yet converted or split for transcription.
- preprocessed_audio
Contains audio files converted to 16kHz mono .wav format, ready for transcription by Whisper.
- transcripts
Stores the generated transcripts as .txt files.
- scripts
Custom scripts related to audio preprocessing, transcription, or automation.
- whisper-env
Python virtual environment containing dependencies, including Whisper and any other required libraries.
##### Usage:
1. Place Raw audio file in raw_audio/
2. Navigate to scripts/
3. Run `process_audio.sh`
4. Once audio clip has been processed, run `python3 TransribeAudio.py`
#### TeleRipper

##### Usage: 
1. List channels available from telegram account, to list the channels, run 
   `python3 listChannels.py`
2. From the listed Channels, to download all videos, run
   ``download_videos.py``
