from deepface import DeepFace
import os

DATASET_PATH = "dataset"

print("Loading DeepFace model...")

# Load model (this is your 'training')
model = DeepFace.build_model("VGG-Face")

print("Model loaded ✅")

# Scan dataset
print("Processing dataset...")

for person in os.listdir(DATASET_PATH):
    person_path = os.path.join(DATASET_PATH, person)

    for img in os.listdir(person_path):
        img_path = os.path.join(person_path, img)

        try:
            # Just detect face once (pre-processing)
            DeepFace.extract_faces(img_path, enforce_detection=False)
            print(f"Processed: {img_path}")
        except:
            print(f"Skipped: {img_path}")

print("DeepFace setup completed ✅")