import os
import csv
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch
import cv2 # Import OpenCV

# ◆ Folder containing images
folder_path = r"E:\freelancing\tavistra\Products pictures\CPU processor keychain\Ankit"
user_keywords = "cpu-processor-keychain" # Customize your keywords here, separated by hyphens

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

def generate_seo_name(file_path, keywords=""):
    """Use Hugging Face BLIP model to generate an SEO-friendly name, incorporating provided keywords."""
    
    # Define supported video extensions
    video_extensions = ('.mov', '.mp4', '.avi', '.mkv')

    if file_path.lower().endswith(video_extensions):
        # Process video file
        cap = cv2.VideoCapture(file_path)
        if not cap.isOpened():
            raise IOError(f"Cannot open video file: {file_path}")
        
        # Get middle frame
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        mid_frame_index = total_frames // 2
        cap.set(cv2.CAP_PROP_POS_FRAMES, mid_frame_index)
        
        ret, frame = cap.read()
        cap.release()
        
        if not ret:
            raise ValueError(f"Could not read frame from video: {file_path}")
        
        # Convert OpenCV BGR frame to PIL RGB image
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    elif file_path.lower().endswith(('.heic', '.heif')):
        from pillow_heif import register_heif_opener
        register_heif_opener()
        image = Image.open(file_path).convert("RGB")
    else:
        image = Image.open(file_path).convert("RGB")

    inputs = processor(image, return_tensors="pt")
    out = model.generate(**inputs)
    caption = processor.decode(out[0], skip_special_tokens=True)

    # Incorporate keywords
    if keywords:
        full_caption = f"{keywords.replace(' ', '-')}-{caption}"
    else:
        full_caption = caption

    # Format caption into an SEO-friendly name
    seo_name = full_caption.strip().lower().replace(" ", "-").replace(".", "")
    return seo_name, caption

def bulk_rename(folder_path):
    log_file_path = os.path.join(folder_path, "rename_log.csv")
    with open(log_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        log_writer = csv.writer(csvfile)
        log_writer.writerow(["Original Filename", "New Filename", "Alt Text", "Status", "Error Message"]) # CSV header

        for filename in os.listdir(folder_path):
            old_path = os.path.join(folder_path, filename)
            if os.path.isdir(old_path) or filename == "rename_log.csv":
                continue

            try:
                name, ext = os.path.splitext(filename)
                seo_name, alt_text = generate_seo_name(old_path, user_keywords)
                new_name = f"{seo_name}{ext.lower()}"
                new_name_base, new_ext = os.path.splitext(new_name)
                counter = 1
                while os.path.exists(os.path.join(folder_path, new_name)):
                    new_name = f"{new_name_base}-{counter}{new_ext}"
                    counter += 1
                new_path = os.path.join(folder_path, new_name)

                os.rename(old_path, new_path)
                print(f"✅ {filename} -> {new_name}")
                log_writer.writerow([filename, new_name, alt_text, "Success", ""])
            except Exception as e:
                print(f"❌ Error with {filename}: {e}")
                log_writer.writerow([filename, "", "Error", str(e)])

bulk_rename(folder_path)
