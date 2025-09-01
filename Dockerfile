# Python tabanlı imaj
FROM python:3.11-slim

# Çalışma dizini oluştur
WORKDIR /app

# Gereken dosyaları kopyala
COPY requirements.txt .

# Bağımlılıkları yükle
RUN pip install --no-cache-dir -r requirements.txt

# Proje dosyalarını kopyala
COPY . .

# Flask default portu aç
EXPOSE 5000

# Uygulamayı çalıştır
CMD ["python", "app.py"]
