from flask import Flask, request, jsonify
from flask_cors import CORS
import imageExtract
import analysis
import subprocess
import base64
import io
from PIL import Image


app = Flask(__name__)
# Allow requests from all origins (or restrict to your Chrome extension ID)
CORS(app, origins=["chrome-extension://caomgookpgdkaoliabljgmejoiknhlmg"])

@app.route('/process-image', methods=['POST', 'OPTIONS'])
def process_image():
    try:
        
        if request.method == 'OPTIONS':
            return jsonify({"message": "Preflight request successful"}), 200
        
        board_url = request.json.get('url')  # URL from the frontend
        if not board_url:
            return jsonify({"error": "No URL provided"}), 400

        puppeteer_script = './Backend/main.js'  # Path to the Puppeteer script

        print("Running puppeteer script")
        # Run the Puppeteer script using subprocess
        result = subprocess.run(['node', puppeteer_script, board_url], capture_output=True, text=True)

        if result.returncode != 0:
            return jsonify({"error": "Error running Puppeteer script", "details": result.stderr}), 500

        print("Retrieving image")
        
        image_base64 = result.stdout.strip()  # Assuming Puppeteer outputs base64 directly
        if not image_base64:
            return jsonify({"error": "No image generated"}), 500

        print("Decoding base image")
        image_data = base64.b64decode(fix_base64_padding(image_base64))
        
        print("Opening image with PIL")
        try:
            image = Image.open(io.BytesIO(image_data))
            print(f"Image format: {image.format}")
        except Exception as e:
            print(f"Error processing image: {e}")
                
        extracted_images = imageExtract.extractImages(image)
        
        analysis_results = analysis.processImage(extracted_images)

        return jsonify({"analysis_results": analysis_results}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
def fix_base64_padding(base64_string):
    """
    Ensure the base64 string has the correct padding.
    Base64 strings should be divisible by 4. If not, padding ('=') is added.
    """
    
    print(len(base64_string))
    padding_needed = len(base64_string) % 4
    if padding_needed == 2:
        base64_string += "=="
    elif padding_needed == 3:
        base64_string += "="
        
    print(len(base64_string))
    return base64_string

if __name__ == '__main__':
    app.run(debug=True, port=5000)
