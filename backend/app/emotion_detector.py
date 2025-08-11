# app/emotion_detector.py
import cv2
from deepface import DeepFace
import numpy as np
import base64

def detect_emotion_from_frame(frame):
    """
    Detects emotion from a BGR image frame (OpenCV format).
    Returns (emotion_label, confidence_score) or (None, None) if failed.
    """
    try:
        # DeepFace expects RGB images
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Analyze emotions
        result = DeepFace.analyze(rgb_frame, actions=['emotion'], enforce_detection=False)

        # Extract dominant emotion and its score
        dominant_emotion = result[0]['dominant_emotion']
        confidence = result[0]['emotion'][dominant_emotion]

        return dominant_emotion, confidence

    except Exception as e:
        print(f"Error detecting emotion: {e}")
        return None, None


def detect_emotion_from_base64(img_base64):
    """
    Detects emotion from a base64 encoded image string.
    Useful when frontend sends webcam frame as base64.
    """
    try:
        # Decode base64 → bytes → numpy array
        img_bytes = base64.b64decode(img_base64.split(",")[-1])
        np_arr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        return detect_emotion_from_frame(frame)

    except Exception as e:
        print(f"Error decoding base64: {e}")
        return None, None


if __name__ == "__main__":
    # Quick test using your webcam
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        emotion, score = detect_emotion_from_frame(frame)
        if emotion:
            text = f"{emotion} ({score:.2f}%)"
            cv2.putText(frame, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 255, 0), 2)

        cv2.imshow("Emotion Detector Test", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
