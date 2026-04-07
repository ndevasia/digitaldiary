FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (ffmpeg, etc.)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY backend/ .

# Create necessary directories
RUN mkdir -p recordings screenshots audio profile_pics

# Copy ffmpeg to the expected bin directory structure based on container arch
RUN ARCH="$(dpkg --print-architecture)" && \
    if [ "$ARCH" = "amd64" ]; then TARGET_ARCH="x64"; \
    elif [ "$ARCH" = "arm64" ]; then TARGET_ARCH="arm64"; \
    else echo "Unsupported architecture: $ARCH" && exit 1; fi && \
    mkdir -p "bin/linux/${TARGET_ARCH}" && \
    cp "$(which ffmpeg)" "bin/linux/${TARGET_ARCH}/ffmpeg"

# Expose port
EXPOSE 5001

# Run the Flask app
CMD ["python", "window/app.py"]
