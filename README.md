# VoiceAsistant



# 🎤 Voice Assistant - E-Ticaret Ses Asistanı

Kullanıcıların ses ile soru sormasını ve AI’dan sesli yanıt almasını sağlayan modern bir sesli asistan uygulaması. E-ticaret odaklıdır ve sipariş takibi, kargo durumu, iade süreçleri gibi müşteri hizmetleri sorularına yanıt verir.

---

## 🌟 Özellikler

* 🎤 **Ses Tanıma (STT)** → OpenAI Whisper ile Türkçe ses tanıma
* 🤖 **AI Yanıtları** → Together AI (Mistral 7B) ile akıllı yanıtlar
* 🔊 **Ses Üretimi (TTS)** → OpenAI TTS ile doğal ses sentezi
* 🌐 **Web Arayüzü** → Flask tabanlı, kullanıcı dostu ve hızlı
* 🛡️ **Güvenlik** → Dosya validasyonu, hata yönetimi ve güvenli API kullanımı

---


## 3️⃣ Kurulum (Docker ile)

1. Repo’yu klonlayın ve klasöre girin:

```bash
git clone https://github.com/hakanalphan/VoiceAsistantdocker.git
cd VoiceAsistantdocker
```

2. `.env` dosyasına API key’leri ekleyin:


OPENAI_API_KEY=sk-your-openai-api-key
TOGETHER_API_KEY=your-together-api-key


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






