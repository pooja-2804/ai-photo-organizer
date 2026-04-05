from deepface import DeepFace

result = DeepFace.verify(
    img1_path="dataset/dhoni/Dhoni1.jpg",
    img2_path="dataset/dhoni/Dhoni2.jpg"
)

print(result)