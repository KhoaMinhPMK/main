# Sử dụng base image đã cài đặt sẵn TensorFlow
FROM tensorflow/tensorflow:2.6.0 AS base

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Sao chép file yêu cầu vào thư mục làm việc
COPY requirements.txt .

# Cài đặt các thư viện từ requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn của bạn vào thư mục làm việc
COPY . .

# Mở cổng để Flask có thể chạy
EXPOSE 8080

# Chạy ứng dụng
CMD ["python", "app.py"]
