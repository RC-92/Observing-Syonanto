#!/usr/bin/env python3
import json
import os
import time
import subprocess

from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions

def main():
    # Read configs
    with open('url.json', 'r') as f:
        url = json.load(f)['url']

    with open('cookie.json', 'r') as f:
        cookies = json.load(f)

    with open('duration.json', 'r') as f:
        duration = int(json.load(f)['duration'])

    # Get the X display set by x11docker
    display = os.getenv("DISPLAY", ":0")  # fallback if somehow not set

    # Setup Selenium for Firefox
    firefox_opts = FirefoxOptions()
    # Remove comment to run invisibly in headless mode if you prefer:
    # firefox_opts.add_argument("--headless")

    driver = webdriver.Firefox(options=firefox_opts)

    # 1) Visit the top-level domain so we can set the cookies
    #    If domain is ".tiktok.com", let's just open the main site
    driver.get("https://www.tiktok.com/")
    time.sleep(3)  # wait for initial page to load

    # 2) Insert the cookies
    for c in cookies:
        driver.add_cookie(c)

    # 3) Now navigate to the actual Live URL
    driver.get(url)
    time.sleep(2)

    # 4) Launch ffmpeg to record the container’s X display + PulseAudio
    #    We assume x11docker has set up PulseAudio inside the container, too.
    #    If you prefer to record from the host, skip this step in the container
    #    and do it on the host with your own ffmpeg or OBS.

    # Construct the ffmpeg command. We’ll capture from the container’s
    # display (e.g. :100) and from PulseAudio’s default device for sound.
    output_file = "recorded_tiktok.mkv"
    cmd = [
        "ffmpeg",
        "-y",  # overwrite existing file
        "-f", "x11grab",
        "-i", display,      # capture the container’s display
        "-f", "pulse",
        "-i", "default",    # capture container’s PulseAudio default
        "-t", str(duration),
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "23",
        "-c:a", "aac",
        output_file
    ]
    print("Starting recording with ffmpeg:")
    print(" ".join(cmd))
    ffmpeg_proc = subprocess.Popen(cmd)

    # Wait for ffmpeg to finish
    ffmpeg_proc.wait()

    # Shut down Firefox
    driver.quit()

if __name__ == "__main__":
    main()
