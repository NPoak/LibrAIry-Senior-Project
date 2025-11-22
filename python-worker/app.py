from fastapi import FastAPI, Request
from sentence_transformers import SentenceTransformer
import torch

app = FastAPI()

# 1. GPU Setup
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"🚀 Loading model on device: {device}")

MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
# Load model to GPU
encoder = SentenceTransformer(MODEL_NAME, device=device)

@app.post("/embed")
async def embed_items(request: Request):
    # Get input data from n8n HTTP Request
    input_data = await request.json()
    
    # Ensure it's a list to match your original loop logic
    items = input_data if isinstance(input_data, list) else [input_data]
    
    output_items = []

    for item in items:
        try:
            # Extract fields
            # Note: Direct JSON input uses .get(), not .json.get()
            title = item.get('title', '') or ""
            author = item.get('author', '') or ""
            publisher = item.get('publisher', '') or ""
            description = item.get('description', '') or ""

            # --- YOUR EXACT LOGIC START ---
            parts = [
                f"Title: {title}",
                f"Author: {author}" if author else "",
                f"Publisher: {publisher}" if publisher else "",
                f"Description: {description}" if description else ""
            ]
            text_to_embed = ". ".join([p for p in parts if p != ""])

            if text_to_embed:
                # Encode on GPU
                embedding = encoder.encode(text_to_embed)
                vector_list = embedding.tolist()

                # Your specific string formatting
                vector_str_format = str(vector_list).replace(" ", "")

                output_items.append({
                    "title": title,
                    "combined_text_used": text_to_embed,
                    "vector": vector_list,
                    "vector_text": vector_str_format,
                    "dimension": len(vector_list)
                })
            else:
                output_items.append({"error": "No content to embed", "title": title})
            # --- YOUR EXACT LOGIC END ---

        except Exception as e:
            output_items.append({
                "error": str(e),
                "title": item.get('title')
            })

    return output_items