# Sử dụng debian:10-slim làm base image
FROM debian:10-slim

# Tạo thư mục /app và đặt làm thư mục làm việc
RUN mkdir -p /app
WORKDIR /app

# Sao chép các file cần thiết vào thư mục /app
COPY . /app
# Cài đặt các dependencies hệ thống
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

# Tải và cài đặt Python 3.9.6
RUN wget https://www.python.org/ftp/python/3.9.6/Python-3.9.6.tgz \
    && tar xzf Python-3.9.6.tgz \
    && cd Python-3.9.6 \
    && ./configure --enable-optimizations \
    && make altinstall \
    && cd .. \
    && rm -rf Python-3.9.6* \
    && ln -s /usr/local/bin/python3.9 /usr/local/bin/python \
    && ln -s /usr/local/bin/pip3.9 /usr/local/bin/pip

# Nâng cấp pip cho Python 3.9
RUN pip install --upgrade pip

# Sao chép và cài đặt các dependencies Python từ requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn vào thư mục làm việc
COPY . .

# Thiết lập biến môi trường cho Google Cloud Vision API
ENV GOOGLE_APPLICATION_CREDENTIALS="/app/rapid-stage-425307-j4-58d15bd4cd2e.json"

# Mở cổng 8080
EXPOSE 8080

# Lệnh chạy ứng dụng
CMD ["python", "newapp.py"]
