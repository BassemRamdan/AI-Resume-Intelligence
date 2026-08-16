FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (needed for PyMuPDF, PyTorch, etc)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create a non-root user (required by HuggingFace Spaces)
RUN useradd -m -u 1000 user
USER user

# Set home to the user's home directory
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

# Copy the rest of the application
COPY --chown=user . $HOME/app

# HuggingFace Spaces exposes port 7860 by default
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
