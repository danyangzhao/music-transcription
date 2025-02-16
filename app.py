from flask import Flask, render_template, request, send_file
import os
from music21 import converter
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('upload.html')

@app.route("/convert_midi_to_xml", methods=["POST"])
def convert_midi_to_xml():
    try:
        file = request.files.get("midi_file")
        logger.debug(f"Received file: {file}")
        if not file:
            logger.error("No file uploaded")
            return "No file uploaded", 400
        
        # Save it temporarily
        midi_path = os.path.join(app.config['UPLOAD_FOLDER'], "transcribed.mid")
        logger.debug(f"Saving MIDI to: {midi_path}")
        file.save(midi_path)
        
        # Convert to MusicXML (via music21)
        logger.debug("Starting music21 conversion")
        score = converter.parse(midi_path)
        xml_path = midi_path.replace(".mid", ".musicxml")
        logger.debug(f"Writing MusicXML to: {xml_path}")
        score.write("musicxml", fp=xml_path)

        logger.debug("Sending file back to client")
        return send_file(xml_path, as_attachment=True, download_name="transcribed.musicxml")
    
    except Exception as e:
        logger.exception(f"Error during conversion: {str(e)}")
        return f"An error occurred: {str(e)}", 500

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
