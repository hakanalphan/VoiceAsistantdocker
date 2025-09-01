from flask import Flask, request, jsonify, send_file, render_template_string
from flask_cors import CORS
from werkzeug.utils import secure_filename
import uuid
from datetime import datetime
from pathlib import Path

from assistant import VoiceAssistantAPI
from config import RESPONSES_DIR, UPLOADS_DIR, client, logger
from templates import HTML_TEMPLATE
from utils import safe_delete

app = Flask(__name__)
CORS(app)

voice_assistant = VoiceAssistantAPI()

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route("/ask_assistant", methods=["POST"])
def ask_assistant():
    if 'audio_file' not in request.files:
        return jsonify({'error': 'audio_file gerekli'}), 400
    audio_file = request.files['audio_file']
    if audio_file.filename == '':
        return jsonify({'error': 'Dosya seçilmedi'}), 400

    voice = request.form.get('voice', 'nova')
    filename = secure_filename(f"{uuid.uuid4().hex[:8]}_{audio_file.filename}")
    temp_file_path = UPLOADS_DIR / filename
    audio_file.save(temp_file_path)

    try:
        text = voice_assistant.speech_to_text(str(temp_file_path))
        response_text = voice_assistant.generate_assistant_response(text)["assistant_response"]
        tts_path = voice_assistant.text_to_speech_openai(response_text, voice, filename_prefix=Path(filename).stem)

        return jsonify({
            "transcribed_text": text,
            "assistant_response": response_text,
            "response_audio_url": f"/responses/{Path(tts_path).name}" if tts_path else None
        })
    finally:
        safe_delete(temp_file_path)

@app.route("/responses/<filename>")
def serve_response_audio(filename):
    audio_path = RESPONSES_DIR / filename
    if not audio_path.exists():
        return jsonify({'error': 'Dosya bulunamadı'}), 404
    return send_file(audio_path, mimetype="audio/wav")

@app.route("/health")
def health_check():
    return jsonify({
        "status": "healthy" if client else "degraded",
        "timestamp": datetime.now().isoformat(),
        "version": "v2.3"
    })

if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000, debug=True)
