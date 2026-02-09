from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from gtts import gTTS
import os
import uuid

app = Flask(__name__)
CORS(app)  # Allow all origins

@app.route('/')
def home():
    return jsonify({
        "status": "online", 
        "message": "Text-to-Audiobook Backend is Running!",
        "version": "1.0.0",
        "instructions": "Send POST request to /convert with JSON: {\"text\": \"your text here\"}"
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/convert', methods=['POST', 'OPTIONS'])
def convert_text_to_speech():
    if request.method == 'OPTIONS':
        # Handle preflight request
        return '', 200
    
    try:
        # Get text from the request
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({"error": "No text provided"}), 400
        
        # Optional: get language and speed (for future use)
        language = data.get('language', 'en')
        speed = data.get('speed', 1.0)
        
        # Limit text length
        if len(text) > 5000:
            text = text[:5000]
        
        print(f"Converting text ({len(text)} characters)...")
        
        # Create a unique filename
        filename = f"speech_{uuid.uuid4().hex}.mp3"
        
        # Convert text to speech
        # Note: gTTS doesn't support speed parameter directly
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(filename)
        
        print(f"Audio saved: {filename}")
        
        # Send the file back
        response = send_file(
            filename,
            mimetype='audio/mpeg',
            as_attachment=True,
            download_name="student_speech.mp3"
        )
        
        # Clean up the file after sending
        @response.call_on_close
        def cleanup():
            try:
                if os.path.exists(filename):
                    os.remove(filename)
                    print(f"Cleaned up: {filename}")
            except:
                pass
        
        return response
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": f"Conversion failed: {str(e)}"}), 500

if __name__ == '__main__':
    print("=" * 50)
    print("TEXT-TO-AUDIOBOOK BACKEND")
    print("=" * 50)
    print("Endpoints:")
    print("- GET  /        : Server status")
    print("- GET  /health  : Health check")
    print("- POST /convert : Convert text to speech")
    print("=" * 50)
    
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
    app.run(host='0.0.0.0', port=5000, debug=True)
