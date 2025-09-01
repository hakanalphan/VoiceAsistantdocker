import os
import logging
from pathlib import Path
from openai import OpenAI


from dotenv import load_dotenv
load_dotenv()  # .env dosyasını yükle
# Logging ayarları
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Klasörler
RESPONSES_DIR = Path("responses")
RESPONSES_DIR.mkdir(parents=True, exist_ok=True)
UPLOADS_DIR = Path("uploads")
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

# OpenAI API Key (Whisper STT ve TTS için kullandım)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
   OPENAI_API_KEY = "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"
   logger.warning(" OPENAI_API_KEY environment'dan alınamadı, fallback key kullanılıyor!")

# Together API Key (Mistral 7B için kullandım)
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
if not TOGETHER_API_KEY:
    logger.error(" TOGETHER_API_KEY bulunamadı! Environment variable olarak ayarlayın.")
    TOGETHER_API_KEY = "tgp_v1_TuE3WPVhlXEVvcNDF_61SYnSoeqVWfk3rSJd2gKoQOA"

# OpenAI Client (Whisper ve TTS için)
client = OpenAI(api_key=OPENAI_API_KEY)
logger.info(" OpenAI client başarıyla başlatıldı (Whisper & TTS için)")

# Together API ayarları
TOGETHER_BASE_URL = "https://api.together.xyz/v1/chat/completions"
MISTRAL_MODEL = "mistralai/Mistral-7B-Instruct-v0.1"

logger.info(f" Mistral Model: {MISTRAL_MODEL}")
logger.info(f" Responses klasörü: {RESPONSES_DIR}")
logger.info(f" Uploads klasörü: {UPLOADS_DIR}")