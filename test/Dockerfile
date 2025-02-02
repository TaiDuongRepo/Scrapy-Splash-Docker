# Dockerfile
FROM python:3.9-slim

# Cài đặt các thư viện cần thiết
RUN pip install requests

# Sao chép script Python vào container
COPY test.py /app/test.py

# Thiết lập thư mục làm việc
WORKDIR /app

# Chạy test Python
CMD ["python", "test.py"]