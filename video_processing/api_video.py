import io
import os
from google.oauth2 import service_account
from google.cloud import speech
import subprocess
from flask import *

app = Flask(__name__)

"""
speech to text code
"""
def channel_cnt(file_name):

    cmd = ['ffprobe', file_name, '-show_entries', 'stream=channels', '-select_streams', 'a', '-of', 'compact=p=0:nk=1', '-v', '0']


    result = subprocess.run(cmd, capture_output=True, text=True)

    
    return (result.stdout)


def speech_to_text(file_name):

    client_file = 'sa_speech_demo.json'
    credentials = service_account.Credentials.from_service_account_file(client_file)
    client = speech.SpeechClient(credentials = credentials)

    #load audio file
    audio_file = file_name 
    with io.open(audio_file, 'rb') as f:
        content = f.read()
        audio = speech.RecognitionAudio(content = content)

    cnt = channel_cnt(file_name)
    config = speech.RecognitionConfig(
        encoding = speech.RecognitionConfig.AudioEncoding.LINEAR16,
        audio_channel_count= int(cnt[0]),
        language_code = 'en-US',

    )

    response = client.recognize(config = config, audio = audio)

    audio_transcript = ''
    for result in response.results:
        audio_transcript+=((result.alternatives[0].transcript)+'.')
    
    return audio_transcript


def mp4_to_wav(file_name):
    new_file = file_name[:-4]
    print(new_file)
    file_type = '.wav'
    new_file += file_type
    cmd = ['ffmpeg', '-i', file_name, '-ac', '2', '-f','wav',new_file]
    result = subprocess.run(cmd, capture_output=True, text=True)

    
    return (result)

# TODO
def process_transcript_with_ml():
    pass

"""
API to integrate speech to text and ML model

need a POST request so we can send the video as a file parameter
"""

@app.route("/api/video", methods=["POST"])
def process_video():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
            
        file = request.files['file']
        video_id = request.form.get('video_id')
        
        if not video_id:
            return jsonify({'error': 'No video_id provided'}), 400

        # Create temporary file for video processing
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_video:
            file.save(temp_video.name)
            temp_video_path = temp_video.name

        # Process video
        wav_path = mp4_to_wav(temp_video_path)
        transcript = speech_to_text(wav_path)
        ml_results = process_transcript_with_ml(transcript)
        
        # Clean up temporary files
        os.remove(temp_video_path)
        os.remove(wav_path)
        
        # TODO
        # Store ML results in database
        # Implement database storage logic here
        
        return jsonify({
            "success": True,
            "video_id": video_id,
            "results": ml_results
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True)