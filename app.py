from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from gtts import gTTS
import os
import uuid

app = Flask(__name__)
CORS(app)  # Allow all origins

@app.route('/')
def home():
    return jsonify({"status": "online", "message": "Text-to-Audiobook Backend is Running!"})

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
        
        # Limit text length
        if len(text) > 5000:
            text = text[:5000]
        
        print(f"Converting text ({len(text)} characters)...")
        
        # Create a unique filename
        filename = f"speech_{uuid.uuid4().hex}.mp3"
        
        # Convert text to speech
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(filename)
        
        print(f"Audio saved: {filename}")
        
        # Send the file back
        response = send_file(
            filename,
            mimetype='audio/mpeg',
            as_attachment=True,
            download_name=f"student_speech.mp3"
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
    print("TEXT-TO-AUDIOBOOK BACKEND FOR STUDENTS")
    print("=" * 50)
    print("Server running at: http://localhost:5000")
    print("Server running at: http://127.0.0.1:5000")
    print("\nTo use:")
    print("1. Keep this window OPEN")
    print("2. Open index.html in your browser")
    print("3. Type text and click 'Convert to Speech'")
    print("=" * 50)
    app.run(host='0.0.0.0', port=5000, debug=True)