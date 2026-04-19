import os
import glob
import json
import base64
import requests
import shutil
import time
from PIL import Image
import io

API_KEY = "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"
MODEL = "google/gemini-2.5-flash"

CATEGORIES = ["book-covers", "book-scans", "schematics-and-figures", "misc"]
SOURCE_DIR = r"C:\Users\Justi\McCasland\assets\TMBSPACESHIPS"
TARGET_DIR = r"C:\Users\Justi\McCasland\assets\categorized"

def encode_image(image_path):
    try:
        with Image.open(image_path) as img:
            # Convert to RGB to avoid issues with PNG transparency when saving as JPEG
            if img.mode != "RGB":
                img = img.convert("RGB")
            
            # Resize image to save tokens and bandwidth (max 512x512)
            img.thumbnail((512, 512))
            
            buffer = io.BytesIO()
            img.save(buffer, format="JPEG", quality=85)
            return base64.b64encode(buffer.getvalue()).decode('utf-8')
    except Exception as e:
        print(f"Error encoding image {image_path}: {e}")
        return None

def analyze_image(base64_img):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    prompt = (
        "You are an assistant organizing a collection of UFO/space/historical research images. "
        "Analyze this image and categorize it into exactly ONE of the following categories: "
        f"{', '.join(CATEGORIES)}. "
        "Also suggest a short, descriptive filename base directly related to visually what's happening (e.g. 'alien-schematic-top-view', '1950s-ufo-book-cover', 'handwritten-field-schema', 'newspaper-clipping-roswell'). "
        "Use hyphens for spaces in the filename. "
        "Respond ONLY with a raw JSON object string (do not format as markdown) with format: "
        '{"category": "category-name", "suggested_filename": "some-descriptive-name"}'
    )
    
    data = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_img}"}}
                ]
            }
        ],
        "response_format": {"type": "json_object"}
    }
    
    for attempt in range(3):
        try:
            response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                # clean possible markdown
                content = content.replace("```json", "").replace("```", "").strip()
                try:
                    js = json.loads(content)
                    return js
                except json.JSONDecodeError:
                    print(f"JSON Parse Error on: {content}")
                    return None
            else:
                print(f"API Error {response.status_code}: {response.text}")
                time.sleep(2)
        except Exception as e:
            print(f"Request exception: {e}")
            time.sleep(2)
            
    return None


def main():
    image_paths = []
    for ext in ('*.jpg', '*.png', '*.jpeg'):
        image_paths.extend(glob.glob(os.path.join(SOURCE_DIR, '**', ext), recursive=True))
    
    print(f"Found {len(image_paths)} images to process.")
    
    for cat in CATEGORIES:
        os.makedirs(os.path.join(TARGET_DIR, cat), exist_ok=True)
        
    for idx, path in enumerate(image_paths):
        print(f"Processing {idx+1}/{len(image_paths)}: {os.path.basename(path)}")
        b64 = encode_image(path)
        if not b64:
            continue
            
        result = analyze_image(b64)
        if result:
            cat = result.get('category')
            if cat not in CATEGORIES:
                cat = "misc"
                
            base_filename = os.path.basename(path)
            # Try to preserve the existing YYYYMMDD_HHMMSS prefix
            parts = base_filename.split('_')
            prefix = parts[0] + "_" + parts[1] if len(parts) >= 2 and len(parts[0]) == 8 else "unknown-date"
            
            sug_name = result.get('suggested_filename', 'unnamed')
            ext = os.path.splitext(path)[1]
            
            new_filename = f"{prefix}_{sug_name}{ext}"
            new_filename = new_filename.replace(" ", "-").lower() # sanitize just in case
            
            target_path = os.path.join(TARGET_DIR, cat, new_filename)
            
            # Avoid overwrites
            counter = 1
            while os.path.exists(target_path):
                new_filename = f"{prefix}_{sug_name}-{counter}{ext}"
                target_path = os.path.join(TARGET_DIR, cat, new_filename)
                counter += 1
                
            shutil.copy2(path, target_path)
            print(f" -> Copied to {cat}/{new_filename}")
        else:
            print(" -> Failed to analyze.")

if __name__ == '__main__':
    main()
