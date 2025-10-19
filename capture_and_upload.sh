#!/bin/bash

# Directory to store temporary images
IMG_DIR="/tmp/pose_imgs"
mkdir -p "$IMG_DIR"

# Start capturing images in a loop every second
while true; do
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    IMG_FILE="${IMG_DIR}/img_${TIMESTAMP}.jpg"

    # Capture single image quickly (timeout is in milliseconds)
    libcamera-still --width 432 --height 368 --output "$IMG_FILE" --nopreview --timeout 1 -v0

    # Upload to Google Cloud Storage
    gsutil cp "$IMG_FILE" gs://living_room_dogs/

    # Check if upload was successful before deleting
    if [ $? -eq 0 ]; then
        rm "$IMG_FILE"
    else
        echo "Upload failed for $IMG_FILE" >&2
    fi

    # Wait 1 second before next capture
    sleep 1
done

