# import cv2
# import tempfile
# from deepface import DeepFace

# def capture_and_detect_mood():
#     cap = cv2.VideoCapture(0)

#     if not cap.isOpened():
#         return "Unable to access webcam"

#     stframe = None
#     cv2.namedWindow("Press 's' to capture and 'q' to quit", cv2.WINDOW_NORMAL)
    
#     mood = None
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break

#         cv2.imshow("Press 's' to capture and 'q' to quit", frame)

#         key = cv2.waitKey(1)
#         if key == ord('s'):
#             # Save image to temp file
#             with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
#                 cv2.imwrite(tmp.name, frame)
#                 try:
#                     result = DeepFace.analyze(img_path=tmp.name, actions=['emotion'])
#                     mood = result[0]['dominant_emotion'].capitalize()
#                 except Exception as e:
#                     mood = f"Error: {e}"
#                 break
#         elif key == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()
#     return mood
