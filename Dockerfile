FROM debian:bookworm-slim

LABEL maintainer="user@example.com"
LABEL description="Python Development Environment with venv and PyInstaller on Debian"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3 \
    python3-full \
    python3-pip \
    python3-venv \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create and activate virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install PyInstaller in the virtual environment
RUN /opt/venv/bin/pip install pyinstaller

# Create symlink for PyInstaller binary
RUN ln -s /opt/venv/bin/pyinstaller /usr/local/bin/pyinstaller

# Setup app directory
WORKDIR /app
VOLUME /app

# Verify installations
RUN python3 --version \
    && pip3 --version \
    && pyinstaller --version

CMD ["/bin/bash"]