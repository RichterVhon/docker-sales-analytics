# CREATE PRO Dockerfile
@"
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
LABEL org.opencontainers.image.source="https://github.com/yourname/sales-analytics"

# 📦 System dependencies (matplotlib + fonts)
RUN apt-get update && apt-get install -y \\
    gcc \\
    g++ \\
    libfreetype6-dev \\
    libpng-dev \\
    libjpeg-dev \\
    fonts-dejavu-core \\
    curl \\
    && apt-get clean \\
    && rm -rf /var/lib/apt/lists/*

# 📁 Working directory
WORKDIR /app

# 🔄 Copy requirements first (Docker layer caching!)
COPY requirements.txt .

# 🚀 Install Python packages + upgrade pip
RUN pip install --upgrade pip && \\
    pip install --no-cache-dir -r requirements.txt

# 📂 Copy source code
COPY . .

# 🛠️ Setup permissions & folders
RUN mkdir -p /app/graphs /app/logs && \\
    chmod +x main.py && \\
    echo \"$(date): App ready\" > /app/logs/docker.log

# 🌡️ Expose port (if you add web UI later)
EXPOSE 8080

# 📊 Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
    CMD python -c \"import pandas, seaborn; print('Healthy')\" || exit 1

# 📜 Logging config
ENV PYTHONUNBUFFERED=1
ENV LOG_DIR=/app/logs

# 🚀 Entry point with logging
CMD echo \"🚀 Starting Sales Analytics...\" && \\
    echo \"$(date): Container started\" >> /app/logs/docker.log && \\
    python main.py 2>&1 | tee -a /app/logs/app.log && \\
    echo \"$(date): Analysis complete\" >> /app/logs/docker.log
"@ | Out-File -FilePath "Dockerfile" -Encoding UTF8