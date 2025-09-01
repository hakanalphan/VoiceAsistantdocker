import os
import uuid
import requests
from pathlib import Path
from config import client, RESPONSES_DIR, logger, TOGETHER_API_KEY, TOGETHER_BASE_URL, MISTRAL_MODEL

class VoiceAssistantAPI:
    def __init__(self):
        self.supported_audio_formats = ['.wav', '.mp3', '.m4a', '.flac', '.ogg', '.webm']
        self.available_voices = {
            'alloy': 'Alloy - Dengeli Kadın',
            'echo': 'Echo - Erkek',
            'fable': 'Fable - İngiliz Erkek',
            'onyx': 'Onyx - Derin Erkek',
            'nova': 'Nova - Genç Kadın (Önerilen)',
            'shimmer': 'Shimmer - Yumuşak Kadın'
        }

    # OpenAI Whisper ile ses tanıma
    def speech_to_text(self, audio_file_path: str) -> str:
        if not client:
            logger.error("OpenAI client bulunamadı")
            return "OpenAI client bağlanamıyor"
        
        if not os.path.exists(audio_file_path):
            logger.error(f"Ses dosyası bulunamadı: {audio_file_path}")
            return "Ses dosyası bulunamadı"

        try:
            file_size = os.path.getsize(audio_file_path)
            if file_size == 0:
                logger.error("Ses dosyası boş")
                return "Ses dosyası boş"
            if file_size > 25 * 1024 * 1024:
                logger.error("Ses dosyası çok büyük")
                return "Ses dosyası çok büyük"

            logger.info(f"🎤 Ses tanıma başlıyor: {audio_file_path} ({file_size} bytes)")

            with open(audio_file_path, "rb") as audio_file:
                response = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language="tr"
                )

            transcribed_text = response.text.strip()
            logger.info(f"Ses tanıma tamamlandı: '{transcribed_text}'")

            if not transcribed_text or len(transcribed_text.strip()) < 2:
                logger.warning("Ses tanıma boş sonuç döndü")
                return "Ses tanınamadı"
            
            return transcribed_text

        except Exception as e:
            logger.error(f"STT hatası: {str(e)}")
            return "Ses tanıma hatası"

    # Together AI ile Mistral yanıt üretme
    def generate_assistant_response(self, user_message: str) -> dict:
        if not user_message or user_message.startswith("❌"):
            return {"assistant_response": "Geçerli bir mesaj bulunamadı"}
        
        if not TOGETHER_API_KEY or TOGETHER_API_KEY == "your-together-api-key-here":
            logger.error("Together API key bulunamadı")
            return {"assistant_response": "Together API key bulunamadı"}
        
        headers = {
            "Authorization": f"Bearer {TOGETHER_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": MISTRAL_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "Sen bir e-ticaret müşteri hizmetleri asistanısın. "
                        "Türkçe konuş, kısa, anlaşılır ve net yanıtlar ver. "
                        "Her zaman nazik, profesyonel ve kullanıcı dostu ol. "
                        "Yanıtların bilgilendirici, çözüm odaklı ve güven verici olsun."
                    )
                },

# ----- Elimde RAG veya fine-tuning için kullanılacak hazır bir veri olmadığından, 
#       modelin yanıtlarını yönlendirmek için Few-shot kullandım. -----


                {
                    "role": "user",
                    "content": "Siparişim nerede?"
                },
                {
                    "role": "assistant",
                    "content": "Siparişiniz kargoya verilmiş olup, 4 iş günü içinde teslim edilmesi beklenmektedir."
                },
                {
                    "role": "user",
                    "content": "Kargom ne zaman gelir?"
                },
                {
                    "role": "assistant",
                    "content": "Kargonuz yola çıkmıştır, 2-3 iş günü içinde adresinize teslim edilmesi beklenmektedir."
                },
                {
                    "role": "user",
                    "content": "İade nasıl yapabilirim?"
                },
                {
                    "role": "assistant",
                    "content": "Ürün iadesi için hesabınıza giriş yapıp, 'Siparişlerim' bölümünden iade talebi oluşturabilirsiniz. Kargo görevlisi ürünü adresinizden alacaktır."
                },
                {
                    "role": "user",
                    "content": "Teslimat adresimi değiştirebilir miyim?"
                },
                {
                    "role": "assistant",
                    "content": "Siparişiniz henüz kargoya verilmediyse, adres değişikliğini müşteri panelinizden yapabilirsiniz. Eğer kargoya verildiyse kargo firması ile iletişime geçmeniz gerekir."
                },
                # Gerçek kullanıcı sorusu
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            "max_tokens": 150,
            "temperature": 0.5,
            "top_p": 0.9,
            "stream": False
        }

        try:
            logger.info(f"AI yanıtı istek gönderiliyor: '{user_message}'")
            response = requests.post(TOGETHER_BASE_URL, headers=headers, json=payload, timeout=30)
            response.raise_for_status()

            result = response.json()
            assistant_response = result.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
            logger.info(f"AI yanıtı alındı: '{assistant_response[:50]}...'")
            return {"assistant_response": assistant_response or "Yanıt boş döndü"}

        except requests.exceptions.Timeout:
            logger.error("Together API timeout")
            return {"assistant_response": "Yanıt süresi aşıldı"}
        except Exception as e:
            logger.error(f"Mistral yanıt hatası: {str(e)}")
            return {"assistant_response": "Üzgünüm, şu anda yanıt veremiyorum"}

    # OpenAI TTS ile ses üretme
    def text_to_speech_openai(self, text: str, voice: str = "nova", filename_prefix: str = "response") -> str:
        if not client:
            logger.error("OpenAI client bulunamadı (TTS)")
            return None
            
        if not text or not text.strip():
            logger.error("TTS için metin boş")
            return None
            
        if text.startswith("❌"):
            logger.warning("Hata mesajı için TTS üretilmeyecek")
            return None

        try:
            logger.info(f"🔊 TTS üretiliyor: '{text[:30]}...' (ses: {voice})")

            filename = f"{filename_prefix}_{uuid.uuid4().hex[:8]}.wav"
            output_path = RESPONSES_DIR / filename

            with client.audio.speech.with_streaming_response.create(
                model="gpt-4o-mini-tts",
                voice=voice if voice in self.available_voices else "nova",
                input=text
            ) as response:
                response.stream_to_file(output_path)

            logger.info(f"TTS dosyası oluşturuldu: {output_path}")
            return str(output_path)

        except Exception as e:
            logger.error(f"TTS hatası: {str(e)}")
            return None





