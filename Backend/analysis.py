import torch
import clip
from PIL import Image

# load model and preprocess
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)
    
def processImage():
    
    similarities = []

    for image in extracted_images:
        # load image
        image = preprocess()
        image = torch.unsqueeze(image, 0).to(device)

        # Define text descriptions
        texts = ["bohemian", "grunge", "goth", "Early 2000s", "Soft girl"]
        text_tokens = clip.tokenize(texts).to(device)

        # Make predictions
        with torch.no_grad():
            image_features = model.encode_image(image)
            text_features = model.encode_text(text_tokens)

        # Compute similarity between image and text
        similarity = (image_features @ text_features.T).softmax(dim=-1)
        similarities.append(similarity)
    
