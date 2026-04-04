
from flask import Flask, render_template, request
import os
from deepface import DeepFace

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads/"
DATASET_PATH = "dataset"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    dhoni_list = []
    pvsindhu_list = []
    unknown_list = []

    files = request.files.getlist("files")

    if not files or files[0].filename == "":
        return render_template("index.html")

    for file in files:
        if file.filename == "":
            continue

        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        label = "unknown"
        emotion = "unknown"

        try:
            result = DeepFace.find(
                img_path=filepath,
                db_path=DATASET_PATH,
                enforce_detection=False,
                model_name="Facenet"
            )

            if len(result) > 0 and len(result[0]) > 0:
                identity_path = result[0]['identity'][0]
                if "dhoni" in identity_path.lower():
                    label = "dhoni"
                elif "pvsindhu" in identity_path.lower():
                    label = "pvsindhu"

        except:
            label = "unknown"

        try:
            analysis = DeepFace.analyze(
                img_path=filepath,
                actions=['emotion'],
                enforce_detection=False
            )
            emotion = analysis[0]['dominant_emotion']
        except:
            emotion = "unknown"

        img_data = {"path": "/" + filepath, "emotion": emotion}

        if label == "dhoni":
            dhoni_list.append(img_data)
        elif label == "pvsindhu":
            pvsindhu_list.append(img_data)
        else:
            unknown_list.append(img_data)

    return render_template(
        "gallery.html",
        dhoni=dhoni_list,
        pvsindhu=pvsindhu_list,
        unknown=unknown_list
    )


# --------- Live Camera ----------
@app.route("/live_camera")
def live_camera():
    return render_template("live_camera.html")


@app.route("/capture_live", methods=["POST"])
def capture_live():
    file = request.files.get("file")
    if not file:
        return "No file received", 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    dhoni_list = []
    pvsindhu_list = []
    unknown_list = []

    label = "unknown"
    emotion = "unknown"

    try:
        result = DeepFace.find(img_path=filepath, db_path=DATASET_PATH, enforce_detection=False, model_name="Facenet")
        if len(result) > 0 and len(result[0]) > 0:
            identity_path = result[0]['identity'][0]
            if "dhoni" in identity_path.lower():
                label = "dhoni"
            elif "pvsindhu" in identity_path.lower():
                label = "pvsindhu"
    except:
        label = "unknown"

    try:
        analysis = DeepFace.analyze(img_path=filepath, actions=['emotion'], enforce_detection=False)
        emotion = analysis[0]['dominant_emotion']
    except:
        emotion = "unknown"

    img_data = {"path": "/" + filepath, "emotion": emotion}

    if label == "dhoni":
        dhoni_list.append(img_data)
    elif label == "pvsindhu":
        pvsindhu_list.append(img_data)
    else:
        unknown_list.append(img_data)

    return render_template(
        "gallery.html",
        dhoni=dhoni_list,
        pvsindhu=pvsindhu_list,
        unknown=unknown_list
    )


if __name__ == "__main__":
    app.run(debug=True)