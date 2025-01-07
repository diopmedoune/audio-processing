// JavaScript pour afficher le nom du fichier sélectionné
const audioInput = document.getElementById('audio_file');
const fileNameDisplay = document.getElementById('file-name');

audioInput.addEventListener('change', function () {
    if (this.files && this.files[0]) {
        fileNameDisplay.textContent = `Fichier sélectionné : ${this.files[0].name}`;
    } else {
        fileNameDisplay.textContent = 'Aucun fichier sélectionné';
    }
});

let mediaRecorder;
    let audioChunks = [];
    let audioBlob;

    async function startRecording() {
        // Obtenir les permissions du microphone
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);

        audioChunks = [];

        // Collecter les données audio
        mediaRecorder.ondataavailable = event => {
            audioChunks.push(event.data);
        };

        mediaRecorder.onstop = async () => {
            // Créer un Blob audio
            audioBlob = new Blob(audioChunks, { type: 'audio/webm' });

            // Convertir le Blob audio en WAV
            const wavBlob = await convertToWAV(audioBlob);

            // Prévisualiser l'audio dans un lecteur
            const audioUrl = URL.createObjectURL(wavBlob);
            document.getElementById('audioPreview').src = audioUrl;

            // Lire les données WAV pour l'envoi
            const reader = new FileReader();
            reader.onloadend = () => {
                document.getElementById('audioData').value = reader.result.split(',')[1];
                document.getElementById('submitAudio').disabled = false; // Activer le bouton d'envoi
            };
            reader.readAsDataURL(wavBlob);
        };

        mediaRecorder.start();
        document.getElementById('startRecording').disabled = true;
        document.getElementById('stopRecording').disabled = false;
    }

    function stopRecording() {
        mediaRecorder.stop();
        document.getElementById('startRecording').disabled = false;
        document.getElementById('stopRecording').disabled = true;
    }

    // Fonction pour convertir le Blob en WAV
    async function convertToWAV(blob) {
        const audioBuffer = await blob.arrayBuffer();
        const context = new AudioContext();
        const decodedAudio = await context.decodeAudioData(audioBuffer);

        const numberOfChannels = decodedAudio.numberOfChannels;
        const sampleRate = decodedAudio.sampleRate;

        // Convertir l'audio en PCM
        const pcmData = [];
        for (let channel = 0; channel < numberOfChannels; channel++) {
            pcmData.push(decodedAudio.getChannelData(channel));
        }

        // Encapsuler le PCM dans un fichier WAV
        const wavBlob = encodeWAV(pcmData, sampleRate, numberOfChannels);
        return new Blob([wavBlob], { type: 'audio/wav' });
    }

    function encodeWAV(samples, sampleRate, numChannels) {
        const bufferLength = samples[0].length * numChannels * 2 + 44;
        const buffer = new ArrayBuffer(bufferLength);
        const view = new DataView(buffer);

        // Écriture de l'entête WAV
        writeString(view, 0, 'RIFF'); // ChunkID
        view.setUint32(4, 36 + samples[0].length * numChannels * 2, true); // ChunkSize
        writeString(view, 8, 'WAVE'); // Format
        writeString(view, 12, 'fmt '); // Subchunk1ID
        view.setUint32(16, 16, true); // Subchunk1Size
        view.setUint16(20, 1, true); // AudioFormat (PCM)
        view.setUint16(22, numChannels, true); // NumChannels
        view.setUint32(24, sampleRate, true); // SampleRate
        view.setUint32(28, sampleRate * numChannels * 2, true); // ByteRate
        view.setUint16(32, numChannels * 2, true); // BlockAlign
        view.setUint16(34, 16, true); // BitsPerSample
        writeString(view, 36, 'data'); // Subchunk2ID
        view.setUint32(40, samples[0].length * numChannels * 2, true); // Subchunk2Size

        // Écriture des données PCM
        let offset = 44;
        for (let i = 0; i < samples[0].length; i++) {
            for (let channel = 0; channel < numChannels; channel++) {
                const sample = Math.max(-1, Math.min(1, samples[channel][i]));
                view.setInt16(offset, sample < 0 ? sample * 0x8000 : sample * 0x7FFF, true);
                offset += 2;
            }
        }

        return buffer;
    }

    function writeString(view, offset, string) {
        for (let i = 0; i < string.length; i++) {
            view.setUint8(offset + i, string.charCodeAt(i));
        }
    }