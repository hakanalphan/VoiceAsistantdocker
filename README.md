# VoiceAsistant

🎤 Voice Assistant - E-Ticaret Ses Asistanı

Kullanıcıların ses ile soru sormasını ve AI’dan sesli yanıt almasını sağlayan modern bir sesli asistan uygulaması.
E-ticaret odaklıdır ve sipariş takibi, kargo durumu, iade süreçleri gibi müşteri hizmetleri sorularına yanıt verir.

🌟 Özellikler

🎤 Ses Tanıma (STT) → OpenAI Whisper ile Türkçe ses tanıma

🤖 AI Yanıtları → Together AI (Mistral 7B) ile akıllı yanıtlar

🔊 Ses Üretimi (TTS) → OpenAI TTS ile doğal ses sentezi

🌐 Web Arayüzü → Flask tabanlı, kullanıcı dostu ve hızlı

📱 Responsive Tasarım → Mobil ve masaüstü uyumlu arayüz

🛡️ Güvenlik → Dosya validasyonu, hata yönetimi ve güvenli API kullanımı

🚀 Hızlı Başlangıç
1️⃣ Gereksinimler

Python 3.9+

OpenAI API Key (Whisper ve TTS için)

Together AI API Key (Mistral LLM için)

2️⃣ Kurulum
# Projeyi klonlayın
git clone <your-repo-url>
cd voice-assistant

# Virtual environment oluşturun (önerilen)
python -m venv venv
source venv/bin/activate    # Linux / Mac
venv\Scripts\activate       # Windows

# Bağımlılıkları yükleyin
pip install -r requirements.txt

3️⃣ API Key'lerini Ayarlayın

🔹 Yöntem 1: Environment Variables (Önerilen)

# Windows
set OPENAI_API_KEY=sk-your-openai-api-key-here
set TOGETHER_API_KEY=your-together-api-key-here

# Linux / Mac
export OPENAI_API_KEY=sk-your-openai-api-key-here
export TOGETHER_API_KEY=your-together-api-key-here


🔹 Yöntem 2: .env Dosyası

Proje kök dizininde .env dosyası oluşturun ve içine şu satırları ekleyin:

OPENAI_API_KEY=sk-your-openai-api-key-here
TOGETHER_API_KEY=your-together-api-key-here

4️⃣ Uygulamayı Çalıştırın
python app.py
    

Uygulama çalıştığında şu adrese gidin:
👉 http://127.0.0.1:5000

⚡ Artık mikrofonunuzla soru sorabilir ve AI’dan anında sesli yanıt alabilirsiniz!
