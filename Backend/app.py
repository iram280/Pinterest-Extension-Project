from flask import Flask, request, jsonify
import imageExtract
import analysis

app = Flask(__name__)

@app.route('/process-image', methods=['GET'])
def process_image():
    try:
        # Step 1: Get the image from the frontend
        #board = request.files['image']  # Assuming the image is sent as a form file

        # Step 2: Extract images from the screenshot
        extracted_images = imageExtract.extractImages()

        # Step 3: Analyze the extracted images (e.g., using CLIP)
        analysis_results = analysis.processImage(extracted_images)

        # Step 4: Search for related products based on the analysis
        #products = search.search_for_products(analysis_results)

        # Step 5: Send the results back to the frontend as JSON
        #return jsonify({"products": products, "analysis": analysis_results})

    except Exception as e:
        return jsonify({"error": str(e),
                        "analysis_results" : analysis_results}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
