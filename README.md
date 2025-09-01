# VoiceAsistant

Tamam 👍 Sana iki versiyonlu **README** hazırladım: bir **Docker ile çalışma** ve bir **Docker’sız Python ile çalışma** bölümü var. Hem adım adım hem de kullanıcı dostu şekilde düzenlendi.

---

# 🎤 Voice Assistant - E-Ticaret Ses Asistanı

Kullanıcıların ses ile soru sormasını ve AI’dan sesli yanıt almasını sağlayan modern bir sesli asistan uygulaması. E-ticaret odaklıdır ve sipariş takibi, kargo durumu, iade süreçleri gibi müşteri hizmetleri sorularına yanıt verir.

---

## 🌟 Özellikler

* 🎤 **Ses Tanıma (STT)** → OpenAI Whisper ile Türkçe ses tanıma
* 🤖 **AI Yanıtları** → Together AI (Mistral 7B) ile akıllı yanıtlar
* 🔊 **Ses Üretimi (TTS)** → OpenAI TTS ile doğal ses sentezi
* 🌐 **Web Arayüzü** → Flask tabanlı, kullanıcı dostu ve hızlı
* 📱 **Responsive Tasarım** → Mobil ve masaüstü uyumlu arayüz
* 🛡️ **Güvenlik** → Dosya validasyonu, hata yönetimi ve güvenli API kullanımı

---

## 🚀 Hızlı Başlangıç

### 1️⃣ Gereksinimler

* Python 3.9+
* OpenAI API Key (Whisper ve TTS için)
* Together AI API Key (Mistral LLM için)

---

## 2️⃣ Kurulum (Docker’sız Python ile)

1. Repo’yu klonlayın:

```bash
git clone https://github.com/hakanalphan/VoiceAsistantdocker.git
cd VoiceAsistantdocker
```

2. Virtual environment oluşturun (önerilen):

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / Mac
python -m venv venv
source venv/bin/activate
```

3. Bağımlılıkları yükleyin:

```bash
pip install -r requirements.txt
```

4. API Key’lerini ayarlayın:

**Yöntem 1: Environment Variables (Önerilen)**

```bash
# Windows
set OPENAI_API_KEY=sk-your-openai-api-key
set TOGETHER_API_KEY=your-together-api-key

# Linux / Mac
export OPENAI_API_KEY=sk-your-openai-api-key
export TOGETHER_API_KEY=your-together-api-key
```

**Yöntem 2: `.env` Dosyası**

* Proje kök dizininde `.env` oluşturun ve içine ekleyin:

```
OPENAI_API_KEY=sk-your-openai-api-key
TOGETHER_API_KEY=your-together-api-key
```

5. Uygulamayı çalıştırın:

```bash
python app.py
```

6. Tarayıcıdan açın:
   👉 [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 3️⃣ Kurulum (Docker ile)

1. Repo’yu klonlayın ve klasöre girin:

```bash
git clone https://github.com/hakanalphan/VoiceAsistantdocker.git
cd VoiceAsistantdocker
```

2. `.env` dosyasını UTF-8 olarak oluşturun veya Notepad ile açın ve API key’leri ekleyin:

```
OPENAI_API_KEY=sk-your-openai-api-key
TOGETHER_API_KEY=your-together-api-key
```

3. Docker imajını build edin:

```bash
docker build -t voiceassistant2 .
```

4. Container’ı çalıştırın:

```bash
docker run -it -p 5000:5000 --env-file .env voiceassistant2
```

5. Tarayıcıdan açın:
   👉 [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

⚡ Artık mikrofonunuzla soru sorabilir ve AI’dan anında sesli yanıt alabilirsiniz!

---

İstersen ben bunu **doğrudan GitHub README.md formatına uygun, renkli emoji ve başlıklarla hazır** hale getirebilirim. Böylece GitHub’da direkt güzel görünür. Bunu yapayım mı?

    

Uygulama çalıştığında şu adrese gidin:
👉 http://127.0.0.1:5000

⚡ Artık mikrofonunuzla soru sorabilir ve AI’dan anında sesli yanıt alabilirsiniz!

