FROM debian:10-slim

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libreadline-dev \
    libsqlite3-dev \
    libgdbm-dev \
    libdb5.3-dev \
    libbz2-dev \
    libexpat1-dev \
    liblzma-dev \
    tk-dev \
    libffi-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Download and install Python 3.8.5
RUN wget https://www.python.org/ftp/python/3.8.5/Python-3.8.5.tgz \
    && tar xzf Python-3.8.5.tgz \
    && cd Python-3.8.5 \
    && ./configure --enable-optimizations \
    && make altinstall \
    && cd .. \
    && rm -rf Python-3.8.5* 

# Upgrade pip
RUN python3.8 -m pip install --upgrade pip

# Copy and install requirements
COPY requirements.txt requirements.txt
RUN python3.8 -m pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

EXPOSE 8080

CMD ["python3.8", "app.py"]
