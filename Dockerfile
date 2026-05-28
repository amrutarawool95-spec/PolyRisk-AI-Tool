# Use a lightweight python base image
FROM python:3.11-slim

# Install necessary system libraries for building bioinformatics extensions
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    zlib1g-dev \
    libbz2-dev \
    liblzma-dev \
    libcurl4-gnutls-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Set up working directory inside container framework
WORKDIR /app

# Copy requirements mapping references first to speed up caching layers
COPY requirements.txt .

# Install dependencies using clean pip optimization flags
RUN pip install --no-cache-dir -r requirements.txt

# Copy all engineering package components across internal systems
COPY . .

# Expose standard default port mapping parameters used by Streamlit apps
EXPOSE 8501

# Configure container parameters checking health monitoring vectors
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Direct standard runtime structures to run app components automatically
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

