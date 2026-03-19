# ========================================
# 🚀 DELACRUZ SALES ANALYTICS - PRODUCTION
# Python 3.11 + Data Science + Logging
# ========================================

# 🏗️ Base image with data science stack
FROM python:3.11-slim

# 🏷️ Labels (professional metadata)
LABEL maintainer="delacruz@example.com"
LABEL version="1.0"
LABEL description="Sales Analytics Dashboard"

# 📦 System dependencies (matplotlib + fonts)
# We use \ at the end of lines to split one command into many for readability.
# IMPORTANT: Ensure there are NO spaces after the backslashes.
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libfreetype6-dev \
    libpng-dev \
    libjpeg-dev \
    fonts-dejavu-core \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 📁 Working directory inside the container
WORKDIR /app

# 🔄 Copy requirements first (to leverage Docker layer caching)
COPY requirements.txt .

# 🚀 Install Python packages + upgrade pip
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 📂 Copy all source code from your current folder to /app
COPY . .

# 🛠️ Setup permissions & folders for output (Updated to 'output')
RUN mkdir -p /app/output /app/logs && \
    chmod -R 777 /app/output /app/logs && \
    chmod +x main.py

# 🌡️ Expose port (useful if you add a Flask/FastAPI UI later)
EXPOSE 8080

# 📊 Healthcheck: Verifies if the core libraries are functional
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import pandas; print('Healthy')" || exit 1

# 📜 Logging and Python Environment config
ENV PYTHONUNBUFFERED=1
ENV LOG_DIR=/app/logs

# 🚀 Entry point: Logs the start time and runs the script
CMD ["sh", "-c", "echo '🚀 Starting Sales Analytics...' && python main.py 2>&1 | tee -a /app/logs/app.log"]