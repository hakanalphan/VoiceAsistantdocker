HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎤 Voice Assistant v2.3</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; background: linear-gradient(135deg, #667eea, #764ba2); min-height: 100vh; padding: 20px; }
        .container { max-width: 900px; margin: 0 auto; background: white; border-radius: 15px; padding: 30px; box-shadow: 0 15px 35px rgba(0,0,0,0.1); }
        .mic-section { background: linear-gradient(135deg, #ff6b6b, #ee5a24); color: white; text-align: center; padding: 30px; border-radius: 15px; margin: 25px 0; }
        .mic-button { background: white; color: #ff6b6b; border: none; padding: 20px; border-radius: 50%; font-size: 24px; cursor: pointer; transition: all 0.3s; margin: 15px; min-width: 80px; min-height: 80px; }
        .mic-button:hover { transform: scale(1.1); box-shadow: 0 5px 20px rgba(255,255,255,0.3); }
        .mic-button.recording { background: #ff4757; color: white; animation: pulse 2s infinite; }
        @keyframes pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.05); } }
        select, button { padding: 12px; border-radius: 8px; border: 1px solid #ddd; font-size: 16px; margin: 10px; }
        .result-box { background: #e8f5e8; border: 1px solid #c3e6cb; border-radius: 8px; padding: 20px; margin: 20px 0; display: none; }
        .json-display { background: #2d3748; color: #68d391; padding: 15px; border-radius: 8px; font-family: Monaco, monospace; font-size: 14px; white-space: pre-wrap; }
        .status { padding: 10px 20px; border-radius: 25px; display: inline-block; font-weight: bold; margin: 5px; }
        .status.ready { background: #d4edda; color: #155724; }
        .status.processing { background: #fff3cd; color: #856404; }
        .status.error { background: #f8d7da; color: #721c24; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎤 Voice Assistant v2.3</h1>
        <p>Sadece mikrofon ile sesli asistan</p>
        
        <!-- Mikrofon Bölümü -->
        <div class="mic-section">
            <h2>🎤 Mikrofon ile Konuş</h2>
            <p>Butona basıp tutarak konuşun</p>
            <button id="micButton" class="mic-button">🎤</button>
            <br>
            <select id="micVoiceSelect">
                <option value="nova">Nova - Genç Kadın</option>
                <option value="alloy">Alloy - Dengeli Kadın</option>
                <option value="shimmer">Shimmer - Yumuşak Kadın</option>
                <option value="echo">Echo - Erkek</option>
                <option value="onyx">Onyx - Derin Erkek</option>
                <option value="fable">Fable - İngiliz Erkek</option>
            </select>
            <div id="micStatus" class="status ready">Mikrofonunuz hazır</div>
        </div>

        <!-- Sonuç -->
        <div id="resultBox" class="result-box">
            <h3>📋 API Yanıtı:</h3>
            <div id="jsonResult" class="json-display"></div>
            <div id="audioPlayer" style="margin-top: 15px;"></div>
        </div>
    </div>

    <script>
        let mediaRecorder;
        let audioChunks = [];
        let isRecording = false;
        
        const micButton = document.getElementById('micButton');
        const micStatus = document.getElementById('micStatus');
        const resultBox = document.getElementById('resultBox');
        const jsonResult = document.getElementById('jsonResult');
        const audioPlayer = document.getElementById('audioPlayer');

        // Mikrofon başlat
        async function initMicrophone() {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                mediaRecorder = new MediaRecorder(stream);
                
                mediaRecorder.ondataavailable = (event) => {
                    audioChunks.push(event.data);
                };
                
                mediaRecorder.onstop = async () => {
                    const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
                    audioChunks = [];
                    await sendAudioToAPI(audioBlob, document.getElementById('micVoiceSelect').value);
                };
                
                micStatus.innerHTML = 'Mikrofonunuz hazır - Butona basıp tutarak konuşun';
                micStatus.className = 'status ready';
                
            } catch (error) {
                micStatus.innerHTML = 'Mikrofon erişim hatası: ' + error.message;
                micStatus.className = 'status error';
                micButton.disabled = true;
            }
        }

        // Mikrofon kontrolleri
        micButton.addEventListener('mousedown', startRecording);
        micButton.addEventListener('mouseup', stopRecording);
        micButton.addEventListener('mouseleave', stopRecording);
        micButton.addEventListener('touchstart', startRecording);
        micButton.addEventListener('touchend', stopRecording);

        function startRecording() {
            if (!mediaRecorder || isRecording) return;
            isRecording = true;
            audioChunks = [];
            mediaRecorder.start();
            micButton.classList.add('recording');
            micButton.innerHTML = '🔴';
            micStatus.innerHTML = 'Kayıt ediliyor...';
            micStatus.className = 'status processing';
        }

        function stopRecording() {
            if (!mediaRecorder || !isRecording) return;
            isRecording = false;
            mediaRecorder.stop();
            micButton.classList.remove('recording');
            micButton.innerHTML = '🎤';
            micStatus.innerHTML = 'İşleniyor...';
            micStatus.className = 'status processing';
        }

        // API'ye ses gönder
        async function sendAudioToAPI(audioBlob, voice) {
            try {
                const formData = new FormData();
                formData.append('audio_file', audioBlob, 'recording.webm');
                formData.append('voice', voice);

                const response = await fetch('/ask_assistant', {
                    method: 'POST',
                    body: formData
                });

                const data = await response.json();
                displayResult(data);
                
                micStatus.innerHTML = 'Hazır';
                micStatus.className = 'status ready';
                
            } catch (error) {
                micStatus.innerHTML = 'Hata: ' + error.message;
                micStatus.className = 'status error';
            }
        }

        // Sonuç göster
        function displayResult(data) {
            resultBox.style.display = 'block';
            jsonResult.textContent = JSON.stringify(data, null, 2);
            if (data.response_audio_url) {
                audioPlayer.innerHTML = `
                    <h4>🔊 Sesli Yanıt:</h4>
                    <audio controls style="width: 100%;">
                        <source src="${data.response_audio_url}" type="audio/wav">
                    </audio>
                `;
            } else {
                audioPlayer.innerHTML = '<p>⚠️ Sesli yanıt oluşturulamadı</p>';
            }
        }

        // Başlat
        initMicrophone();
    </script>
</body>
</html>
"""
