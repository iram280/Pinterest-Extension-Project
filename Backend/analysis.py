import torch
import clip
from PIL import Image


# load model and preprocess
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)
    
def processImage(extracted_images):
    
    similarities = []

    for image in extracted_images:
        
        image = preprocess(image).unsqueeze(0).to(device)

        # Define text descriptions
        texts = ["bohemian", "grunge", "goth", "Early 2000s", "Soft girl"]
        text_tokens = clip.tokenize(texts).to(device)

        # Make predictions
        with torch.no_grad():
            image_features = model.encode_image(image)
            text_features = model.encode_text(text_tokens)

        # Compute similarity between image and text
        similarity = (image_features @ text_features.T)

        similarity = similarity.squeeze(0)

        similarity = similarity.softmax(dim=-1)

        formatted_similarity = [f"{sim:.4f}" for sim in similarity.tolist()]

        similarities.append(formatted_similarity)

    print(similarities)

    token_score = [0, 0, 0, 0, 0]

    for similarity in similarities:

        highest_value_index = similarity.index(max(similarity))

        token_score[highest_value_index] += 1

    print(token_score)
    print(f"This board's aesthetic is {texts[token_score.index(max(token_score))]}")