from flask import Flask, request, jsonify
import imageExtract
import analysis
import subprocess
import os

app = Flask(__name__)

@app.route('/process-image', methods=['POST'])
def process_image():
    try:
        # Step 1: Get the board URL from the frontend
        board_url = request.json.get('url')  # URL from the frontend
        if not board_url:
            return jsonify({"error": "No URL provided"}), 400

        # Step 2: Run Puppeteer script
        puppeteer_script = './screenshot.js'  # Path to the Puppeteer script
        screenshot_path = './yoursite.png'    # Expected screenshot path

        # Run the Puppeteer script
        subprocess.run(["node", puppeteer_script, board_url], check=True)

        # Step 3: Check if the screenshot exists
        if not os.path.exists(screenshot_path):
            return jsonify({"error": "Screenshot not generated"}), 500

        # Step 2: Extract images from the screenshot or board
        extracted_images = imageExtract.extractImages(board_url)

        # Step 3: Analyze the extracted images (e.g., using CLIP)
        analysis_results = analysis.processImage(extracted_images)

        # Step 4: Prepare response data (for now, just the analysis results)
        return jsonify({"analysis_results": analysis_results}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
