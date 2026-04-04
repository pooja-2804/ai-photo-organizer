from deepface import DeepFace

result = DeepFace.verify(
    img1_path="dataset/dhoni/dhoni1.jpg",
    img2_path="dataset/dhoni/dhoni2.jpg"
)

print(result)