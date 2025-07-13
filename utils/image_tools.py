from PIL import Image, ImageDraw
import cv2
import numpy as np
import streamlit as st
from utils.logger import log_action

def create_image(st):
    st.subheader("🖼️ Create Digital Image")
    if st.button("Generate Image"):
        try:
            img = Image.new('RGB', (800, 600), color='white')
            draw = ImageDraw.Draw(img)
            draw.rectangle([50, 50, 750, 550], outline='black')
            draw.ellipse([200, 150, 600, 450], fill='blue')
            path = 'digital_image.png'
            img.save(path)
            st.image(path, caption="Generated Image")
            st.success("✅ Image created successfully!")
            log_action("Digital image created")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            log_action(f"Image creation error: {str(e)}")


def real_time_face_swap(st):
    st.subheader("👥 Real-Time Face Swap")
    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    captured_faces = []
    instructions = ["Show face 1 and press 's' to capture", "Show face 2 and press 's' again"]

    while len(captured_faces) < 2:
        ret, frame = cap.read()
        if not ret:
            st.warning("Failed to capture video frame.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        cv2.putText(frame, instructions[len(captured_faces)], (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Face Swap", frame)
        key = cv2.waitKey(1)
        if key == ord('s'):
            if len(faces) > 0:
                (x, y, w, h) = faces[0]
                face_img = frame[y:y+h, x:x+w].copy()
                captured_faces.append((face_img, (x, y, w, h)))
            else:
                print("No face detected.")
        elif key == ord('q'):
            break

    if len(captured_faces) == 2:
        _, (x1, y1, w1, h1) = captured_faces[0]
        _, (x2, y2, w2, h2) = captured_faces[1]

        final_frame = frame.copy()
        face1_resized = cv2.resize(captured_faces[0][0], (w2, h2))
        face2_resized = cv2.resize(captured_faces[1][0], (w1, h1))

        final_frame[y1:y1+h1, x1:x1+w1] = face2_resized
        final_frame[y2:y2+h2, x2:x2+w2] = face1_resized

        cv2.imshow("Swapped Faces", final_frame)
        cv2.waitKey(0)
        log_action("Face swap done")
    else:
        st.error("❌ Failed to capture both faces.")

    cap.release()
    cv2.destroyAllWindows()
