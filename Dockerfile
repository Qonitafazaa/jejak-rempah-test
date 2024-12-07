# Gunakan image Python 3.9
FROM python:3.9-slim

# Tentukan working directory di dalam container
WORKDIR /app

# Salin file requirements.txt dan install dependensi
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Salin seluruh file aplikasi ke dalam container
COPY . .

# Expose port yang digunakan
EXPOSE 8080

# Tentukan perintah yang akan dijalankan ketika container berjalan
CMD ["python", "run.py"]
