# Simple base image
FROM ubuntu:latest

# Prevent apt from asking questions
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      firefox \
      wget \
      xauth \
      x11-apps \
      pulseaudio \
      ffmpeg \
      python3 \
      python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install geckodriver (version may be updated as needed)
RUN wget -qO /tmp/geckodriver.tar.gz \
    https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux64.tar.gz && \
    tar -xzf /tmp/geckodriver.tar.gz -C /usr/local/bin && \
    rm /tmp/geckodriver.tar.gz

# Install Selenium Python package
RUN pip3 install selenium

# Copy our script into the container
COPY run_browser.py /usr/local/bin/run_browser.py
WORKDIR /data

# By default, run our Python script
CMD ["python3", "/usr/local/bin/run_browser.py"]
