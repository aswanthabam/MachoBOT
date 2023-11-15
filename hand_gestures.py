import cv2
import mediapipe

mp_hands = mediapipe.solutions.hands
hands = mp_hands.Hands()

# Create a capture object
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the camera
    success, img = cap.read()

    # Convert the image to RGB format
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Detect hands in the image
    results = hands.process(img)

    # Check if any hands were detected
    if results.multi_hand_landmarks:
        # Loop through each detected hand
        for hand_landmarks in results.multi_hand_landmarks:
            # Get the hand's bounding box
            bbox = hand_landmarks.bounding_box

            # Get the hand's center point
            center = bbox.center

            # Get the hand's radius
            radius = bbox.height / 2

            # Draw a circle around the hand
            cv2.circle(img, center, radius, (255, 0, 0), 2)

    # Display the image
    cv2.imshow('Hand Tracking', img)

    # Check if the user wants to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Close the capture object
cap.release()