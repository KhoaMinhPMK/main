# Sử dụng hình ảnh Python chính thức làm hình ảnh gốc
FROM python:3.9-slim

# Đặt biến môi trường PYTHONUNBUFFERED thành 1 để đầu ra của Python được gửi thẳng tới terminal
ENV PYTHONUNBUFFERED=1

# Tạo và đặt thư mục làm việc
WORKDIR /app

# Sao chép file requirements.txt vào thư mục làm việc
COPY requirements.txt /app/

# Cài đặt các thư viện cần thiết
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép tất cả các file và thư mục vào thư mục làm việc
COPY . /app/

# Mở cổng 8080 để truy cập vào ứng dụng
EXPOSE 8080

# Khởi động ứng dụng Flask
CMD ["python", "newapp.py"]
