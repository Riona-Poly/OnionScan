from flask import Flask, render_template, request
import cv2
import os
import uuid
import time
import threading

from detector import detect_layers

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Temporary files will be deleted after 1 minute
FILE_LIFETIME = 60


def cleanup_old_files():
    """Continuously delete temporary files older than 1 minute."""

    while True:

        current_time = time.time()

        for filename in os.listdir(UPLOAD_FOLDER):

            filepath = os.path.join(
                UPLOAD_FOLDER,
                filename
            )

            if not os.path.isfile(filepath):
                continue

            file_age = (
                current_time -
                os.path.getmtime(filepath)
            )

            if file_age > FILE_LIFETIME:

                try:
                    os.remove(filepath)
                    print(
                        "Deleted temporary file:",
                        filename
                    )

                except OSError:
                    pass

        # Check every 10 seconds
        time.sleep(10)


@app.route("/", methods=["GET", "POST"])
def index():

    count = None
    output_image = None

    if request.method == "POST":

        if "image" not in request.files:

            return render_template(
                "index.html",
                error="No image selected."
            )

        file = request.files["image"]

        if file.filename == "":

            return render_template(
                "index.html",
                error="Please select an image."
            )

        # Get original file extension
        extension = os.path.splitext(
            file.filename
        )[1]

        # Create temporary upload filename
        filename = (
            "upload_" +
            str(uuid.uuid4()) +
            extension
        )

        filepath = os.path.join(
            UPLOAD_FOLDER,
            filename
        )

        # Save uploaded image temporarily
        file.save(filepath)

        # Read image
        image = cv2.imread(filepath)

        if image is None:

            try:
                os.remove(filepath)
            except OSError:
                pass

            return render_template(
                "index.html",
                error="Could not read the image."
            )

        # Run onion layer detection
        count, result = detect_layers(image)

        # Create temporary result filename
        result_filename = (
            "result_" +
            str(uuid.uuid4()) +
            ".jpg"
        )

        result_path = os.path.join(
            UPLOAD_FOLDER,
            result_filename
        )

        # Save result
        cv2.imwrite(
            result_path,
            result
        )

        # Original uploaded image is no longer needed
        try:
            os.remove(filepath)
        except OSError:
            pass

        # Browser displays the result
        output_image = (
            "/static/uploads/" +
            result_filename
        )

    return render_template(
        "index.html",
        count=count,
        image=output_image
    )


# Start automatic cleanup in background
cleanup_thread = threading.Thread(
    target=cleanup_old_files,
    daemon=True
)

cleanup_thread.start()


if __name__ == "__main__":
    app.run(debug=True)