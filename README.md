# Bulk Rename Script

This Python script renames image and video files in a specified folder using AI-generated SEO-friendly names and alt text. It leverages the Hugging Face BLIP model for captioning and supports various image and video formats.

## Features

-   **AI-powered renaming:** Uses the `Salesforce/blip-image-captioning-large` model to generate descriptive captions.
-   **SEO-friendly names:** Incorporates user-defined keywords and formats captions into URL-friendly filenames.
-   **Alt text generation:** Generates alt text for improved accessibility and SEO.
-   **Image support:** Handles common image formats, including HEIC/HEIF (requires `pillow-heif`).
-   **Video support:** Extracts a keyframe from video files (e.g., MOV, MP4) and uses it for captioning (requires `opencv-python`).
-   **Duplicate handling:** Appends incremental numbers to filenames to avoid conflicts.
-   **Logging:** Creates a CSV log file (`rename_log.csv`) with original filenames, new filenames, alt text, and status.

## Setup Instructions

1.  **Install the required packages:**

    ```bash
    pip install -r requirements_bulk_rename.txt
    ```

2.  **Configure the script:**

    Open `bulk_rename.py` and modify the following variables:

    ```python
    # ◆ Folder containing images and videos
    folder_path = r"E:\freelancing\tavistra\Products pictures\CPU processor keychain\Ankit"
    user_keywords = "cpu-processor-keychain" # Customize your keywords here, separated by hyphens
    ```

    -   `folder_path`: The absolute path to the directory containing the image and video files you want to rename.
    -   `user_keywords`: A string of keywords (separated by hyphens) that will be prepended to the AI-generated captions to create more specific and SEO-friendly filenames.

3.  **Run the script:**

    ```bash
    python bulk_rename.py
    ```

## How it Works

1.  The script iterates through all files in the specified `folder_path`.
2.  For each file:
    -   If it's a video file, it extracts the middle frame using OpenCV.
    -   If it's an HEIC/HEIF image, it uses `pillow-heif` to open it.
    -   Otherwise, it opens the image directly using Pillow.
3.  The image (or video keyframe) is then passed to the BLIP model to generate a descriptive caption.
4.  The `user_keywords` are prepended to the caption, and the entire string is formatted into an SEO-friendly filename (lowercase, hyphens instead of spaces, special characters removed).
5.  The file is renamed, and a log entry is recorded in `rename_log.csv`.

## Dependencies

-   `transformers`
-   `Pillow`
-   `torch`
-   `opencv-python`
-   `pillow-heif`
