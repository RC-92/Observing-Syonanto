#!/usr/bin/env bash

############################################################
# Precheck: Detect OS, Check and possibly install Docker & x11docker
############################################################

# Detect OS in a simple manner
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS_ID="$ID"
else
    echo "Cannot detect OS. /etc/os-release not found."
    exit 1
fi

# Function to install Docker
install_docker() {
    case "$OS_ID" in
        ubuntu|debian)
            echo "Installing Docker on $OS_ID..."
            sudo apt-get update
            sudo apt-get install -y docker.io
            ;;
        arch)
            echo "Installing Docker on Arch..."
            sudo pacman -Sy --noconfirm docker
            ;;
        *)
            echo "Unsupported OS for automatic Docker installation."
            echo "Please install Docker manually and re-run."
            exit 1
            ;;
    esac

    # Enable and start Docker
    sudo systemctl enable docker
    sudo systemctl start docker
}

# Function to install x11docker
install_x11docker() {
    case "$OS_ID" in
        ubuntu|debian)
            echo "Installing x11docker on $OS_ID..."
            sudo apt-get update
            sudo apt-get install -y x11docker
            # If package not found in your distro, fallback to manual install:
            # sudo wget https://raw.githubusercontent.com/mviereck/x11docker/master/x11docker -O /usr/local/bin/x11docker
            # sudo chmod +x /usr/local/bin/x11docker
            ;;
        arch)
            echo "Installing x11docker on Arch..."
            sudo pacman -Sy --noconfirm x11docker
            ;;
        *)
            echo "Unsupported OS for automatic x11docker installation."
            echo "Please install x11docker manually and re-run."
            exit 1
            ;;
    esac
}

# 1) Check Docker
if ! command -v docker &> /dev/null
then
    echo "Docker is not installed."
    read -rp "Would you like to install Docker now? (y/n) " DOCKER_CHOICE
    if [[ "$DOCKER_CHOICE" =~ ^[Yy](es)?$ ]]; then
        install_docker
    else
        echo "Docker is required. Exiting."
        exit 1
    fi
else
    echo "Docker is already installed."
fi

# 2) Check x11docker
if ! command -v x11docker &> /dev/null
then
    echo "x11docker is not installed."
    read -rp "Would you like to install x11docker now? (y/n) " X11DOCKER_CHOICE
    if [[ "$X11DOCKER_CHOICE" =~ ^[Yy](es)?$ ]]; then
        install_x11docker
    else
        echo "x11docker is required. Exiting."
        exit 1
    fi
else
    echo "x11docker is already installed."
fi

############################################################
# 3) Build your Docker image
############################################################
echo "Building Docker image 'operation143'..."
docker build -t operation143 .

# If the build fails, exit
if [ "$?" -ne 0 ]; then
    echo "Docker build failed. Exiting."
    exit 1
fi

############################################################
# 4) Sleep or wait for all the above to be completed
############################################################
echo "Sleeping 20 seconds..."
sleep 20

############################################################
# 5) Launch with x11docker
############################################################
echo "Launching container with x11docker..."
x11docker \
  --pulseaudio \
  --clipboard \
  --gpu \
  -v "$(pwd)":/data \
  -w /data \
  operation143
