
import cv2

def open_webcam():
    
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ Error: Could not open webcam.")
        return

    print("✅ Press 'q' to quit webcam preview.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Error: Failed to read frame.")
            break
        
       # Flip the frame horizontally (mirror effect)
        frame = cv2.flip(frame, 1)

        # Show the frame in a window
        cv2.imshow("Webcam Feed", frame)

        # Exit when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    open_webcam()
